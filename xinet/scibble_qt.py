from Qt.qt5 import QtCore, QtGui, QtWidgets, Signal, Slot

def run(window_type, *args, **kwargs):
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = window_type(*args, **kwargs)
    window.show()
    app.exec_()


if __name__ == "__main__":
    run(ScribbleWindow)