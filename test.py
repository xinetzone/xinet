from pathlib import Path

from xinet import QtWidgets, QtCore, QtGui, RectItem, Signal
from xinet.run_qt import run


QIcon = QtGui.QIcon
QAction = QtWidgets.QAction
QFileDialog = QtWidgets.QFileDialog


class ImageToolMeta(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_Ui()

    def init_Ui(self):
        self.statusBar()
        self.create_menubar()
        self.setGeometry(300, 300, 300, 200)
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

    def open_image(self):
        caption = "Open image or label file"
        dir_default = ""  # 默认打开目录
        filter_file = "*.jpg;;*.png;;*.json;;All Files(*)"
        name, imgType = QFileDialog.getOpenFileName(self, caption, dir_default, filter_file)
        self.photo = Path(name)
        print(name, imgType)

    def create_menubar(self):
        exitAct = self.create_quit_action()
        openAct = self.create_open_action()
        # 创建菜单栏
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openAct)
        fileMenu.addAction(exitAct)


if __name__ == '__main__':
    run(ImageToolMeta)
