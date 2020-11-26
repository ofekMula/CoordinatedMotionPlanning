from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtOpenGL import QGLWidget, QGLFormat, QGL
from PyQt5.QtWidgets import (QApplication, QGraphicsView,
                             QGraphicsPixmapItem, QGraphicsScene, QGraphicsPolygonItem,
                             QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem, QOpenGLWidget)
from PyQt5.QtGui import QPainter, QPixmap, QPolygonF, QPen, QVector3D, QPalette, QFont
from PyQt5.QtCore import (QObject, QPointF, QPoint, QRectF,
                          QPropertyAnimation, pyqtProperty, QSequentialAnimationGroup,
                          QParallelAnimationGroup, QPauseAnimation, Qt)

from gui.RCircleSegment import RCircleSegment
from gui.RDiscRobot import RDiscRobot

from gui.RPolygon import RPolygon
from gui.RDisc import RDisc
from gui.RSegment import RSegment
from gui.RText import RText
import time


class MainWindowPlus(QtWidgets.QMainWindow):
    def __init__(self, gui):
        super().__init__()
        self.gui = gui

    # Adjust zoom level/scale on +/- key press
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Plus:
            self.gui.zoom /= 0.9
        if event.key() == QtCore.Qt.Key_Minus:
            self.gui.zoom *= 0.9
        self.gui.redraw()


class GUI(object):
    width = 1600
    height = 1000
    zoom = 50.0
    base_line_width = 3.5
    base_text_size = 2 * zoom
    animation_finished_action = lambda: None

    def __init__(self):
        MainWindow = MainWindowPlus(self)
        self.setupUi(MainWindow)

    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        self.sequence = QSequentialAnimationGroup()
        self.sequence.finished.connect(self.animation_finished)
        self.scene = QGraphicsScene()

        MainWindow.setObjectName("MainWindow")
        #todo: icon
        # icon = QtGui.QIcon()
        # icon.addFile('icon.png', QtCore.QSize(48, 48))
        # MainWindow.setWindowIcon(icon)
        MainWindow.resize(self.width, self.height)

        # qt designer generated code
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1118, 864)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 3, 1, 1, 1)
        self.gridLayout_0 = QtWidgets.QGridLayout()
        self.gridLayout_0.setObjectName("gridLayout_0")
        self.lineEdit_0 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_0.setObjectName("lineEdit_0")
        self.gridLayout_0.addWidget(self.lineEdit_0, 1, 0, 1, 1)
        self.pushButton_0 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_0.setObjectName("pushButton_0")
        self.gridLayout_0.addWidget(self.pushButton_0, 4, 0, 1, 1)
        self.toolButton_0 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_0.setObjectName("toolButton_0")
        self.gridLayout_0.addWidget(self.toolButton_0, 1, 1, 1, 1)
        self.pushButton_1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_1.setObjectName("pushButton_1")
        self.gridLayout_0.addWidget(self.pushButton_1, 6, 0, 1, 1)
        self.toolButton_1 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_1.setObjectName("toolButton_1")
        self.gridLayout_0.addWidget(self.toolButton_1, 3, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_0.addItem(spacerItem, 8, 0, 1, 1)
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setObjectName("label_1")
        self.gridLayout_0.addWidget(self.label_1, 2, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(300, 20, QtWidgets.QSizePolicy.MinimumExpanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_0.addItem(spacerItem1, 9, 0, 1, 1)
        self.label_0 = QtWidgets.QLabel(self.centralwidget)
        self.label_0.setObjectName("label_0")
        self.gridLayout_0.addWidget(self.label_0, 0, 0, 1, 1)
        self.lineEdit_1 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_1.setObjectName("lineEdit_1")
        self.gridLayout_0.addWidget(self.lineEdit_1, 3, 0, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout_0.addWidget(self.textEdit, 7, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_0, 3, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # end of eq designer generated code

        self.lineEdits = []
        self.lineEdits.append(self.lineEdit_0)
        self.lineEdits.append(self.lineEdit_1)
        self.pushButtons = []
        self.pushButtons.append(self.pushButton_0)
        self.pushButtons.append(self.pushButton_1)
        self.pushButtons.append(self.toolButton_0)
        self.pushButtons.append(self.toolButton_1)
        self.labels = []
        self.labels.append(self.label_0)
        self.labels.append(self.label_1)
        self.progressBars = []
        self.textEdits = []
        self.textEdits.append(self.textEdit)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.setSceneRect(0, 0, 0, 0)
        self.graphicsView.setRenderHints(QPainter.Antialiasing)
        # self.graphicsView.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        self.graphicsView.setViewport(QGLWidget(QGLFormat(QGL.SampleBuffers)))
        self.graphicsView.scale(self.zoom, -self.zoom)
        self.graphicsView.setDragMode(1)

    # Add a disc to the scene with radius r centered at (x, y) and return the object associated with it
    def add_disc(self, r, x, y, fill_color=QtCore.Qt.black, line_color=QtCore.Qt.black):
        d = RDisc(r, x, y, fill_color, line_color=line_color, line_width=self.base_line_width / self.zoom)
        self.scene.addItem(d.disc)
        return d

    # Add a disc robot to the scene with radius r centered at (x, y) and return the object associated with it
    def add_disc_robot(self, r, x, y, text="", fill_color=QtCore.Qt.black):
        d = RDiscRobot(r, x, y, fill_color, line_width=self.base_line_width / self.zoom, text=text)
        self.scene.addItem(d.disc)
        self.scene.addItem(d._text)
        return d

    # Add a polygon to the scene and return the object associated with it
    def add_polygon(self, points, line_color=QtCore.Qt.black, fill_color=QtCore.Qt.black):
        p = RPolygon(points, line_color, fill_color, line_width=self.base_line_width / self.zoom)
        self.scene.addItem(p.polygon)
        return p

    # Add a segment to the scene and return the object associated with it
    def add_segment(self, x1, y1, x2, y2, line_color=QtCore.Qt.black):
        s = RSegment(x1, y1, x2, y2, line_color, line_width=self.base_line_width / self.zoom)
        self.scene.addItem(s.line)
        return s

    # Add a circle segment to the scene and return the object associated with it
    def add_circle_segment(self, radius: float, center_x: float, center_y: float, start_angle: float, end_angle: float,
                           clockwise, fill_color=QtCore.Qt.transparent, line_color=QtCore.Qt.black):
        s = RCircleSegment(radius, center_x, center_y, start_angle, end_angle,
                           line_width=self.base_line_width / self.zoom, clockwise=clockwise,
                           fill_color=fill_color, line_color=line_color)
        self.scene.addItem(s.path)
        return s

    def add_text(self, text, x, y, size, color=QtCore.Qt.black):
        t = RText(text, x, y, size, color)
        self.scene.addItem(t.text)
        return t

    # Create a new linear translation animation for obj starting at ix, iy and ending at x, y
    def linear_translation_animation(self, obj, ix, iy, x, y, duration=1000):
        anim = QPropertyAnimation(obj, b'pos')
        anim.setDuration(duration)
        anim.setStartValue(QPointF(ix, iy))
        anim.setEndValue(QPointF(x, y))
        return anim

    # Create a general translation animation for obj. func is path from the unit interval I to R^2
    def translation_animation(self, obj, func, duration=1000):
        anim = QPropertyAnimation(obj, b'pos')
        anim.setDuration(duration)
        anim.setStartValue(QPointF(func(0)[0], func(0)[1]))
        anim.setEndValue(QPointF(func(1)[0], func(1)[1]))
        vals = [p / 100 for p in range(0, 101)]
        for i in vals:
            anim.setKeyValueAt(i, (QPointF(func(i)[0], func(i)[1])))
        return anim

    # Create an animation the changes the visibility of an object
    def visibility_animation(self, obj, visible):
        anim = QPropertyAnimation(obj, b'visible')
        anim.setDuration(0)
        if visible:
            anim.setEndValue(1)
        else:
            anim.setEndValue(0)
        return anim

    # Create an animation that does nothing
    def pause_animation(self, duration=1000):
        anim = QPauseAnimation(duration)
        return anim

    # Create an animation that changes the value of an object
    def value_animation(self, obj, v_begin, v_end, duration=1000):
        anim = QPropertyAnimation(obj, b'value')
        anim.setDuration(duration)
        anim.setStartValue(v_begin)
        anim.setEndValue(v_end)
        return anim

    # Create an animation that changes the text of an object
    def text_animation(self, obj, text: int):
        anim = QPropertyAnimation(obj, b'text')
        anim.setDuration(0)
        anim.setEndValue(text)
        return anim

    # Create an animation from a set of animations that will run in parallel
    def parallel_animation(self, *animations):
        group = QParallelAnimationGroup()
        for anim in animations:
            group.addAnimation(anim)
        return group

    # Add an animation to the animation queue
    def queue_animation(self, *animations):
        for anim in animations:
            self.sequence.addAnimation(anim)

    # Play (and empty) the animation queue
    def play_queue(self):
        self.sequence.start()

    # Empty the animation queue queue
    def empty_queue(self):
        self.sequence.clear()

    # Clear the scene of all objects
    def clear_scene(self):
        self.scene.clear()

    # Redraw the scene with updated parameters
    def redraw(self):
        line_width = self.base_line_width / self.zoom
        text_size = max(1, self.base_text_size / self.zoom)
        for item in self.graphicsView.items():
            if not isinstance(item, QGraphicsTextItem):
                pen = item.pen()
                pen.setWidthF(line_width)
                item.setPen(pen)
            else:
                item.setFont(QFont("Times", text_size))
        self.graphicsView.resetTransform()
        self.graphicsView.scale(self.zoom, -self.zoom)

    def animation_finished(self):
        self.empty_queue()
        print("Finished playing animation")
        self.animation_finished_action()

    def set_animation_finished_action(self, action):
        self.animation_finished_action = action

    # Set the i'th text of field in the GUI
    def set_field(self, i, s):
        self.lineEdits[i].setText(s)

    # Get the text of the i'th text field in the GUI
    def get_field(self, i):
        return self.lineEdits[i].text()

    # Set the text and color of the i'th label in the GUI
    def set_label(self, i, s, color=Qt.black):
        self.labels[i].setText(s)
        palette = self.labels[i].palette()
        palette.setColor(QPalette.WindowText, color)
        self.labels[i].setPalette(palette)

    # Set the function to be called when the i'th button in the GUI is pressed
    def set_logic(self, i, logic):
        try:
            self.pushButtons[i].clicked.disconnect()
        except Exception:
            pass
        self.pushButtons[i].clicked.connect(logic)

    # Set the i'th button text in the GUI
    def set_button_text(self, i, s):
        self.pushButtons[i].setText(s)

    # Set the value of the i'th progressBar
    def set_progressbar_value(self, i, n: int):
        self.progressBars[i].setValue(n)

    # Set the program's name
    def set_program_name(self, s):
        self.MainWindow.setWindowTitle(s)
