import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QFrame,
    QPushButton,
    QFileDialog,
    QHBoxLayout
)
from PyQt5.QtCore import Qt, QTimer, QPoint, QSize
from PyQt5.QtGui import QIcon

from Capturer_Rectangle import Capture_Rectangle
from Capture_Polygon import Capture_Polygon



class ScreenRegionSelector(QMainWindow):
    
    def __init__(self,):
        super().__init__(None)
        self.setWindowFlags(Qt.FramelessWindowHint)  # Fenster rahmenlos machen
        self.setWindowTitle("")
        
        # self.m_width = 400
        # self.m_height = 500

        frame = QFrame()
        frame.setContentsMargins(0, 0, 0, 0)
        lay = QVBoxLayout(frame)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.setContentsMargins(1, 1, 1, 1)

        # Layout für die Schaltflächen erstellen
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        button_layout.setContentsMargins(1, 1, 1, 1)

        self.label = QLabel()
        self.btn_capture_rectangle = QPushButton()
        self.btn_capture_rectangle.setIcon(QIcon("./images/rectangle.svg"))
        self.btn_capture_rectangle.setIconSize(QSize(100, 100))  # Icon-Größe auf 100x100 setzen
        self.btn_capture_rectangle.setFixedSize(100,100)
        self.btn_capture_rectangle.clicked.connect(self.capture_rectangle)

        self.label = QLabel()
        self.btn_capture_polygon = QPushButton()
        self.btn_capture_polygon.setIcon(QIcon("./images/polygon.svg"))
        self.btn_capture_polygon.setIconSize(QSize(100, 100))  # Icon-Größe auf 100x100 setzen
        self.btn_capture_polygon.setFixedSize(100,100)
        self.btn_capture_polygon.clicked.connect(self.capture_polygon)
        
        self.btn_save = QPushButton()
        self.btn_save.setIcon(QIcon("./images/save.svg"))
        self.btn_save.setIconSize(QSize(100, 100))  # Icon-Größe auf 30x30 setzen
        self.btn_save.setFixedSize(100, 100)
        self.btn_save.clicked.connect(self.save)
        self.btn_save.setVisible(False)

        # Schaltflächen zum Button-Layout hinzufügen
        button_layout.addWidget(self.label)
        button_layout.addWidget(self.btn_capture_rectangle)
        button_layout.addWidget(self.btn_capture_polygon)
        button_layout.addWidget(self.btn_save)

        # Header-Layout erstellen
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Links ausrichten

        # Icon auf der linken Seite des Headers
        self.header_icon = QLabel()
        self.header_icon.setPixmap(QIcon("./images/logo.png").pixmap(30, 30))
        self.header_icon.setFixedSize(30, 30)
        self.header_icon.mousePressEvent = self.mousePressEvent
        self.header_icon.mouseMoveEvent = self.moveWindow

        # Text neben dem Logo
        self.header_text = QLabel("Schnipping Tool")
        self.header_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header_text.setStyleSheet("color: white;")  # Textfarbe auf weiß setzen
        self.header_text.mousePressEvent = self.mousePressEvent
        self.header_text.mouseMoveEvent = self.moveWindow

        # Drag-Schaltfläche mit Icon
        self.btn_drag = QPushButton()
        self.btn_drag.setIcon(QIcon("./images/move.svg"))
        self.btn_drag.setFixedSize(30, 30)
        self.btn_drag.setMouseTracking(True)
        self.btn_drag.setStyleSheet("background-color: #ec7c25;")  # Hintergrundfarbe auf gelb setzen
        self.btn_drag.mousePressEvent = self.mousePressEvent
        self.btn_drag.mouseMoveEvent = self.moveWindow

        # Schließen-Schaltfläche mit Icon
        self.btn_close = QPushButton()
        self.btn_close.setIcon(QIcon("./images/close.svg"))
        self.btn_close.setFixedSize(30, 30)
        self.btn_close.setStyleSheet("background-color: red;")  # Hintergrundfarbe auf rot setzen
        self.btn_close.clicked.connect(self.close)

        # Schaltflächen zum Header-Layout hinzufügen
        header_layout.addWidget(self.header_icon)  # Icon hinzufügen
        header_layout.addWidget(self.header_text)  # Text hinzufügen
        header_layout.addStretch()  # Platzhalter hinzufügen, um die restlichen Widgets nach rechts zu schieben
        header_layout.addWidget(self.btn_drag)
        header_layout.addWidget(self.btn_close)

        # Header-Layout zum Hauptlayout hinzufügen
        lay.addLayout(header_layout)

        # Setze das zentrale Widget zwischen Header und Button-Layout
        self.setCentralWidget(frame)

        # Button-Layout zum Hauptlayout hinzufügen
        lay.addLayout(button_layout)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clickPosition = event.globalPos()
            event.accept()

    def moveWindow(self, e):
        if not self.isMaximized():
            if e.buttons() == Qt.LeftButton:
                self.move(self.pos() + e.globalPos() - self.clickPosition)
                self.clickPosition = e.globalPos()
                e.accept()

    def capture_rectangle(self):
        self.capturer_rectangle = Capture_Rectangle(self)
        self.capturer_rectangle.show()
        self.btn_save.setVisible(True)
        self.adjustSize()  # Größe des Fensters anpassen

    def capture_polygon(self):
        self.capturer_polygon = Capture_Polygon(self)

        self.capturer_polygon.show()
        self.adjustSize()
          # Gröe des Fensters anpassen
        self.btn_save.setVisible(True) # Verbindung zum Signal

    def save(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Image files (*.png *.jpg *.bmp)")
        if file_name:
            if hasattr(self, 'capturer_rectangle') and self.capturer_rectangle.isVisible():
                self.capturer_rectangle.imgmap.save(file_name)
            elif hasattr(self, 'capturer_polygon') and self.capturer_polygon.isVisible():
                self.capturer_polygon.imgmap.save(file_name)

  

if __name__ == "__main__":
    app = QApplication(sys.argv)    
    app.setStyleSheet("""
    QFrame {
        background-color: #3f3f3f;
    }
                      
    QPushButton {
        border-radius: 1px;
        background-color: rgb(60, 90, 255);
        padding: 0px;
        color: white;
        font-weight: bold;
        font-family: Arial;
        font-size: 12px;
    }
                      
    QPushButton::hover {
        background-color: rgb(60, 20, 255)
    }
    """)

    selector = ScreenRegionSelector()
    selector.show()
    app.exit(app.exec_())
