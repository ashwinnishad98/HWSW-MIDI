from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QGridLayout, QHBoxLayout, QLabel, QPushButton,
                             QVBoxLayout, QWidget)

from utils.utils import add_musical_notes


class TutorialPage(QWidget):
    def __init__(self, parent, font_family):
        super().__init__(parent)
        self.font_family = font_family
        self.initUI()

    def initUI(self):
        tutorial_layout = QHBoxLayout(self)

        # Add musical notes to the tutorial layout
        add_musical_notes(tutorial_layout)

        grid_layout = QGridLayout()

        # Creating 4 tiles
        lessons_list = [
            "Rhythm 1",
            "Musical Simon Says",
            "Rhythm 2",
            "Song Follow Along",
        ]
        positions = [(i, j) for i in range(2) for j in range(2)]

        for lesson, position in zip(lessons_list, positions):
            button = QPushButton()
            button.setFixedSize(200, 100)

            # Create a label to wrap the text inside the button
            label = QLabel(lesson)
            label.setWordWrap(True)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet(
                f"font-size: 18px; color: black; font-family: {self.font_family};"
            )  # Set font size and color

            # Create a layout for the button and add the label to it
            layout = QVBoxLayout(button)
            layout.addWidget(label)
            button.setLayout(layout)

            grid_layout.addWidget(button, *position)

        # Back button
        back_button_tutorial = QPushButton("Back")
        back_button_tutorial.clicked.connect(lambda: self.parent().setCurrentIndex(0))
        grid_layout.addWidget(
            back_button_tutorial, 2, 0, 1, 2
        )  # Spanning the back button across the grid

        tutorial_layout.addLayout(grid_layout)
        add_musical_notes(tutorial_layout)
        self.setLayout(tutorial_layout)
