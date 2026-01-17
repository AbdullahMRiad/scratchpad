import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PyQt6.QtGui import QPainter, QPen, QAction, QPainterPath
from PyQt6.QtCore import Qt, QPoint

class DrawingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.paths = []  # List to store all vector paths
        self.current_path = None
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
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)  # Enable smooth drawing

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
        self.setWindowTitle("Scratchpad (Vector)")
        self.resize(800, 600)

        # Main layout container
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Drawing area
        self.drawing_widget = DrawingWidget()
        layout.addWidget(self.drawing_widget)

        # Clear button
        self.clear_button = QPushButton("Clear All")
        self.clear_button.clicked.connect(self.drawing_widget.clear_canvas)
        layout.addWidget(self.clear_button)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScratchpadApp()
    window.show()
    sys.exit(app.exec())