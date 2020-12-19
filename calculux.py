import sys
from dataclasses import dataclass
from typing import Callable, Any
import PyQt5.QtWidgets as qw
import PyQt5.QtGui as qg
from PyQt5.QtCore import Qt


@dataclass
class Button:
    row: int
    col: int
    label_1: str
    connection_1: Callable[..., Any] = None
    label_2: str = ''
    connection_2: Callable[..., Any] = None
    label_3: str = ''
    connection_3: Callable[..., Any] = None
    ref_1: qw.QWidget = None
    ref_2: qw.QWidget = None
    ref_3: qw.QWidget = None


class Calculux(qw.QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Calculux')

        # setup the central widget
        self._centralWidget = qw.QWidget(self)
        self.setCentralWidget(self._centralWidget)

        # create the layout
        self.grid = qw.QGridLayout()
        self._centralWidget.setLayout(self.grid)

        # create dictionary to hold all button references
        self.buttons = {Qt.Key_0: Button(5, 1, '0'),
                        Qt.Key_1: Button(4, 0, '1'),
                        Qt.Key_2: Button(4, 1, '2'),
                        Qt.Key_3: Button(4, 2, '3'),
                        Qt.Key_4: Button(3, 0, '4'),
                        Qt.Key_5: Button(3, 1, '5'),
                        Qt.Key_6: Button(3, 2, '6'),
                        Qt.Key_7: Button(2, 0, '7'),
                        Qt.Key_8: Button(2, 1, '8'),
                        Qt.Key_9: Button(2, 2, '9'),
                        Qt.Key_Period: Button(5, 0, '.'),
                        Qt.Key_ParenLeft: Button(1, 0, '('),
                        Qt.Key_ParenRight: Button(1, 1, ')'),
                        Qt.Key_Asterisk: Button(2, 3, '*'),
                        Qt.Key_Slash: Button(3, 3, '/'),
                        Qt.Key_Plus: Button(4, 3, '+'),
                        Qt.Key_Minus: Button(5, 3, '-'),
                        Qt.Key_Equal: Button(5, 2, '=', self.evaluate),
                        Qt.Key_C: Button(1, 3, 'C', self.clear),
                        Qt.Key_D: Button(1, 2, 'D', self.delete)}

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
            # Buttons must have at least one function so create the first
            # reference, add it to the grid, and connect the functionality
            button.ref_1 = qw.QPushButton(text=button.label_1)
            self.grid.addWidget(button.ref_1, button.row, button.col)
            if button.connection_1 is None:
                # connect default functionality (insert)
                button.ref_1.clicked.connect(self.buttonFactory(button.label_1))
            else:
                # connect special functionality that is already defined in dict
                button.ref_1.clicked.connect(button.connection_1)

            # add the second function if applicable
            if len(button.label_2) > 0:
                button.ref_2 = qw.QPushButton(text=button.label_2)
                # change this to add in top left
                self.grid.addWidget(button.ref_2, button.row, button.col)
                if button.connection_2 is None:
                    button.ref_2.clicked.connect(self.buttonFactory(button.label_2))
                else:
                    button.ref_2.clicked.connect(button.connection_2)

            # add the third function if applicable
            if len(button.label_3) > 0:
                button.ref_3 = qw.QPushButton(text=button.label_3)
                # change this to add in top left
                self.grid.addWidget(button.ref_3, button.row, button.col)
                if button.connection_3 is None:
                    button.ref_3.clicked.connect(self.buttonFactory(button.label_3))
                else:
                    button.ref_3.clicked.connect(button.connection_3)

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

    def buttonFactory(self, text):
        def f():
            self.insert(text)
        return f

    def insert(self, text):
        self.screen.setText(self.screen.text() + text)
        return

    def evaluate(self):
        self.screen.setText(str(eval(self.screen.text())))
        return

    def clear(self):
        self.screen.setText('')
        return

    def delete(self):
        self.screen.setText(self.screen.text()[:-1])
        return


def main():
    calculux = qw.QApplication(sys.argv)
    view = Calculux()
    view.show()
    sys.exit(calculux.exec_())


if __name__ == '__main__':
    main()
