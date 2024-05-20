from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QSize
from PyQt5.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtGui import QPixmap

from utils.utils import add_musical_notes


class TutorialPage(QWidget):
    def __init__(self, parent, font_family):
        super().__init__(parent)
        self.font_family = font_family
        self.initUI()

    def initUI(self):
        # Main layout
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)

        # Add musical notes to the tutorial layout
        add_musical_notes(self.main_layout)

        # Central widget and layout for buttons
        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout(self.central_widget)
        self.grid_layout = QGridLayout()


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
                f"font-size: 18px; color: white; font-family: {self.font_family};"
            )  # Set font size and color

            # Create a layout for the button and add the label to it
            layout = QVBoxLayout(button)
            layout.addWidget(label)
            button.setLayout(layout)

            # Connect the Rhythm 1 button to the countdown function
            if lesson == "Rhythm 1":
                button.clicked.connect(self.start_tutorial_countdown)
            elif lesson == "Musical Simon Says":
                button.clicked.connect(self.start_tutorial_countdown)
            elif lesson == "Rhythm 2":
                button.clicked.connect(self.start_tutorial_countdown)
            elif lesson == "Song Follow Along":
                button.clicked.connect(self.start_tutorial_countdown)

            self.grid_layout.addWidget(button, *position)

        # Back button
        back_button_tutorial = QPushButton("Back")
        back_button_tutorial.clicked.connect(lambda: self.parent().setCurrentIndex(0))
        self.grid_layout.addWidget(
            back_button_tutorial, 2, 0, 1, 2
        )  # Spanning the back button across the grid

        self.central_layout.addLayout(self.grid_layout)
        self.main_layout.addWidget(self.central_widget)
        
        add_musical_notes(self.main_layout)
        
        self.setLayout(self.main_layout)

    def start_tutorial_countdown(self):
        # Clear current layout
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Create countdown layout
        countdown_layout = QVBoxLayout()
        countdown_layout.setAlignment(Qt.AlignCenter)

        self.countdown_label = QLabel("Starting in...")
        self.countdown_label.setAlignment(Qt.AlignCenter)
        self.countdown_label.setStyleSheet(
            f"font-size: 36px; color: white; font-family: {self.font_family};"
        )
        countdown_layout.addWidget(self.countdown_label)

        self.number_label = QLabel("3")
        self.number_label.setAlignment(Qt.AlignCenter)
        self.number_label.setStyleSheet(
            f"font-size: 48px; color: white; font-family: {self.font_family};"
        )
        countdown_layout.addWidget(self.number_label)

        # Add countdown layout to central layout
        self.central_layout.addLayout(countdown_layout)

        # Initialize timer for countdown
        self.countdown_value = 3
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_countdown)
        self.timer.start(1000)  # Update every second

    def update_countdown(self):
        if self.countdown_value > 0:
            self.animate_number_change(str(self.countdown_value))
            self.countdown_value -= 1
        else:
            self.timer.stop()
            self.countdown_label.setText("Remember the sounds!")
            self.number_label.setText("")

    def animate_number_change(self, number):
        self.number_label.setText(number)
        animation = QPropertyAnimation(self.number_label, b"size")
        animation.setDuration(500)
        animation.setStartValue(QSize(10, 10))
        animation.setEndValue(QSize(100, 100))
        animation.start()
