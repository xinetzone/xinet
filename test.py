from xinet import QtWidgets, QtCore, RectItem
from xinet.run_qt import run


class MainWindow(QtWidgets.QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设定视图尺寸
        self.resize(600, 600)
        # 创建场景
        self.scene = QtWidgets.QGraphicsScene()
        self.setSceneRect(0, 0, 600, 600)  # 设置场景的边界矩形，即可视化区域矩形
        # x1, y1, w, h
        self.item = RectItem(20, 25, 120, 120) # 可塑性矩形
        self.scene.addItem(self.item)
        self.scene.addItem(RectItem(200, 250, 120, 120))
        # 设定视图的场景
        self.setScene(self.scene)
        self.fitInView(self.scene.sceneRect(), QtCore.Qt.KeepAspectRatio)


if __name__ == '__main__':
    run(MainWindow)