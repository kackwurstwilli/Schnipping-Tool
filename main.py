import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QFrame,
    QHBoxLayout,
    QStackedLayout,
    QPushButton,
    QFileDialog,
    QToolBar,
    QWidget,
    QSizePolicy
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

        # Layout für die Schaltflächen erstellen\
        box_and_button_layout = QVBoxLayout()
        box_and_button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        box_and_button_layout.setContentsMargins(1, 1, 1, 1)
        
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_layout.setContentsMargins(1, 1, 1, 1)

        self.label = QLabel()
        self.btn_capture_rectangle = QPushButton()
        self.btn_capture_rectangle.setIcon(QIcon("./images/rectangle.svg"))
        self.btn_capture_rectangle.setIconSize(QSize(100, 100))  # Icon-Größe auf 100x100 setzen
        self.btn_capture_rectangle.setFixedSize(100,100)
        self.btn_capture_rectangle.clicked.connect(self.capture_rectangle)

        self.btn_capture_polygon = QPushButton()
        self.btn_capture_polygon.setIcon(QIcon("./images/polygon.svg"))
        self.btn_capture_polygon.setIconSize(QSize(100, 100))  # Icon-Größe auf 100x100 setzen
        self.btn_capture_polygon.setFixedSize(100,100)
        self.btn_capture_polygon.clicked.connect(self.capture_polygon)
        
        self.btn_sized_box = QPushButton()
        self.btn_sized_box.setFixedSize(100, 200)
        self.btn_sized_box.setStyleSheet("background-color: #5d5d5d;")
        self.btn_sized_box.setVisible(False)# Grauer Hintergrund

        
        
        self.btn_save_rectangle = QPushButton()
        self.btn_save_rectangle.setIcon(QIcon("./images/save.svg"))
        self.btn_save_rectangle.setIconSize(QSize(100, 100))  # Icon-Größe auf 30x30 setzen
        self.btn_save_rectangle.setFixedSize(100, 100)
        self.btn_save_rectangle.clicked.connect(self.save_recangle)
        self.btn_save_rectangle.setVisible(False)
        
        self.btn_save_polygon = QPushButton()
        self.btn_save_polygon.setIcon(QIcon("./images/save.svg"))
        self.btn_save_polygon.setIconSize(QSize(100, 100))  # Icon-Größe auf 30x30 setzen
        self.btn_save_polygon.setFixedSize(100, 100)
        self.btn_save_polygon.clicked.connect(self.save_polygon)
        self.btn_save_polygon.setVisible(False)
        # Schaltflächen zum Button-Layout hinzufügen
        button_layout.addWidget(self.btn_capture_rectangle)
        button_layout.addWidget(self.btn_capture_polygon)
        button_layout.addWidget(self.btn_sized_box)
        button_layout.addWidget(self.btn_save_rectangle)
        button_layout.addWidget(self.btn_save_polygon)
        
        box_and_button_layout.addWidget(self.label)
        box_and_button_layout.addLayout(button_layout)
        
        # Header-Layout erstellen
        #header_layout = QHBoxLayout()
        #header_layout.setContentsMargins(0, 0, 0, 0)
        #header_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Links ausrichten

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

        # Schließen-Schaltfläche mit Icon
        self.btn_close = QPushButton()
        self.btn_close.setIcon(QIcon("./images/close.svg"))
        self.btn_close.setFixedSize(30, 30)
        self.btn_close.setStyleSheet("background-color: #e00505;")  # Hintergrundfarbe auf rot setzen
        self.btn_close.clicked.connect(self.close)

        
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.toolbar.setFloatable(False)
        self.toolbar.mousePressEvent = self.mousePressEvent
        self.toolbar.mouseMoveEvent = self.moveWindow
        self.toolbar.setIconSize(QSize(100, 100))
        self.toolbar.setStyleSheet("background-color: #2b2b2b; border: none;")
        self.toolbar.addWidget(self.header_icon)
        self.toolbar.addWidget(self.header_text)
        # Platzhalter hinzufügen, um die Schließen-Schaltfläche nach rechts zu schieben
        self.btn_minimize = QPushButton()
        self.btn_minimize.setIcon(QIcon("./images/minimize.svg"))
        self.btn_minimize.setFixedSize(30, 30)
        self.btn_minimize.setStyleSheet("background-color: darkgray;")  # Hintergrundfarbe auf gelb setzen
        self.btn_minimize.clicked.connect(self.showMinimized)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolbar.addWidget(spacer)
        self.toolbar.addWidget(self.btn_minimize)
        self.toolbar.addWidget(self.btn_close)
        # Schaltflächen zum Header-Layout hinzufügen
        #header_layout.addWidget(self.header_icon)  # Icon hinzufügen
        #header_layout.addWidget(self.header_text)  # Text hinzufügen
        #header_layout.addStretch()  # Platzhalter hinzufügen, um die restlichen Widgets nach rechts zu schieben
        #header_layout.addWidget(self.btn_drag)
        #header_layout.addWidget(self.btn_close)

        # Header-Layout zum Hauptlayout hinzufügen
        #lay.addLayout(header_layout)
        self.addToolBar(self.toolbar)
        # Setze das zentrale Widget zwischen Header und Button-Layout
        lay.addLayout(box_and_button_layout)
        
        self.setCentralWidget(frame)

        # Button-Layout zum Hauptlayout hinzufügen
        
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
        self.btn_save_polygon.setVisible(False)
        self.capturer_rectangle = Capture_Rectangle(self)
        self.capturer_rectangle.show()
        self.btn_sized_box.setVisible(True)
        self.btn_save_rectangle.setVisible(True)
        self.adjustSize()  # Größe des Fensters anpassen

    def capture_polygon(self):
        self.btn_save_rectangle.setVisible(False)
        self.capturer_polygon = Capture_Polygon(self)
        self.capturer_polygon.show()
        self.btn_sized_box.setVisible(True)
        self.btn_save_polygon.setVisible(True) # Verbindung zum Signal
        self.adjustSize()

    def save_recangle(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Image files (*.png *.jpg *.bmp)")
        if file_name:
                self.capturer_rectangle.imgmap.save(file_name)

    def save_polygon(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Image files (*.png *.jpg *.bmp)")
        if file_name:
                self.capturer_polygon.imgmap.save(file_name)
  

if __name__ == "__main__":
    app = QApplication(sys.argv)    
    app.setStyleSheet("""
    QFrame {
        background-color: #5d5d5d;
    }
                      
    QPushButton {
        border-radius: 1px;
        background-color: #1f5595;
        padding: 20px;
        color: white;
        font-weight: bold;
        font-family: Arial;
        font-size: 12px;
    }
                      
    QPushButton::hover {
        background-color: #ed8600
    }
    """)

    selector = ScreenRegionSelector()
    selector.show()
    app.exit(app.exec_())
