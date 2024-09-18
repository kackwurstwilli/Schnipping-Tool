from PyQt5.QtWidgets import QWidget, QApplication, QRubberBand
from PyQt5.QtGui import QMouseEvent, QPainter, QPolygon, QPixmap
from PyQt5.QtCore import Qt, QPoint, QRect
import time

class Capture_Polygon(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main = main_window
        self.main.hide()
        
        self.setMouseTracking(True)
        desk_size = QApplication.desktop()
        self.setGeometry(0, 0, desk_size.width(), desk_size.height())
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowOpacity(0.30)

        self.points = []
        self.polygon = QPolygon(self.points)  # Initialisiere das Polygon mit den Punkten

        QApplication.setOverrideCursor(Qt.CrossCursor)
        screen = QApplication.primaryScreen()
        rect = QApplication.desktop().rect()

        time.sleep(0.31)
        self.imgmap = screen.grabWindow(
            QApplication.desktop().winId(),
            rect.x(), rect.y(), rect.width(), rect.height()
        )

    def mousePressEvent(self, event: QMouseEvent | None) -> None:
        if event.button() == Qt.LeftButton:
            self.points.append(event.pos())
            self.polygon = QPolygon(self.points)
            self.update()

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Escape, Qt.Key_Return, Qt.Key_Enter):
            self.capturePolygon()
            QApplication.restoreOverrideCursor()
            self.main.show()
            self.close()

    def mouseDoubleClickEvent(self, event: QMouseEvent | None) -> None:
        if event.button() == Qt.LeftButton:
            self.capturePolygon()
            QApplication.restoreOverrideCursor()
            self.main.show()
            self.close()

    def mouseMoveEvent(self, event: QMouseEvent | None) -> None:
        self.current_pos = event.pos()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.red)
        pen = painter.pen()
        pen.setWidth(5)  # Setze die Linienbreite auf 5
        painter.setPen(pen)
        if not self.polygon.isEmpty():
            painter.drawPolygon(self.polygon)
            if hasattr(self, 'current_pos'):
                painter.drawLine(self.points[-1], self.current_pos)

    def capturePolygon(self):
        # Erstelle eine Maske basierend auf dem Polygon
        mask = self.imgmap.createMaskFromColor(Qt.transparent)
        mask.fill(Qt.white)
        painter = QPainter(mask)
        painter.setBrush(Qt.black)
        painter.setPen(Qt.black)
        painter.drawPolygon(self.polygon)
        painter.end()

        # Wende die Maske auf das Bild an
        self.imgmap.setMask(mask)

        # Zuschneiden des Bildes auf das Begrenzungsrechteck des Polygons
        bounding_rect = self.polygon.boundingRect()
        cropped_img = self.imgmap.copy(bounding_rect.intersected(self.imgmap.rect()))

        # Setze das zugeschnittene Bild in die Zwischenablage mit weißem Hintergrund
        white_background = QPixmap(cropped_img.size())
        white_background.fill(Qt.white)
        painter = QPainter(white_background)
        painter.drawPixmap(0, 0, cropped_img)
        painter.end()

        clipboard = QApplication.clipboard()
        clipboard.setPixmap(white_background)

        # Speichere das zugeschnittene Bild
        self.imgmap = cropped_img
        self.main.label.setPixmap(cropped_img)