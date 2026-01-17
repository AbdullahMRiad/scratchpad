import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QFrame
from PyQt6.QtGui import QPainter, QPen, QPainterPath, QFont
from PyQt6.QtCore import Qt, QPoint, QSize

class DrawingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.paths = []
        self.current_path = None
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.current_path = QPainterPath()
            self.current_path.moveTo(event.position())
            self.paths.append(self.current_path)
            self.update()

    def mouseMoveEvent(self, event):
        if self.current_path is not None and (event.buttons() & Qt.MouseButton.LeftButton):
            self.current_path.lineTo(event.position())
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.current_path = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Fill background with white
        painter.setBrush(Qt.GlobalColor.white)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(self.rect())

        pen = QPen(Qt.GlobalColor.black, 3, Qt.PenStyle.SolidLine)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)

        for path in self.paths:
            painter.drawPath(path)

    def clear_canvas(self):
        self.paths = []
        self.update()

class ScratchpadApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scratchpad")
        self.resize(900, 700)
        self.setStyleSheet("QMainWindow { background-color: #f3f3f3; }")

        # Main layout container
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Rounded container for the drawing area
        self.canvas_container = QFrame()
        self.canvas_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 25px;
                border: 1px solid #dcdcdc;
            }
        """)
        container_layout = QVBoxLayout(self.canvas_container)
        container_layout.setContentsMargins(5, 5, 5, 5)

        self.drawing_widget = DrawingWidget()
        container_layout.addWidget(self.drawing_widget)
        layout.addWidget(self.canvas_container)

        # Big Red Clear Button with Glyph
        self.clear_button = QPushButton("\ue107") #  glyph
        self.clear_button.setFixedSize(64, 64)
        
        # Set font for Fluent Icons
        icon_font = QFont("Segoe Fluent Icons", 20)
        self.clear_button.setFont(icon_font)
        
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #E81123;
                color: white;
                border-radius: 32px;
                border: none;
            }
            QPushButton:hover {
                background-color: #FF0000;
            }
            QPushButton:pressed {
                background-color: #C40B1A;
            }
        """)
        self.clear_button.clicked.connect(self.drawing_widget.clear_canvas)
        
        # Center the button horizontally
        layout.addWidget(self.clear_button, alignment=Qt.AlignmentFlag.AlignCenter)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScratchpadApp()
    window.show()
    sys.exit(app.exec())
