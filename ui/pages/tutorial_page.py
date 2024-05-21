from PyQt5.QtCore import QPropertyAnimation, QSize, Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)

from utils.utils import add_musical_notes


class TutorialPage(QWidget):
    def __init__(self, parent, font_family):
        super().__init__(parent)
        self.parent = parent  # Store the parent to interact with it
        self.font_family = font_family
        self.initUI()

    def initUI(self):
        # Main layout with stacked layout
        self.main_layout = QVBoxLayout(self)
        self.stacked_layout = QStackedLayout()
        self.main_layout.addLayout(self.stacked_layout)

        # Create the lessons page and add it to the stacked layout
        self.lessons_widget = QWidget()
        self.lessons_layout = QHBoxLayout(self.lessons_widget)
        self.lessons_layout.setAlignment(Qt.AlignCenter)
        add_musical_notes(self.lessons_layout)

        # Central widget and layout for buttons
        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout(self.central_widget)
        self.grid_layout = QGridLayout()

        self.create_grid_layout()

        self.central_layout.addLayout(self.grid_layout)
        self.lessons_layout.addWidget(self.central_widget)
        add_musical_notes(self.lessons_layout)

        self.stacked_layout.addWidget(self.lessons_widget)

        # Create the countdown page and add it to the stacked layout
        self.countdown_widget = QWidget()
        self.countdown_page_layout = QVBoxLayout(self.countdown_widget)

        # Create countdown layout with spacers to center content
        self.countdown_layout = QVBoxLayout()
        self.countdown_layout.setAlignment(Qt.AlignCenter)

        # Top spacer
        self.countdown_layout.addItem(
            QSpacerItem(20, 110, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        # Create countdown labels
        self.countdown_label = QLabel("Starting in...")
        self.countdown_label.setAlignment(Qt.AlignCenter)
        self.countdown_label.setStyleSheet(
            f"font-size: 36px; color: white; font-family: {self.font_family};"
        )
        self.countdown_layout.addWidget(self.countdown_label)

        self.number_label = QLabel("3")
        self.number_label.setAlignment(Qt.AlignCenter)
        self.number_label.setStyleSheet(
            f"font-size: 48px; color: white; font-family: {self.font_family};"
        )
        self.countdown_layout.addWidget(self.number_label)

        # Bottom spacer
        self.countdown_layout.addItem(
            QSpacerItem(20, 110, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        self.countdown_page_layout.addLayout(self.countdown_layout)

        # Add spacer to push the back button to the bottom
        self.countdown_page_layout.addItem(
            QSpacerItem(20, 110, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        # Add back button to the countdown layout
        back_button = QPushButton("Back")
        back_button.setFixedSize(200, 50)
        back_button.clicked.connect(self.go_back_to_lessons)
        self.countdown_page_layout.addWidget(
            back_button, alignment=Qt.AlignCenter | Qt.AlignBottom
        )

        self.stacked_layout.addWidget(self.countdown_widget)

        self.setLayout(self.main_layout)

    def create_grid_layout(self):
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

            button.clicked.connect(self.start_tutorial_countdown)

            self.grid_layout.addWidget(button, *position)

        # Back button to return to the main page
        self.back_button_tutorial = QPushButton("Back")
        self.back_button_tutorial.clicked.connect(self.go_back_to_main)
        self.grid_layout.addWidget(
            self.back_button_tutorial, 2, 0, 1, 2
        )  # Spanning the back button across the grid

    def start_tutorial_countdown(self):
        # Clear current countdown layout
        for i in reversed(range(self.countdown_layout.count())):
            widget = self.countdown_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Create countdown labels
        self.countdown_label = QLabel("Starting in...")
        self.countdown_label.setAlignment(Qt.AlignCenter)
        self.countdown_label.setStyleSheet(
            f"font-size: 36px; color: white; font-family: {self.font_family};"
        )
        self.countdown_layout.addWidget(self.countdown_label)

        self.number_label = QLabel("3")
        self.number_label.setAlignment(Qt.AlignCenter)
        self.number_label.setStyleSheet(
            f"font-size: 48px; color: white; font-family: {self.font_family};"
        )
        self.countdown_layout.addWidget(self.number_label)

        # Switch to the countdown page
        self.stacked_layout.setCurrentWidget(self.countdown_widget)

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

    def go_back_to_lessons(self):
        # Switch back to the lessons page
        self.stacked_layout.setCurrentWidget(self.lessons_widget)

    def go_back_to_main(self):
        # This method assumes the parent has a method to switch to the main page
        self.parent.setCurrentIndex(0)  # Assuming the main page is at index 0
