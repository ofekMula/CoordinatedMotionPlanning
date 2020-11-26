from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtOpenGL import QGLWidget, QGLFormat, QGL
from PyQt5.QtWidgets import (QApplication, QGraphicsView,
                             QGraphicsPixmapItem, QGraphicsScene, QGraphicsPolygonItem,
                             QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem, QOpenGLWidget)
from PyQt5.QtGui import QPainter, QPixmap, QPolygonF, QPen, QFont, QTransform
from PyQt5.QtCore import (QObject, QPointF, QPoint, QRectF,
                          QPropertyAnimation, pyqtProperty, QSequentialAnimationGroup,
                          QParallelAnimationGroup, QPauseAnimation, Qt)


class RText(QObject):
    def __init__(self, text, x, y, size, color):
        self._pos = QPointF(x - 1.8, y + 1.8)
        super().__init__()
        self.text = QGraphicsTextItem(text)
        transform = QTransform.fromScale(0.3, -0.3)
        self.text.setTransformOriginPoint(self._pos)
        self.text.setTransform(transform)
        self.text.setPos(self._pos)
        # self.text.setRotation(-180)
        font = QFont("Times", 2)
        self.text.setFont(font)

        self._visible = 1

    @pyqtProperty(int)
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        if value > 0:
            self.text.show()
        else:
            self.text.hide()
        self._visible = value

