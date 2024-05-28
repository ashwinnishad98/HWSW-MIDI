from PyQt5.QtWidgets import QGridLayout, QPushButton, QVBoxLayout, QWidget

from sensor.play_piano import PianoLesson  # Import PianoLesson


class PianoPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        piano_layout = QVBoxLayout(self)
        self.grid_layout = QGridLayout()

        # Start the piano lesson when the page is displayed
        self.piano_lesson = PianoLesson()
        self.piano_lesson.start()

        # Back button
        back_button_piano = QPushButton("Back")
        back_button_piano.clicked.connect(self.go_back_to_freestyle)
        self.grid_layout.addWidget(back_button_piano, 2, 0, 1, 3)

        piano_layout.addLayout(self.grid_layout)
        self.setLayout(piano_layout)

    def go_back_to_freestyle(self):
        self.piano_lesson.stop()  # Stop the piano lesson
        self.parent.setCurrentWidget(self.parent.parent())
        self.parent.removeWidget(self)
