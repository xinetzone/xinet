from xinet.Qt.qt5 import QtCore, QtGui, QtWidgets  # , Signal, Slot
from xinet.run_qt import run


class DrawBezierCurve(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.painter = QtGui.QPainter()
        self.pen = QtGui.QPen()

    def initUI(self):
        self.setGeometry(500, 500, 380, 280)

    def paintEvent(self, e):
        self.painter.begin(self)
        # 反锯齿，边缘柔化、消除混叠、反走样
        self.painter.setRenderHint(QtGui.QPainter.Antialiasing)
        self.draw_something()
        self.painter.end()

    def draw_something(self):
        path = QtGui.QPainterPath()
        path.moveTo(30, 30)
        path.cubicTo(30, 30, 200, 350, 350, 30)

        self.painter.drawPath(path)


if __name__ == "__main__":
    run(DrawBezierCurve)
