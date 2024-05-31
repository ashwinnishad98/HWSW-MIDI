from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget

class SongifyPage(QWidget):
    def __init__(self, parent, message):
        super().__init__(parent)
        self.initUI(message)

    def initUI(self, message):
        layout = QVBoxLayout(self)
        self.message_label = QLabel(message)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet("font-size: 36px; color: white;")
        layout.addWidget(self.message_label, alignment=Qt.AlignCenter)
        self.setLayout(layout)
