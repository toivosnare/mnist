import sys
from PySide2 import QtGui, QtCore, QtWidgets


class Canvas(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.image = QtGui.QImage(500, 500, QtGui.QImage.Format_Grayscale8)
        self.image.fill(QtCore.Qt.white)
        self.last_point = None

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

    def draw_line(self, p0, p1, width):
        painter = QtGui.QPainter(self.image)
        pen = QtGui.QPen()
        pen.setWidth(width)
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.drawLine(p0, p1)
        self.update()

    def mouseMoveEvent(self, event):
        if self.last_point == None:
            self.last_point = event.pos()
            return
        self.draw_line(self.last_point, event.pos(), 30)
        self.last_point = event.pos()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        n = 28
        for index, value in enumerate(self.image.scaled(n, n).bits()):
            print(value, end=' ')
            if not index % n:
                print()

    def mouseReleaseEvent(self, event):
        self.last_point = None


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(500, 500)
        self.canvas = Canvas(self)
        self.canvas.setGeometry(0, 0, 500, 500)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()