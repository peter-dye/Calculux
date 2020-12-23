# fman build system imports
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from fbs_runtime.platform import is_mac

# python built-in imports
import sys
from dataclasses import dataclass
from typing import Callable, Any
from cmath import sin, asin, cos, acos, tan, atan, sqrt, log, log10, pi, e

# PyQt5 imports
import PyQt5.QtWidgets as qw
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt, QEvent, QObject


@dataclass
class Button:
    """
    Holds all the information associated with a button, including
    all three functions: primary, secondary, and tertiary.

    Note that a button consists of 3 push buttons, with the functionalities
    mapped as:

    |-----------|----------|
    | secondary | tertiary |
    |----------------------|
    |        primary       |
    |----------------------|
    """
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
    """
    Creates and runs the user interface.
    """

    def __init__(self, appctxt):
        super().__init__()

        # hold the reference to fbs ApplicationContext to access runtime variables
        # and resources
        self.appctxt = appctxt

        # set the window title
        self.setWindowTitle('Calculux')

        # set up the central widget
        self.centralWidget = qw.QWidget(self)
        self.centralWidget.setMinimumSize(500, 500)
        self.centralWidget.setObjectName('centralWidget')
        self.setCentralWidget(self.centralWidget)

        # add the about menu (for macs)
        self.aboutAction = qw.QAction()
        self.aboutAction.setMenuRole(qw.QAction.AboutRole)
        self.aboutAction.triggered.connect(self.showAboutWindow)
        self.mainMenuBar = qw.QMenuBar()
        self.mainMenu = qw.QMenu()
        self.mainMenuBar.addMenu(self.mainMenu)
        self.mainMenu.addAction(self.aboutAction)
        self.setMenuBar(self.mainMenuBar)

        # load in the style sheet
        with open(self.appctxt.get_resource('stylesheet.qss'), 'r') as stylesheet:
            self.setStyleSheet(stylesheet.read())

        # create the layout and assign it to the central widget
        self.grid = qw.QGridLayout()
        self.grid.setHorizontalSpacing(0)
        self.grid.setVerticalSpacing(0)
        self.centralWidget.setLayout(self.grid)

        # create dictionary to hold all Button references and define the 3
        # functionalities of each button
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
            Qt.Key_Minus: Button(4, 3, '-', None, 'abs', '(', None, 'j', '', None),
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
            Qt.Key_Delete: QKeyEvent(QEvent.KeyPress, Qt.Key_Equal, Qt.ControlModifier),
            Qt.Key_Backspace: QKeyEvent(QEvent.KeyPress, Qt.Key_Equal, Qt.ControlModifier),
            Qt.Key_I: QKeyEvent(QEvent.KeyPress, Qt.Key_Minus, Qt.ControlModifier),
            Qt.Key_Comma: QKeyEvent(QEvent.KeyPress, Qt.Key_9, Qt.ControlModifier),
            Qt.Key_E: QKeyEvent(QEvent.KeyPress, Qt.Key_Period, Qt.AltModifier)
        }

        # create display and add it to the grid
        self.display = qw.QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setMinimumHeight(60)
        self.display.installEventFilter(self)
        self.grid.addWidget(self.display, 0, 0, 1, 4)

        # create the buttons
        for button in self.buttons.values():
            # create subgrid for button and add it to the main grid
            button.grid = qw.QGridLayout()
            self.grid.addLayout(button.grid, button.row, button.col)

            # Buttons must have at least one function so create the first
            # reference, add it to the grid, and connect the functionality
            button.ref_1 = self.createButtonFunctionality(button.grid, button.label_1, button.connection_1, 'FIRST')

            # add the second function if applicable
            if len(button.label_2) > 0:
                button.ref_2 = self.createButtonFunctionality(button.grid, button.label_2, button.connection_2, 'SECOND', button.hidden_2)

            # add the third function if applicable
            if len(button.label_3) > 0:
                button.ref_3 = self.createButtonFunctionality(button.grid, button.label_3, button.connection_3, 'THIRD', button.hidden_3)

        # initialize memory and previous result variables
        self.memory = 0
        self.previous_result = ''
        self.last_operation_was_evaluate = False

        return

    def keyPressEvent(self, orig_event: QKeyEvent) -> None:
        """
        Re-definition of QWidget.keyPressEvent(). This function is called by Qt
        every time a key press is registered in the MainWindow / centralWidget.
        """
        # check if this key needs to be translated
        if orig_event.key() in self.keyTranslations:
            # get the translated event
            event = self.keyTranslations[orig_event.key()]
            translated = True

            # if the translation does not specify modifiers, keep the original modifiers
            if not event.modifiers() & Qt.AltModifier and not event.modifiers() & Qt.ControlModifier:
                event = QKeyEvent(QEvent.KeyPress, event.key(), orig_event.modifiers())
                translated = False
        else:
            # otherwise use the original event
            event = orig_event
            translated = False

        # if a valid key was pressed
        if event.key() in self.buttons:
            # get the Button corresponding to the key
            button = self.buttons[event.key()]

            # check for mac or windows to know to switch what funcitons Alt
            # and Ctrl correspond to
            if is_mac() or translated:
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
            else:
                # use modifiers() to determine which reference to animateClick on
                # and therefore which function to perform
                if event.modifiers() & Qt.ControlModifier and button.ref_2 is not None:
                    # second function
                    button.ref_2.animateClick()
                elif event.modifiers() & Qt.AltModifier and button.ref_3 is not None:
                    # third function
                    button.ref_3.animateClick()
                else:
                    # first / main funciton
                    button.ref_1.animateClick()

        return

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        """
        Filters events for the display in order to get backspace and delete key
        presses. Otherwise they go straight to the display (because they the are
        shortcuts I think) and do nothing (because the display is not editable).
        """
        if obj == self.display:
            if event.type() == QEvent.KeyPress:
                self.keyPressEvent(event)
                return True
            else:
                return False

    def showAboutWindow(self):
        """
        Creates and displays the About window on Mac.
        """
        self.aboutWindow = AboutWindow()
        self.aboutWindow.show()
        return

    def createButtonFunctionality(self, grid: qw.QGridLayout, label: str, connection: Callable, function: str, hidden='') -> Callable:
        """
        Creates a specific functionality for a button, and handles all
        associated setup.
        """
        # create the push button object and apply basic styling
        ref = qw.QPushButton(text=label)
        ref.setFlat(True)
        ref.setSizePolicy(qw.QSizePolicy.Expanding, qw.QSizePolicy.Expanding)

        # place push button in correct spot for that functionality
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
        """
        Creates the default functionality for a push button (inserting it's text
        to the display).
        """
        def f():
            self.insert(text)
        return f

    def insert(self, text: str) -> None:
        """
        Inserts number or operator to the far right of the display.
        """
        # clear the display if the last operation was an evaluation
        if self.last_operation_was_evaluate:
            self.display.setText('')
            self.last_operation_was_evaluate = False

        # instert the number/operator
        self.display.setText(self.display.text() + text)

        return

    def evaluate(self) -> None:
        """
        Takes in the expression on the display and displays the result.
        """
        expression = self.display.text()

        # check that there is something to evaluate
        if len(expression) > 0 and expression != 'ERROR':
            # parse the operation to a valid python math string
            expression = self.parse(expression)

            try:
                # attempt to evaluate the expression
                result = eval(expression)
            except SyntaxError:
                # user probably entered an invalid math string
                self.display.setText('ERROR')
            else:
                # if the string was able to be evaluated
                # check if result is complex number
                if isinstance(result, complex):
                    if result.imag == 0:
                        # return a real number if imag part is 0
                        result = str(round(result.real, 5))
                    else:
                        # pretty print the complex number
                        result = complex(round(result.real, 5), round(result.imag, 5))
                        result = str(result)[1:-1]  # remove the parentheses
                else:
                    result = str(round(result, 5))

                # prepare the result and display it
                result = result.replace('e', 'E')
                self.display.setText(result)

                self.previous_result = result

        self.last_operation_was_evaluate = True

        return

    def parse(self, expression: str) -> str:
        """
        Performs a series of string substitutions to manipulate the text from
        the display, into a string that can be properly evaluated with the
        eval() function.
        """
        expression = expression.replace('fact', 'self.factorial')
        expression = expression.replace('PRV', self.previous_result)
        expression = expression.replace('ln', 'self.ln')
        expression = expression.replace('E', '*10**')
        expression = expression.replace('^', '**')
        expression = expression.replace('x_rt', 'self.x_rt')
        expression = expression.replace('mod', 'self.mod')
        expression = expression.replace('M', str(self.memory_get()))
        expression = expression.replace('j', '*1j')
        return expression

    def clear(self) -> None:
        """
        Clears the display.
        """
        self.display.setText('')
        return

    def delete(self) -> None:
        """
        Deleted the right-most character on the display.
        """
        self.display.setText(self.display.text()[:-1])
        return

    def noAction(self) -> None:
        """
        Does nothing. Used as the connection for empty buttons so they can still
        be properly created like the other ones.
        """
        return

    def ln(self, x: float) -> float:
        """
        Returns the natural logarithm of input x.
        """
        return log(x, e)

    def x_rt(self, x: float, expr: float) -> float:
        """
        Returns the xth root of input expression.
        """
        return expr ** (1.0/x)

    def mod(self, expr: int, x: int):
        """
        Returns the modulo of the input expression by x.
        """
        return expr % x

    def factorial(self, x: int) -> int:
        """
        Returns the factorial of x.
        """
        return factorial(x)

    def memory_clear(self) -> None:
        """
        Clears the value stored in memory.
        """
        self.memory = 0
        return

    def memory_get(self) -> float:
        """
        Returns the value stored in memory.
        """
        return self.memory

    def memory_add(self) -> None:
        """
        Adds (as in sum) the result of the display to memory.
        """
        self.evaluate()
        if self.display.text() != 'ERROR':
            self.memory += float(self.display.text())
        return

    def memory_subtract(self) -> None:
        """
        Subtracts the result of the display from memory.
        """
        self.evaluate()
        if self.display.text() != 'ERROR':
            self.memory -= float(self.display.text())
        return


class AboutWindow(qw.QWidget):
    """
    Sets information and layout of the AboutWindow.
    (only used on mac)
    """

    def __init__(self):
        super().__init__()

        self.info = [
            'Calculux',
            'Version: v0',
            'Author: Peter Dye',
            'Website: https://github.com/peter-dye/Calculux',
            'License: GNU GPL-3.0'
        ]

        self.layout = qw.QVBoxLayout()

        for label in self.info:
            self.layout.addWidget(qw.QLabel(text=label))

        self.setLayout(self.layout)

        return


def main():
    appctxt = ApplicationContext()  # needed for fbs
    view = Calculux(appctxt)  # create the main window
    view.show()  # show the main window
    exit_code = appctxt.app.exec_()  # needed for fbs
    sys.exit(exit_code)  # exit the app


if __name__ == '__main__':
    main()
