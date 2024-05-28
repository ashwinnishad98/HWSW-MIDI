from PyQt5.QtWidgets import QGridLayout, QPushButton, QVBoxLayout, QWidget

from sensor.play_guitar import GuitarLesson  # Import GuitarLesson


class GuitarPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        guitar_layout = QVBoxLayout(self)
        self.grid_layout = QGridLayout()

        # Start the guitar lesson when the page is displayed
        self.guitar_lesson = GuitarLesson()
        self.guitar_lesson.start()

        # Back button
        back_button_guitar = QPushButton("Back")
        back_button_guitar.clicked.connect(self.go_back_to_freestyle)
        self.grid_layout.addWidget(back_button_guitar, 2, 0, 1, 3)

        guitar_layout.addLayout(self.grid_layout)
        self.setLayout(guitar_layout)

    def go_back_to_freestyle(self):
        self.guitar_lesson.stop()  # Stop the guitar lesson
        self.parent.setCurrentWidget(self.parent.parent())
        self.parent.removeWidget(self)
