from pathlib import Path
from xinet import QtWidgets, QtCore, QtGui, RectItem, Signal
from xinet.image_utils import ImageLoader
from xinet.run_qt import run


Qt = QtCore.Qt
QColor = QtGui.QColor
QPoint = QtCore.QPoint
QRectF = QtCore.QRectF
QLabel = QtWidgets.QLabel
QIcon = QtGui.QIcon
QAction = QtWidgets.QAction
QFileDialog = QtWidgets.QFileDialog


class ImageScene(QtWidgets.QGraphicsScene):
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
        super().drawBackground(painter, rect)
        if self.photo.isNull():
            self.setBackgroundBrush(QColor(0, 0, 200, 100))  # 默认背景颜色
        else:
            # 设置场景的边界矩形，即可视化区域矩形
            _w = self.photo.width()
            _h = self.photo.height()
            self.setSceneRect(0, 0, _w, _h)
            #self.setBackgroundBrush(QColor(0, 0, 200, 30))  # 默认背景颜色
            painter.drawImage(0, 0, self.photo)


class ImageView(QtWidgets.QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 创建场景
        self.scene = ImageScene()
        self.init_Ui()
        self.lastPos = QPoint()
        self.endPos = QPoint()

    def init_Ui(self):
        # 设定视图的场景
        self.setScene(self.scene)
        self.fitInView(self.scene.sceneRect(), QtCore.Qt.KeepAspectRatio)
        self.setViewportUpdateMode(self.FullViewportUpdate)  # 消除重影 移动重影
        self.setDragMode(self.RubberBandDrag)  # 设置可以进行鼠标的拖拽选择
        # 这里是左上角方式显示
        self.setAlignment(QtCore.Qt.AlignLeft |
                          QtCore.Qt.AlignTop)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.lastPos = self. mapToScene(event.pos())
        self.endPos = self.lastPos

    def mouseMoveEvent(self, event):
        pt = event.pos()  # 获取鼠标坐标--view坐标
        self.endPos = self. mapToScene(pt)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        # 鼠标右键释放
        if event.button() == Qt.RightButton:
            x = self.lastPos.x()
            y = self.lastPos.y()
            w = self.endPos.x() - x
            h = self.endPos.y() - y
            rect = QRectF(x, y, w, h).normalized()  # 转换 w, h 为正数
            item = RectItem(rect)
            self.scene.addItem(item)
        super().mouseReleaseEvent(event)


class ImageToolMeta(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_Ui()
        self.loader = ImageLoader('')

    def init_Ui(self):
        self.statusBar()
        self.create_menubar()
        self.setWindowTitle('Image Tool')

    def create_quit_action(self):
        # 创建一个图标、一个 exit 的标签和一个快捷键组合，都执行了一个动作
        exitAct = QAction(QIcon('icons/quit.png'), '&Quit', self)
        exitAct.setShortcut('Ctrl+Q')
        # 创建了一个状态栏，当鼠标悬停在菜单栏的时候，能显示当前状态
        exitAct.setStatusTip('Exit application')
        # 当执行这个指定的动作时，就触发了一个事件。
        ## 这个事件跟 QApplication 的 quit() 行为相关联，所以这个动作就能终止这个应用。
        exitAct.triggered.connect(self.close)
        return exitAct

    def create_open_action(self):
        # 创建一个图标、一个 exit 的标签和一个快捷键组合，都执行了一个动作
        act = QAction(QIcon('icons/open.png'), '&Open', self)
        act.setShortcut('Ctrl+O')
        # 创建了一个状态栏，当鼠标悬停在菜单栏的时候，能显示当前状态
        act.setStatusTip('Open Image & Label file')
        # 当执行这个指定的动作时，就触发了一个事件。
        ## 这个事件跟 QApplication 的 quit() 行为相关联，所以这个动作就能终止这个应用。
        act.triggered.connect(self.open_image)
        return act

    def create_open_dir_action(self):
        # 创建一个图标、一个 exit 的标签和一个快捷键组合，都执行了一个动作
        act = QAction(QIcon('icons/open.png'), '&Open Dir', self)
        act.setShortcut('Ctrl+U')
        # 创建了一个状态栏，当鼠标悬停在菜单栏的时候，能显示当前状态
        act.setStatusTip('Open Dir')
        # 当执行这个指定的动作时，就触发了一个事件。
        ## 这个事件跟 QApplication 的 quit() 行为相关联，所以这个动作就能终止这个应用。
        act.triggered.connect(self.open_dir)
        return act

    def open_image(self):
        caption = "Open image or label file"
        dir_default = ""  # 默认打开目录
        filter_file = "*.jpg;;*.png;;*.json;;All Files(*)"
        name, _ = QFileDialog.getOpenFileName(self, caption, dir_default, filter_file)
        self.photo = Path(name)

    def open_dir(self):
        caption = "Open image or label file"
        dir_default = ""  # 默认打开目录
        name = QFileDialog.getExistingDirectory(self, caption, dir_default)
        self.loader = ImageLoader(name)
        self.photo = self.loader.current_path
        print(self.photo)

    def create_menubar(self):
        exitAct = self.create_quit_action()
        openAct = self.create_open_action()
        openDirAct = self.create_open_dir_action()
        # 创建菜单栏
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openAct)
        fileMenu.addAction(openDirAct)
        fileMenu.addAction(exitAct)


class MainWindow(ImageToolMeta):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设定窗口尺寸
        self.setGeometry(300, 300, 500, 500)
        self.view = ImageView()  # 创建视图窗口
        self.setCentralWidget(self.view)  # 设置中央控件

    def open_image(self):
        super().open_image()
        self.view.scene.photo = self.photo.as_posix()

    def open_dir(self):
        super().open_dir()
        self.view.scene.photo = self.photo.as_posix()


if __name__ == '__main__':
    run(MainWindow)
