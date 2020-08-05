from xinet import QtWidgets, QtCore, QtGui, RectItem
from xinet.run_qt import run

Qt = QtCore.Qt
QColor = QtGui.QColor
QPen = QtGui.QPen
QPainter = QtGui.QPainter
QPoint = QtCore.QPoint


class EditorScene(QtWidgets.QGraphicsScene):
    def __init__(self, photo=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._photo = photo

    @property
    def photo(self):
        if self._photo:
            return QtGui.QImage(self._photo)
        else:
            return QtGui.QImage()

    @photo.setter
    def photo(self, photo_name):
        self._photo = photo_name

    def drawBackground(self, painter, rect):
        '''切换图片背景'''
        super().drawBackground(painter, rect)
        if self.photo.isNull():
            self.setBackgroundBrush(QColor(0, 0, 200, 100))  # 默认背景颜色
        else:
            # 设置场景的边界矩形，即可视化区域矩形
            _w = self.photo.width()
            _h = self.photo.height()
            w = _w if _w >500 else 500
            h = _h if _h >500 else 500
            self.setSceneRect(0, 0, w, h)
            painter.drawImage(0, 0, self.photo)


class MainWindow(QtWidgets.QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_Ui()
        # 设定视图尺寸
        self.resize(500, 500)
        # 创建场景
        self.scene = EditorScene('test.jpg')
        # 设定视图的场景
        self.setScene(self.scene)
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        #
        self.lastPos = QPoint()
        self.endPos = QPoint()

    def init_Ui(self):
        self.setViewportUpdateMode(self.FullViewportUpdate)  # 消除重影 移动重影
        self.setDragMode(self.RubberBandDrag)  # 设置可以进行鼠标的拖拽选择
        # 这里是左上角方式显示
        self.setAlignment(Qt.AlignLeft |
                          Qt.AlignTop)
        # 设置渲染属性
        self.setRenderHints(QPainter.Antialiasing |  # 抗锯齿
                            QPainter.HighQualityAntialiasing |  # 高品质抗锯齿
                            QPainter.TextAntialiasing |  # 文字抗锯齿
                            QPainter.SmoothPixmapTransform)  # 使图元变换更加平滑

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        # 鼠标左键按下
        if event.button() == Qt.RightButton:
            self.lastPos = event.pos()
            self.endPos = self.lastPos

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        # 鼠标左键按下的同时移动鼠标
        if event.buttons() and Qt.RightButton:
            self.endPos = event.pos()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        # 鼠标左键释放
        if event.button() == Qt.RightButton:
            x = self.lastPos.x()
            y = self.lastPos.y()
            w = self.endPos.x() - x
            h = self.endPos.y() - y
            # 进行重新绘制
            item = RectItem(x, y, w, h)  # 可塑性矩形
            item.setToolTip('可塑性矩形')
            self.scene.addItem(item)
            self.update()
            self.endPos = event.pos()
            #self.scene.photo = 'aaa.jpg'


if __name__ == '__main__':
    run(MainWindow)