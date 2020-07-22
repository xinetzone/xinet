from xinet.Qt.qt5 import QtCore, QtGui, QtWidgets
from xinet.run_qt import run


class MainWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.setWindowTitle("QFrame")
        self.resize(300, 300)
        #创建一个Frame
        fra = QtWidgets.QFrame(self)
        fra.move(50, 50)  # 移动 frame 位置
        fra.resize(100, 100)
        # 设定背景颜色
        fra.setStyleSheet("background-color:green")
        # 设定外观样式
        fra.setLineWidth(7)  # 设置外线宽度
        fra.setMidLineWidth(5)  # 设置中线宽度'
        fra.setMargin(10)
        fra.setFrameShadow(QtWidgets.QFrame.Raised)  # 设置阴影效果：凸起
        fra.setFrameShape(QtWidgets.QFrame.Box)  # 设置图形为：Box
        fra.setFrameRect(QtCore.QRect(10, 10, 80, 80))  # 这是边框


if __name__ == "__main__":
    run(MainWindow)