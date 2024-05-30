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

from sensor.lesson_rhythm1 import RhythmLesson


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

        # Add kirb image
        self.kirb_label = QLabel()
        self.kirb_pixmap = QPixmap("assets/kirb.png")
        self.kirb_label.setPixmap(self.kirb_pixmap.scaled(200, 200, Qt.KeepAspectRatio))
        self.kirb_label.setAlignment(Qt.AlignCenter)
        self.countdown_layout.addWidget(self.kirb_label)
        self.kirb_label.hide()  # Hide initially

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

        # Create the message display label
        self.message_label = QLabel("")
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet(
            f"font-size: 24px; color: white; font-family: {self.font_family};"
        )
        self.main_layout.addWidget(self.message_label)

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

            if lesson == "Rhythm 1":
                button.clicked.connect(self.start_rhythm_1)

            self.grid_layout.addWidget(button, *position)

        # Back button to return to the main page
        self.back_button_tutorial = QPushButton("Back")
        self.back_button_tutorial.clicked.connect(self.go_back_to_main)
        self.grid_layout.addWidget(
            self.back_button_tutorial, 2, 0, 1, 2
        )  # Spanning the back button across the grid

    def start_rhythm_1(self):
        self.message_label.clear()
        self.kirb_label.show()  # Show kirb image when the tutorial starts
        self.start_countdown("Starting in...", 3, self.start_rhythm_lesson)

    def start_countdown(self, text, count, callback):
        self.countdown_label.setText(text)
        self.number_label.setText(str(count))
        self.stacked_layout.setCurrentWidget(self.countdown_widget)
        self.count = count
        self.callback = callback
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_countdown)
        self.timer.start(1000)

    def update_countdown(self):
        if self.count > 0:
            self.number_label.setText(str(self.count))
            self.animate_number_change(str(self.count))
            self.count -= 1
        else:
            self.timer.stop()
            self.number_label.clear()
            # self.countdown_label.clear()
            self.callback()

    def animate_number_change(self, number):
        self.number_label.setText(number)
        animation = QPropertyAnimation(self.number_label, b"size")
        animation.setDuration(500)
        animation.setStartValue(QSize(10, 10))
        animation.setEndValue(QSize(100, 100))
        animation.start()

    def start_rhythm_lesson(self):
        username = "test_user"  # Replace with actual username if needed
        self.update_message("Remember the sounds!")
        QTimer.singleShot(
            1000, self.execute_rhythm_lesson
        )  # Wait for 1 second before starting the lesson

    def execute_rhythm_lesson(self):
        self.rhythm_lesson = RhythmLesson("test_user")
        self.rhythm_lesson.progress.connect(self.update_message)
        self.rhythm_lesson.sequence_complete.connect(self.start_user_turn_countdown)
        self.rhythm_lesson.score_signal.connect(self.display_score)
        self.rhythm_lesson.start()

    def start_user_turn_countdown(self):
        self.start_countdown("Your turn! Starting in...", 3, self.start_user_turn)

    def start_user_turn(self):
        self.update_message("")
        self.countdown_label.setText("Start!")

    def update_message(self, text):
        self.message_label.setText(text)

    def display_score(self, score_text):
        # self.countdown_label.clear()
        self.update_message(score_text)
        QTimer.singleShot(
            5000, self.go_back_to_lessons
        )  # Navigate back after 5 seconds

    def go_back_to_lessons(self):
        self.kirb_label.hide()  # Hide kirb image when tutorial ends
        self.message_label.clear()
        self.stacked_layout.setCurrentWidget(self.lessons_widget)

    def go_back_to_main(self):
        self.kirb_label.hide()  # Hide kirb image when navigating back to the main page
        self.message_label.clear()
        self.parent.setCurrentIndex(0)  # Assuming the main page is at index 0
