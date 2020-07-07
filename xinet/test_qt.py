from Qt.qt5 import QtCore, QtGui, QtWidgets

from run_qt import run


class Drawing(QtWidgets.QWidget):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.setWindowTitle("在窗体中绘画出文字例子")
        self.resize(300, 200)
        self.text = '欢迎学习 PyQt5'

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        # 自定义的绘画方法
        ## 设置笔的颜色
        painter.setPen(QtGui.QColor('purple'))
        ## 设置字体
        painter.setFont(QtGui.QFont('SimSun', 20))
        rect = event.rect()
        print(rect.getRect() == (0, 0, 300, 200))
        # 画出在 widget 中央画出文本
        painter.drawText(rect, QtCore.Qt.AlignCenter, self.text)
        painter.end()


if __name__ == "__main__":
    run(Drawing)
