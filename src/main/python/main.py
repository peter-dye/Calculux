from fbs_runtime.application_context.PyQt5 import ApplicationContext
import sys
from dataclasses import dataclass
from typing import Callable, Any
from math import sin, asin, cos, acos, tan, atan, sqrt, log, log10, fabs, factorial, pi, e
import PyQt5.QtWidgets as qw
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt, QEvent


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

    def __init__(self, appctxt):
        super().__init__()

        self.appctxt = appctxt

        self.setWindowTitle('Calculux')

        # setup the central widget
        self.centralWidget = qw.QWidget(self)
        self.centralWidget.setMinimumSize(500, 500)
        self.centralWidget.setObjectName('centralWidget')
        self.setCentralWidget(self.centralWidget)

        # load in the style sheet
        with open(self.appctxt.get_resource('stylesheet.qss'), 'r') as stylesheet:
            self.setStyleSheet(stylesheet.read())

        # create the layout and assign it to the central widget
        self.grid = qw.QGridLayout()
        self.grid.setHorizontalSpacing(0)
        self.grid.setVerticalSpacing(0)
        self.centralWidget.setLayout(self.grid)

        # create dictionary to hold all Button references
        self.buttons = {
            Qt.Key_0: Button(4, 0, '0', None, 'pi', '', None, 'e', '', None),
            Qt.Key_1: Button(3, 0, '1', None, 'tan', '(', None, 'atan', '(', None),
            Qt.Key_2: Button(3, 1, '2', None, '(', '', None, ')', '', None),
            Qt.Key_3: Button(3, 2, '3', None, 'PRV', '', None, ' ', '', self.noAction),
            Qt.Key_4: Button(2, 0, '4', None, 'cos', '(', None, 'acos', '(', None),
            Qt.Key_5: Button(2, 1, '5', None, 'MC', '', self.memory_clear, 'M', '', None),
            Qt.Key_6: Button(2, 2, '6', None, 'M+', '', self.memory_add, 'M-', '', self.memory_subtract),
            Qt.Key_7: Button(1, 0, '7', None, 'sin', '(', None, 'asin', '(', None),
            Qt.Key_8: Button(1, 1, '8', None, 'log10', '(', None, 'ln', '(', None),
            Qt.Key_9: Button(1, 2, '9', None, 'log', '(', None, ',', '', None),
            Qt.Key_Period: Button(4, 1, '.', None, 'E', '', None, '^2', '', None),
            Qt.Key_Asterisk: Button(1, 3, '*', None, 'fact', '(', None, '^', '', None),
            Qt.Key_Slash: Button(2, 3, '/', None, 'mod', '(', None, 'rad', '', None),
            Qt.Key_Plus: Button(3, 3, '+', None, 'sqrt', '(', None, 'x_rt', '(', None),
            Qt.Key_Minus: Button(4, 3, '-', None, 'abs', '(', None, 'i', '', None),
            Qt.Key_Equal: Button(4, 2, '=', self.evaluate, 'C', '', self.clear, 'D', '', self.delete)
        }

        # define key translations when multiple keys perform the same function
        self.keyTranslations = {
            Qt.Key_Enter: QKeyEvent(QEvent.KeyPress, Qt.Key_Equal, Qt.NoModifier),
            Qt.Key_Return: QKeyEvent(QEvent.KeyPress, Qt.Key_Equal, Qt.NoModifier),
            Qt.Key_Exclam: QKeyEvent(QEvent.KeyPress, Qt.Key_Asterisk, Qt.AltModifier),
            Qt.Key_Percent: QKeyEvent(QEvent.KeyPress, Qt.Key_Slash, Qt.AltModifier),
            Qt.Key_ParenLeft: QKeyEvent(QEvent.KeyPress, Qt.Key_2, Qt.AltModifier),
            Qt.Key_ParenRight: QKeyEvent(QEvent.KeyPress, Qt.Key_2, Qt.ControlModifier),
            Qt.Key_S: QKeyEvent(QEvent.KeyPress, Qt.Key_7, Qt.AltModifier),
            Qt.Key_C: QKeyEvent(QEvent.KeyPress, Qt.Key_4, Qt.AltModifier),
            Qt.Key_T: QKeyEvent(QEvent.KeyPress, Qt.Key_1, Qt.AltModifier),
            Qt.Key_Escape: QKeyEvent(QEvent.KeyPress, Qt.Key_Equal, Qt.AltModifier),
            # Qt.Key_Delete: QKeyEvent(QEvent.KeyPress, Qt.Key_Equal, Qt.ControlModifier),  # not working
            # Qt.Key_Backspace: QKeyEvent(QEvent.KeyPress, Qt.Key_Equal, Qt.ControlModifier),  # not working
            Qt.Key_I: QKeyEvent(QEvent.KeyPress, Qt.Key_Minus, Qt.ControlModifier),
            Qt.Key_Comma: QKeyEvent(QEvent.KeyPress, Qt.Key_9, Qt.ControlModifier),
            Qt.Key_E: QKeyEvent(QEvent.KeyPress, Qt.Key_Period, Qt.AltModifier)
        }

        # create screen and add it to the grid
        self.screen = qw.QLineEdit()
        self.screen.setAlignment(Qt.AlignRight)
        self.screen.setReadOnly(True)
        self.screen.setMinimumHeight(60)
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
                button.ref_2 = self.createButtonFunction(button.grid, button.label_2, button.connection_2, 'SECOND', button.hidden_2)

            # add the third function if applicable
            if len(button.label_3) > 0:
                button.ref_3 = self.createButtonFunction(button.grid, button.label_3, button.connection_3, 'THIRD', button.hidden_3)

        # initialize memory and previous result
        self.memory = 0
        self.previous_result = ''
        self.last_operation_was_evaluate = False

        return

    def keyPressEvent(self, orig_event: QKeyEvent) -> None:
        # check if this key needs to be translated
        if orig_event.key() in self.keyTranslations:
            event = self.keyTranslations[orig_event.key()]

            if not event.modifiers() & Qt.AltModifier and not event.modifiers() & Qt.ControlModifier:
                event = QKeyEvent(QEvent.KeyPress, event.key(), orig_event.modifiers())

        else:
            event = orig_event

        if event.key() in self.buttons:
            # get the Button
            button = self.buttons[event.key()]

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

    def createButtonFunction(self, grid: qw.QGridLayout, label: str, connection: Callable, function: str, hidden='') -> Callable:
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

    def buttonFactory(self, text: str) -> Callable:
        def f():
            self.insert(text)
        return f

    def insert(self, text: str) -> None:
        if self.last_operation_was_evaluate:
            self.screen.setText('')
            self.last_operation_was_evaluate = False

        self.screen.setText(self.screen.text() + text)

        return

    def evaluate(self) -> None:
        expression = self.screen.text()

        if len(expression) > 0 and expression != 'ERROR':
            expression = self.parse(expression)

            try:
                result = eval(expression)
            except SyntaxError:
                self.screen.setText('ERROR')
            else:
                result = str(round(result, 5))
                result = result.replace('e', 'E')
                self.screen.setText(result)
                self.previous_result = result

        self.last_operation_was_evaluate = True

        return

    def parse(self, expression: str) -> str:
        expression = expression.replace('abs', 'fabs')
        expression = expression.replace('fact', 'self.factorial')
        expression = expression.replace('PRV', self.previous_result)
        expression = expression.replace('ln', 'self.ln')
        expression = expression.replace('E', '*10**')
        expression = expression.replace('^', '**')
        expression = expression.replace('x_rt', 'self.x_rt')
        expression = expression.replace('mod', 'self.mod')
        expression = expression.replace('M', str(self.memory_get()))
        return expression

    def clear(self) -> None:
        self.screen.setText('')
        return

    def delete(self) -> None:
        self.screen.setText(self.screen.text()[:-1])
        return

    def noAction(self) -> None:
        return

    def ln(self, x: float) -> float:
        return log(x, e)

    def x_rt(self, x: float, expr: float) -> float:
        return expr ** (1.0/x)

    def mod(self, x: int, expr: int):
        return expr % x

    def factorial(self, x: int) -> int:
        return factorial(x)

    def memory_clear(self) -> None:
        self.memory = 0
        return

    def memory_get(self) -> float:
        return self.memory

    def memory_add(self) -> None:
        self.evaluate()
        if self.screen.text() != 'ERROR':
            self.memory += float(self.screen.text())
        return

    def memory_subtract(self) -> None:
        self.evaluate()
        if self.screen.text() != 'ERROR':
            self.memory -= float(self.screen.text())
        return


def main():
    appctxt = ApplicationContext()
    view = Calculux(appctxt)
    view.show()
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
