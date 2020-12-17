import sys
import PyQt5.QtWidgets as qw
import PyQt5.QtGui as qg
from PyQt5.QtCore import Qt


class UserInterface(qw.QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Calculux')

        self._centralWidget = qw.QWidget(self)
        self.setCentralWidget(self._centralWidget)

        self.grid = qw.QGridLayout()

        # create number buttons
        self.numbers = []
        for i in range(10):
            self.numbers.append(qw.QPushButton(text=str(i)))

        self.numbers[1].clicked.connect(self.print_1)

        # add number buttons to display
        btn = iter(self.numbers)
        self.grid.addWidget(next(btn), 3, 1)
        for i in range(2, -1, -1):
            for j in range(3):
                self.grid.addWidget(next(btn), i, j)

        # create and add other buttons
        self.decimal = qw.QPushButton(text='.')
        self.grid.addWidget(self.decimal, 3, 0)

        self.equals = qw.QPushButton(text='=')
        self.grid.addWidget(self.equals, 3, 2)

        self.multiply = qw.QPushButton(text='*')
        self.grid.addWidget(self.multiply, 0, 3)

        self.divide = qw.QPushButton(text='/')
        self.grid.addWidget(self.divide, 1, 3)

        self.subtract = qw.QPushButton(text='-')
        self.grid.addWidget(self.subtract, 2, 3)

        self.add = qw.QPushButton(text='+')
        self.grid.addWidget(self.add, 3, 3)

        self._centralWidget.setLayout(self.grid)

        return

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_0:
            self.numbers[0].animateClick()
        elif event.key() == Qt.Key_1:
            self.numbers[1].animateClick()
        elif event.key() == Qt.Key_2:
            self.numbers[2].animateClick()
        elif event.key() == Qt.Key_3:
            self.numbers[3].animateClick()
        elif event.key() == Qt.Key_4:
            self.numbers[4].animateClick()
        elif event.key() == Qt.Key_5:
            self.numbers[5].animateClick()
        elif event.key() == Qt.Key_6:
            self.numbers[6].animateClick()
        elif event.key() == Qt.Key_7:
            self.numbers[7].animateClick()
        elif event.key() == Qt.Key_8:
            self.numbers[8].animateClick()
        elif event.key() == Qt.Key_9:
            self.numbers[9].animateClick()
        elif event.key() == Qt.Key_Asterisk:
            self.multiply.animateClick()
        elif event.key() == Qt.Key_Slash:
            self.divide.animateClick()
        elif event.key() == Qt.Key_Minus:
            self.subtract.animateClick()
        elif event.key() == Qt.Key_Plus:
            self.add.animateClick()
        elif event.key() == Qt.Key_Equal:
            self.equals.animateClick()
        elif event.key() == Qt.Key_Period:
            self.decimal.animateClick()

        return

    def print_1(self):
        print(1)
        return


def main():
    calculux = qw.QApplication(sys.argv)
    view = UserInterface()
    view.show()
    sys.exit(calculux.exec_())

if __name__ == '__main__':
    main()
