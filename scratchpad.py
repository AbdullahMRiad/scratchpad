import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PyQt6.QtGui import QPainter, QPen, QPainterPath, QFont
from PyQt6.QtCore import Qt, QSize

class DrawingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.paths = []
        self.current_path = None
        # We don't need translucent background anymore since we want to fill the screen
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.GlobalColor.white)
        self.setPalette(p)

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
        
        # Draw paths
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
        
        # Drawing area is now the central widget, taking up everything
        self.drawing_widget = DrawingWidget()
        self.setCentralWidget(self.drawing_widget)

        # Use a layout on the DrawingWidget to position the button overlay
        overlay_layout = QVBoxLayout(self.drawing_widget)
        overlay_layout.setContentsMargins(0, 0, 0, 30) # 30px padding from bottom
        overlay_layout.addStretch() # Push button to bottom

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
        
        # Add button to the overlay layout
        overlay_layout.addWidget(self.clear_button, alignment=Qt.AlignmentFlag.AlignCenter)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScratchpadApp()
    window.show()
    sys.exit(app.exec())