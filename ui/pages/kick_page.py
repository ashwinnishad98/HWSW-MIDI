from PyQt5.QtWidgets import QGridLayout, QPushButton, QVBoxLayout, QWidget

from sensor.play_kick import KickLesson  # Import KickLesson


class KickPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        kick_layout = QVBoxLayout(self)
        self.grid_layout = QGridLayout()

        # Start the kick lesson when the page is displayed
        self.kick_lesson = KickLesson()
        self.kick_lesson.start()

        # Back button
        back_button_kick = QPushButton("Back")
        back_button_kick.clicked.connect(self.go_back_to_freestyle)
        self.grid_layout.addWidget(back_button_kick, 2, 0, 1, 3)

        kick_layout.addLayout(self.grid_layout)
        self.setLayout(kick_layout)

    def go_back_to_freestyle(self):
        self.kick_lesson.stop()  # Stop the kick lesson
        self.parent.setCurrentWidget(self.parent.parent())
        self.parent.removeWidget(self)
