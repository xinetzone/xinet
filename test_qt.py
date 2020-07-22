from xinet.Qt.qt5 import QtCore, QtGui, QtWidgets
from xinet.run_qt import run


class StockDialog(QtWidgets.QWidget):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.setWindowTitle("绘制图形")
        self.pen = QtGui.QPen(QtGui.QColor('blue'))

        self.label_column = self.create_label_column()
        self.init_Ui()
        # 信号和槽函数
        self.shapeComboBox.activated.connect(self.slotShape)
        self.widthSpinBox.valueChanged.connect(self.slotPenWidth)
        self.penStyleComboBox.activated.connect(self.slotPenStyle)
        # 
        self.penColorPushButton.clicked.connect(self.slotPenColor)
        
        self.penCapComboBox.activated.connect(self.slotPenCap)
        self.penJoinComboBox.activated.connect(self.slotPenJoin)
        self.brushStyleComboBox.activated.connect(self.slotBrush)
        self.brushColorPushButton.clicked.connect(self.slotBrushColor)

        self.slotShape(self.shapeComboBox.currentIndex())
        self.slotPenWidth(self.widthSpinBox.value())
        self.slotBrush(self.brushStyleComboBox.currentIndex())

    def init_Ui(self):
        mainSplitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        # 设置分割窗的分割条在拖动时实时更新显示
        mainSplitter.setOpaqueResize(True)

        frame = QtWidgets.QFrame(mainSplitter)
        mainLayout = QtWidgets.QGridLayout(frame)
        mainLayout.setSpacing(6)
        # 形状选择器
        shapes = ["Line", "Rectangle", 'Rounded Rectangle',
                  'Ellipse', 'Pie', 'Chord', 'Path', 'Polygon',
                  'Polyline', 'Arc', 'Points', 'Text', 'Pixmap']
        self.shapeComboBox = QtWidgets.QComboBox()
        self.shapeComboBox.addItems(shapes)
        # 画笔线宽选择器
        self.widthSpinBox = QtWidgets.QSpinBox()
        self.widthSpinBox.setRange(0, 20)
        # 画笔颜色选择器
        self.penColorFrame = QtWidgets.QFrame()
        self.penColorFrame.setAutoFillBackground(True)
        self.penColorFrame.setPalette(QtGui.QPalette(QtGui.QColor('blue')))
        self.penColorPushButton = QtWidgets.QPushButton("更改")
        # 画笔风格选择器
        self.penStyleComboBox = QtWidgets.QComboBox()
        pen_styles = ['Solid', 'Dash', 'Dot',
                      'Dash Dot', 'Dash Dot Dot', 'None']
        self.penStyleComboBox.addItems(pen_styles)
        # 画笔笔帽选择器
        self.penCapComboBox = QtWidgets.QComboBox()
        self.penCapComboBox.addItems(["Flat", "Square", "Round"])
        # 画笔连接点选择器
        self.penJoinComboBox = QtWidgets.QComboBox()
        self.penJoinComboBox.addItems(["Miter", "Bebel", "Round'"])
        # 画刷风格选择器
        self.brushStyleComboBox = QtWidgets.QComboBox()
        brush_styles = [
            'Linear Gradient', 'Radial Gradient', 'Texture', 'Solid', 'Horizontal',
            'Vertical', 'Cross', 'Backward Diagonal', 'Forward Diagonal', 'Diagonal Cross',
            'Dense 1', 'Dense 2', 'Dense 3', 'Dense 4', 'Dense 5', 'Dense 6', 'Dense 7',
            'None']
        self.brushStyleComboBox.addItems(brush_styles)
        # 画刷颜色选择器
        self.brushColorFrame = QtWidgets.QFrame()
        self.brushColorFrame.setAutoFillBackground(True)
        self.brushColorFrame.setPalette(QtGui.QPalette(QtGui.QColor('green')))
        self.brushColorPushButton = QtWidgets.QPushButton("更改")
        # 建立布局管理器
        self.create_layout(mainLayout, mainSplitter)

    def create_layout(self, mainLayout, mainSplitter):
        contents = [self.shapeComboBox, self.widthSpinBox,
                    self.penColorFrame, self.penStyleComboBox,
                    self.penCapComboBox, self.penJoinComboBox,
                    self.brushStyleComboBox, self.brushColorFrame]

        #建立布局
        for k, (name, value) in enumerate(zip(self.label_column, contents)):
            mainLayout.addWidget(self.label_column[k], k, 0)
            mainLayout.addWidget(value, k, 1)
            if k == 2:
                mainLayout.addWidget(self.penColorPushButton, k, 3)
            elif k == 7:
                mainLayout.addWidget(self.brushColorPushButton, k, 3)

        mainSplitter1 = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        mainSplitter1.setOpaqueResize(True)

        stack1 = QtWidgets.QStackedWidget()
        stack1.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Raised)
        self.area = PaintArea()
        stack1.addWidget(self.area)
        frame1 = QtWidgets.QFrame(mainSplitter1)
        mainLayout1 = QtWidgets.QVBoxLayout(frame1)
        #mainLayout1.setMargin(10)
        mainLayout1.setSpacing(6)
        mainLayout1.addWidget(stack1)

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(mainSplitter1, 0, 0)
        layout.addWidget(mainSplitter, 0, 1)
        self.setLayout(layout)

    def create_label_column(self):
        contents = ["形状：", "画笔线宽：", "画笔颜色：", "画笔风格：",
                    "画笔顶端：", "画笔连接点：", "画刷风格：", "画刷颜色："]
        return [QtWidgets.QLabel(content) for content in contents]

    def slotShape(self, value):
        shape = self.area.shapes[value]
        self.area.setShape(shape)

    def slotPenWidth(self, value):
        self.pen.setWidth(value)
        self.area.setPen(self.pen)

    def slotPenStyle(self, value):
        penStyle_dict = {
            'Solid': QtCore.Qt.SolidLine,
            'Dash':  QtCore.Qt.DashLine,
            'Dot':  QtCore.Qt.DotLine,
            'Dash Dot':  QtCore.Qt.DashDotLine,
            'Dash Dot Dot':  QtCore.Qt.DashDotDotLine,
            'None':  QtCore.Qt.NoPen
        }
        value = self.penStyleComboBox.currentText()
        self.pen.setStyle(penStyle_dict[value])
        self.area.setPen(self.pen)

    def slotPenCap(self, value):
        penCap_dict = {
            'Flat': QtCore.Qt.FlatCap,
            'Square':  QtCore.Qt.SquareCap,
            'Round':  QtCore.Qt.RoundCap,
        }
        value = self.penCapComboBox.currentText()
        self.pen.setCapStyle(penCap_dict[value])
        self.area.setPen(self.pen)

    def slotPenJoin(self, value):
        self.slotPenWidth(value)

    def slotPenColor(self):
        color = QtWidgets.QColorDialog.getColor(QtCore.Qt.blue)
        self.penColorFrame.setPalette(QtGui.QPalette(color))
        self.area.setPen(QtGui.QPen(color))

    def slotBrushColor(self):
        color = QtWidgets.QColorDialog.getColor(QtCore.Qt.blue)
        self.brushColorFrame.setPalette(QtGui.QPalette(color))
        self.slotBrush(self.brushStyleComboBox.currentIndex())

    def slotBrush(self, value):
        pass

class PaintArea(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.shapes = ["Line", "Rectangle", 'Rounded Rectangle',
                       'Ellipse', 'Pie', 'Chord', 'Path', 'Polygon',
                       'Polyline', 'Arc', 'Points', 'Text', 'Pixmap']
        self.setPalette(QtGui.QPalette(QtCore.Qt.white))
        self.setAutoFillBackground(True)
        self.setMinimumSize(400, 400)
        self.pen = QtGui.QPen()
        self.brush = QtGui.QBrush()
        self.shape = 'Line'

    def setShape(self, s):
        self.shape = s
        self.update()

    def setPen(self, p):
        self.pen = p
        self.update()

    def setBrush(self, b):
        self.brush = b
        self.update()

    def paintEvent(self, QPaintEvent):
        p = QtGui.QPainter(self)
        p.setPen(self.pen)
        p.setBrush(self.brush)

        rect = QtCore.QRect(50, 100, 300, 200)
        points = [QtCore.QPoint(150, 100), QtCore.QPoint(300, 150),
                  QtCore.QPoint(350, 250), QtCore.QPoint(100, 300)]
        startAngle = 30 * 16
        spanAngle = 120 * 16

        path = QtGui.QPainterPath()
        path.addRect(150, 150, 100, 100)
        path.moveTo(100, 100)
        path.cubicTo(300, 100, 200, 200, 300, 300)
        path.cubicTo(100, 300, 200, 200, 100, 100)

        if self.shape == "Line":
            p.drawLine(rect.topLeft(), rect.bottomRight())
        elif self.shape == "Rectangle":
            p.drawRect(rect)
        elif self.shape == 'Rounded Rectangle':
            p.drawRoundedRect(rect, 25, 25, QtCore.Qt.RelativeSize)
        elif self.shape == "Ellipse":
            p.drawEllipse(rect)
        elif self.shape == "Polygon":
            p.drawPolygon(QtGui.QPolygon(points), QtCore.Qt.WindingFill)
        elif self.shape == "Polyline":
            p.drawPolyline(QtGui.QPolygon(points))
        elif self.shape == "Points":
            p.drawPoints(QtGui.QPolygon(points))
        elif self.shape == "Pie":
            p.drawPie(rect, startAngle, spanAngle)
        elif self.shape == "Arc":
            p.drawArc(rect, startAngle, spanAngle)
        elif self.shape == "Chord":
            p.drawChord(rect, startAngle, spanAngle)
        elif self.shape == "Path":
            p.drawPath(path)
        elif self.shape == "Text":
            p.drawText(rect, QtCore.Qt.AlignCenter, "Hello Qt!")
        elif self.shape == "Pixmap":
            p.drawPixmap(150, 150, QtGui.QPixmap("images/qt-logo.png"))


if __name__ == '__main__':
    run(StockDialog)
