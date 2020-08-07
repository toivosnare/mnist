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
        self.model = tf.keras.models.load_model('model')

    def clear(self):
        self.image.fill(QtCore.Qt.white)
        self.update()

    def mousePressEvent(self, event):
        self.last_point = self.toCellCoordinates(event.pos())
        self.paintCell(self.last_point, 5, 0.5)

    def mouseMoveEvent(self, event):
        new_point = self.toCellCoordinates(event.pos())
        if self.last_point and not new_point == self.last_point:
            self.paintCell(new_point, 5, 0.5)
            self.last_point = new_point

    def mouseReleaseEvent(self, event):
        self.last_point = None

    def paintCell(self, point, radius, strength):
        painter = QtGui.QPainter(self.image)
        painter.setPen(QtCore.Qt.NoPen)
        gradient = QtGui.QRadialGradient(point, radius)
        gradient.setColorAt(0, QtGui.QColor(0, 0, 0, 255))
        gradient.setColorAt(strength, QtGui.QColor(0, 0, 0, 0))
        gradient.setColorAt(0.9, QtGui.QColor(0, 0, 0, 0))
        brush = QtGui.QBrush(gradient)
        painter.setBrush(brush)
        painter.drawEllipse(point, radius / 2, radius / 2)
        painter.end()
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image.scaled(Canvas.WINDOW_SIZE, Canvas.WINDOW_SIZE))
        data = np.expand_dims(np.asarray(self.image.bits()) / 255.0, 0)
        result = np.argmax(self.model.predict(data)[0])
        print(result)

    def toCellCoordinates(self, point):
        return point * Canvas.DATA_SIZE / Canvas.WINDOW_SIZE


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
