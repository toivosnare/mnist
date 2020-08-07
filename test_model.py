import sys
from PySide2 import QtGui, QtCore, QtWidgets
import tensorflow as tf
import numpy as np


class Canvas(QtWidgets.QWidget):
    WINDOW_SIZE = 896
    DATA_SIZE = 28

    def __init__(self, parent):
        super().__init__(parent)
        self.image = QtGui.QImage(Canvas.DATA_SIZE, Canvas.DATA_SIZE, QtGui.QImage.Format_Grayscale8)
        self.clear()
        self.last_point = None
        self.model = tf.keras.models.load_model('model')

    # def draw_opaque_line(self, p0, p1, width):
    #     painter = QtGui.QPainter(self.image)
    #     d = p1 - p0
    #     n = (QtGui.QVector2D(d.y(), -d.x()).normalized() * width).toPoint()
    #     gradient = QtGui.QLinearGradient(p0 + n, p0 - n)
    #     gradient.setColorAt(0, QtGui.QColor.fromHsv(0, 0, 255, 0))
    #     gradient.setColorAt(0.35, QtGui.QColor.fromHsv(0, 0, 255, 0))
    #     gradient.setColorAt(0.5, QtGui.QColor.fromHsv(0, 0, 0, 20))
    #     gradient.setColorAt(0.65, QtGui.QColor.fromHsv(0, 0, 255, 0))
    #     gradient.setColorAt(1, QtGui.QColor.fromHsv(0, 0, 255, 0))
    #     brush = QtGui.QBrush(gradient)
    #     painter.setBrush(brush)
    #     pen = QtGui.QPen(brush, width)
    #     pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
    #     painter.setPen(pen)
    #     painter.drawLine(p0, p1)
    #     self.update()

    def clear(self):
        self.image.fill(QtCore.Qt.white)
        self.update()

    def draw_line(self, p0, p1, width):
        painter = QtGui.QPainter(self.image)
        pen = QtGui.QPen()
        pen.setWidth(width)
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.drawLine(p0, p1)
        self.update()

    def mouseMoveEvent(self, event):
        new_point = event.pos() * Canvas.DATA_SIZE / Canvas.WINDOW_SIZE
        if self.last_point:
            self.draw_line(self.last_point, new_point, 1)
        self.last_point = new_point

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image.scaled(Canvas.WINDOW_SIZE, Canvas.WINDOW_SIZE))
        data = np.expand_dims(np.asarray(self.image.bits()) / 255.0, 0)
        result = np.argmax(self.model.predict(data)[0])
        print(result)

    def mouseReleaseEvent(self, event):
        self.last_point = None


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(Canvas.WINDOW_SIZE, Canvas.WINDOW_SIZE)
        self.canvas = Canvas(self)
        self.canvas.setGeometry(0, 0, Canvas.WINDOW_SIZE, Canvas.WINDOW_SIZE)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.canvas.clear()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
