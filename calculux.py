import sys
from dataclasses import dataclass
from typing import Callable, Any
from math import sin, asin, cos, acos, tan, atan, sqrt, log, log10, fabs, pi, e
import PyQt5.QtWidgets as qw
from PyQt5.QtCore import Qt


@dataclass
class Button:
    row: int
    col: int
    label_1: str
    connection_1: Callable[..., Any] = None
    label_2: str = ''
    hidden_2: str = ''
    connection_2: Callable[..., Any] = None
    label_3: str = ''
    hidden_3: str = ''
    connection_3: Callable[..., Any] = None
    ref_1: qw.QWidget = None
    ref_2: qw.QWidget = None
    ref_3: qw.QWidget = None
    grid: qw.QGridLayout = None


class Calculux(qw.QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Calculux')

        # setup the central widget
        self._centralWidget = qw.QWidget(self)
        self._centralWidget.setMinimumSize(500, 309)
        self.setCentralWidget(self._centralWidget)

        # load in the styele sheet
        with open('stylesheet.qss', 'r') as stylesheet:
            self.setStyleSheet(stylesheet.read())

        # create the layout and assign it to the central widget
        self.grid = qw.QGridLayout()
        self.grid.setHorizontalSpacing(0)
        self.grid.setVerticalSpacing(0)
        self._centralWidget.setLayout(self.grid)

        # create dictionary to hold all Button references
        self.buttons = {Qt.Key_0: Button(4, 0, '0', None, 'pi', '', None, 'e', '', None),
                        Qt.Key_1: Button(3, 0, '1', None, 'tan', '(', None, 'atan', '(', None),
                        Qt.Key_2: Button(3, 1, '2', None, '(', '', None, ')', '', None),
                        Qt.Key_3: Button(3, 2, '3', None, 'PRE', '', None, ' ', '', self.noAction),
                        Qt.Key_4: Button(2, 0, '4', None, 'cos', '(', None, 'acos', '(', None),
                        Qt.Key_5: Button(2, 1, '5', None, 'MC', '', self.memory_clear, 'M', '', None),
                        Qt.Key_6: Button(2, 2, '6', None, 'M+', '', self.memory_add, 'M-', '', self.memory_subtract),
                        Qt.Key_7: Button(1, 0, '7', None, 'sin', '(', None, 'asin', '(', None),
                        Qt.Key_8: Button(1, 1, '8', None, 'log10', '(', None, 'ln', '(', None),
                        Qt.Key_9: Button(1, 2, '9', None, 'log', '(', None, ',', '', None),
                        Qt.Key_Period: Button(4, 1, '.', None, 'E', '', None, '^2', '', None),
                        Qt.Key_Asterisk: Button(1, 3, '*', None, '!', '', None, '^', '', None),
                        Qt.Key_Slash: Button(2, 3, '/', None, 'mod', '(', None, 'deg/rad', '', None),
                        Qt.Key_Plus: Button(3, 3, '+', None, 'sqrt', '(', None, 'x_rt', '(', None),
                        Qt.Key_Minus: Button(4, 3, '-', None, 'abs', '(', None, 'i', '', None),
                        Qt.Key_Equal: Button(4, 2, '=', self.evaluate, 'C', '', self.clear, 'D', '', self.delete)}

        # define key translations when multiple keys perform the same function
        self.keyTranslations = {Qt.Key_Enter: Qt.Key_Equal,
                                Qt.Key_Return: Qt.Key_Equal}

        # create screen and add it to the grid
        self.screen = qw.QLineEdit()
        self.screen.setAlignment(Qt.AlignRight)
        self.screen.setReadOnly(True)
        self.grid.addWidget(self.screen, 0, 0, 1, 4)

        # create the buttons
        for button in self.buttons.values():
            # create subgrid for button and add it to the main grid
            button.grid = qw.QGridLayout()
            self.grid.addLayout(button.grid, button.row, button.col)

            # Buttons must have at least one function so create the first
            # reference, add it to the grid, and connect the functionality
            button.ref_1 = self.createButtonFunction(button.grid, button.label_1, button.connection_1, 'FIRST')

            # add the second function if applicable
            if len(button.label_2) > 0:
                button.label_2 = self.createButtonFunction(button.grid, button.label_2, button.connection_2, 'SECOND', button.hidden_2)

            # add the third function if applicable
            if len(button.label_3) > 0:
                button.label_3 = self.createButtonFunction(button.grid, button.label_3, button.connection_3, 'THIRD', button.hidden_3)

        # initialize memory and previous result
        self.memory = 0
        self.previous_result = ''

        return

    def keyPressEvent(self, event):
        # check if this key needs to be translated
        if event.key() in self.keyTranslations:
            key = self.keyTranslations[event.key()]
        else:
            key = event.key()

        if key in self.buttons:
            # get the Button
            button = self.buttons[key]

            # use modifiers() to determine which reference to animateClick on
            # and therefore which function to perform
            if event.modifiers() & Qt.AltModifier and button.ref_2 is not None:
                # second function
                button.ref_2.animateClick()
            elif event.modifiers() & Qt.ControlModifier and button.ref_3 is not None:
                # third function
                button.ref_3.animateClick()
            else:
                # first / main funciton
                button.ref_1.animateClick()

        return

    def createButtonFunction(self, grid, label, connection, function, hidden=''):
        ref = qw.QPushButton(text=label)
        ref.setFlat(True)
        ref.setSizePolicy(qw.QSizePolicy.Expanding, qw.QSizePolicy.Expanding)

        if function == 'FIRST':
            grid.addWidget(ref, 1, 0, 1, 2)
        elif function == 'SECOND':
            grid.addWidget(ref, 0, 0)
        elif function == 'THIRD':
            grid.addWidget(ref, 0, 1)

        if connection is None:
            # connect default functionality (insert)
            ref.clicked.connect(self.buttonFactory(label+hidden))
        else:
            # connect special functionality that is already defined in dict
            ref.clicked.connect(connection)

        return ref

    def buttonFactory(self, text):
        def f():
            self.insert(text)
        return f

    def insert(self, text):
        self.screen.setText(self.screen.text() + text)
        return

    def evaluate(self):
        expression = self.screen.text()

        if len(expression) > 0 and expression != 'ERROR':
            expression = self.parse(expression)

            try:
                result = eval(expression)
            except SyntaxError:
                self.screen.setText('ERROR')
            else:
                result = str(result)
                result = result.replace('e', 'E')
                self.screen.setText(result)
                self.previous_result = result
        return

    def parse(self, expression: str) -> str:
        expression = expression.replace('abs', 'fabs')
        expression = expression.replace('PRE', self.previous_result)
        expression = expression.replace('ln', 'self.ln')
        expression = expression.replace('E', '*10**')
        expression = expression.replace('^', '**')
        expression = expression.replace('x_rt', 'self.x_rt')
        expression = expression.replace('mod', 'self.mod')
        expression = expression.replace('M', str(self.memory_get()))

        # TODO: will need more complex work for factorial

        return expression

    def clear(self):
        self.screen.setText('')
        return

    def delete(self):
        self.screen.setText(self.screen.text()[:-1])
        return

    def noAction(self):
        return

    def ln(self, x):
        return log(x, e)

    def x_rt(self, x, expr):
        return expr ** (1.0/x)

    def mod(self, x, expr):
        return expr % x

    def factorial(self, x):
        return

    def memory_clear(self):
        self.memory = 0
        return

    def memory_get(self):
        return self.memory

    def memory_add(self):
        self.evaluate()
        self.memory += float(self.screen.text())
        return

    def memory_subtract(self):
        self.evaluate()
        self.memory -= float(self.screen.text())
        return


def main():
    calculux = qw.QApplication(sys.argv)
    view = Calculux()
    view.show()
    sys.exit(calculux.exec_())


if __name__ == '__main__':
    main()
