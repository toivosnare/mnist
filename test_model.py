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
        self.image.fill(QtCore.Qt.black)
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
        gradient.setColorAt(0, QtGui.QColor(255, 255, 255, 255))
        gradient.setColorAt(strength, QtGui.QColor(255, 255, 255, 0))
        gradient.setColorAt(0.9, QtGui.QColor(255, 255, 255, 0))
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
        for digit, probability in enumerate(self.model.predict(data)[0]):
            self.parentWidget().probabilities.insert(digit, probability)

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

        self.probabilities = QtCharts.QBarSet('Probability')
        self.probabilities.append([0.1 for _ in range(10)])
        series = QtCharts.QBarSeries()
        series.append(self.probabilities)
        chart = QtCharts.QChart()
        chart.addSeries(series)
        chart_view = QtCharts.QChartView(chart)
        chart_view.setSizePolicy(size_policy)

        x_axis = QtCharts.QBarCategoryAxis()
        x_axis.setCategories([str(i) for i in range(10)])
        chart.addAxis(x_axis, QtCore.Qt.AlignBottom)
        series.attachAxis(x_axis)

        y_axis = QtCharts.QValueAxis()
        y_axis.setRange(0.0, 1.0)
        y_axis.setTickCount(11)
        chart.addAxis(y_axis, QtCore.Qt.AlignLeft)
        series.attachAxis(y_axis)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(chart_view)

        self.setLayout(layout)
        self.show()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.canvas.clear()

    def sizeHint(self):
        return QtCore.QSize(1280, 720)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    app.exec_()
