from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtOpenGL import QGLWidget, QGLFormat, QGL
from PyQt5.QtWidgets import (QApplication, QGraphicsView,
                             QGraphicsPixmapItem, QGraphicsScene, QGraphicsPolygonItem,
                             QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem, QOpenGLWidget)
from PyQt5.QtGui import QPainter, QPixmap, QPolygonF, QPen, QFont, QTransform
from PyQt5.QtCore import (QObject, QPointF, QPoint, QRectF,
                          QPropertyAnimation, pyqtProperty, QSequentialAnimationGroup,
                          QParallelAnimationGroup, QPauseAnimation, Qt)


class RDiscRobot(QObject):
    def __init__(self, r: float, x: float, y: float, color, line_width: float, text=""):
        self._visible = 1
        self._radius = r
        self._pos = QPointF(x, y)
        super().__init__()
        # The supporting rectangle
        self.rect = QRectF(x - r, y - r, 2 * r, 2 * r)
        # The underlying QGraphicsEllipseItem
        self.disc = QGraphicsEllipseItem()
        self.disc.setRect(self.rect)
        self.disc.setBrush(QtGui.QBrush(color))
        # The underlying QGraphicsTextItem
        self._text: QGraphicsTextItem = QGraphicsTextItem(text)
        transform = QTransform.fromScale(0.3, -0.3)
        self._text.setTransformOriginPoint(self._pos)
        self._text.setTransform(transform)
        self._text.setPos(QPointF(x - 1.8, y + 1.8))
        font = QFont("Times", 2)
        self._text.setFont(font)
        pen = QPen()
        pen.setWidthF(line_width)
        self.disc.setPen(pen)
        self._visible = 1

    def x(self) -> float:
        return self._pos.x()

    def y(self) -> float:
        return self._pos.y()

    def set_text(self, text: str):
        self._text.setPlainText(text)

    # The following functions are for animation support

    @pyqtProperty(QPointF)
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self.rect = QRectF(value.x() - self._radius, value.y() - self._radius, 2 * self._radius, 2 * self._radius)
        self.disc.setRect(self.rect)
        self._text.setPos(QPointF(value.x() - 1.8, value.y() + 1.8))
        self._pos = value

    @pyqtProperty(int)
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        if value > 0:
            self.disc.show()
            self._text.show()
        else:
            self.disc.hide()
            self._text.hide()
        self._visible = value

    @pyqtProperty(int)
    def text(self):
        if self._text.toPlainText() == '':
            return 0
        return int(self._text.toPlainText())

    @text.setter
    def text(self, val: int):
        if val == 0:
            self._text.setPlainText('')
        else:
            self._text.setPlainText(str(val))
