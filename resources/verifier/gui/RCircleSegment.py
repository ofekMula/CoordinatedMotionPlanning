from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtOpenGL import QGLWidget, QGLFormat, QGL
from PyQt5.QtWidgets import (QApplication, QGraphicsView,
                             QGraphicsPixmapItem, QGraphicsScene, QGraphicsPolygonItem,
                             QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsPathItem, QOpenGLWidget)
from PyQt5.QtGui import QPainter, QPixmap, QPolygonF, QPen, QPainterPath
from PyQt5.QtCore import (QObject, QPointF, QPoint, QRectF,
                          QPropertyAnimation, pyqtProperty, QSequentialAnimationGroup,
                          QParallelAnimationGroup, QPauseAnimation, Qt)
import math


class RCircleSegment(QObject):
    def __init__(self,radius: float, center_x: float, center_y: float, start_angle: float, end_angle: float, clockwise, line_width: float, line_color = Qt.black, fill_color=Qt.transparent):
        super().__init__()
        # The supporting rectangle
        if end_angle < start_angle:
            end_angle += 2*math.pi
        start_angle = -start_angle
        end_angle = -end_angle
        shift = end_angle-start_angle
        if clockwise:
           shift = -shift-2*math.pi
        x, y = center_x - radius, center_y - radius
        self.rect = QRectF(x, y, 2 * radius, 2 * radius)
        # The underlying QGraphicsPathItem
        self.painter_path = QPainterPath(QPointF(center_x+math.cos(start_angle)*radius, center_y-math.sin(start_angle)*radius))
        self.painter_path.arcTo(self.rect, math.degrees(start_angle), math.degrees(shift))
        self.path = QGraphicsPathItem(self.painter_path)
        self.path.setBrush(QtGui.QBrush(fill_color))
        pen = QPen()
        pen.setWidthF(line_width)
        pen.setColor(line_color)
        self.path.setPen(pen)
        self._visible = 1

    # def x(self):
    #     return self._pos.x()
    #
    # def y(self):
    #     return self._pos.y()
    #
    # # The following functions are for animation support
    #
    # @pyqtProperty(QPointF)
    # def pos(self):
    #     return self._pos
    #
    # @pos.setter
    # def pos(self, value):
    #     self.rect = QRectF(value.x() - self._radius, value.y() - self._radius, 2 * self._radius, 2 * self._radius)
    #     self.path.setRect(self.rect)
    #     self._pos = value
    #
    @pyqtProperty(int)
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        if (value > 0):
            self.path.show()
        else:
            self.path.hide()
        self._visible = value