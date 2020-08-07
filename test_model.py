from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtCharts import QtCharts
import tensorflow as tf
import numpy as np


class Canvas(QtWidgets.QWidget):
    DATA_SIZE = 28

    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = QtGui.QImage(Canvas.DATA_SIZE, Canvas.DATA_SIZE, QtGui.QImage.Format_Grayscale8)
        self.clear()
        self.model = tf.keras.models.load_model('model')

    def clear(self):
        self.image.fill(QtCore.Qt.lightGray)
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
        painter.drawImage(0, 0, self.image.scaled(self.width(), self.height()))
        painter.end()
        data = np.expand_dims(np.asarray(self.image.bits()) / 255.0, 0)
        result = np.argmax(self.model.predict(data)[0])
        print(result)

    def toCellCoordinates(self, point):
        return QtCore.QPoint(point.x() * Canvas.DATA_SIZE / self.width(), point.y() * Canvas.DATA_SIZE / self.height())

    def sizeHint(self):
        return QtCore.QSize(28, 28)

    def heightForWidth(self, width):
        return width


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.canvas = Canvas()
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        size_policy.setHeightForWidth(True)
        self.canvas.setSizePolicy(size_policy)
        label = QtWidgets.QLabel('Testi')

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(label)

        self.setLayout(layout)
        self.show()

        # probability = QtCharts.QBarSet('Probability')
        # probability.append([0.0, 0.1, 0.2])
        # series = QtCharts.QBarSeries()
        # series.append(probability)
        # chart = QtCharts.QChart()
        # chart.addSeries(series)
        # chart.setTitle('Probability')
        # self.chart_view = QtCharts.QChartView(chart)
        # self.chart_view.setGeometry(896, 0, 300, 300)
        # self.setMinimumSize(1280, 720)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.canvas.clear()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    app.exec_()
