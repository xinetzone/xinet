from xinet.Qt.qt5 import QtCore, QtGui, QtWidgets, Signal
from xinet.run_qt import run

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

if __name__ == '__main__':
    run(MainWindow)