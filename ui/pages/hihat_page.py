from PyQt5.QtWidgets import QGridLayout, QPushButton, QVBoxLayout, QWidget

from sensor.play_hihat import HiHatLesson  # Import HiHatLesson


class HiHatPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        hihat_layout = QVBoxLayout(self)
        self.grid_layout = QGridLayout()

        # Start the hihat lesson when the page is displayed
        self.hihat_lesson = HiHatLesson()
        self.hihat_lesson.start()

        # Back button
        back_button_hihat = QPushButton("Back")
        back_button_hihat.clicked.connect(self.go_back_to_freestyle)
        self.grid_layout.addWidget(back_button_hihat, 2, 0, 1, 3)

        hihat_layout.addLayout(self.grid_layout)
        self.setLayout(hihat_layout)

    def go_back_to_freestyle(self):
        self.hihat_lesson.stop()  # Stop the hihat lesson
        self.parent.setCurrentWidget(self.parent.parent())
        self.parent.removeWidget(self)
