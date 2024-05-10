import pathlib
import sys
import time

from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QFontDatabase, QPixmap, QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)


class App(QMainWindow):

    def __init__(self):

        super().__init__()
        # Load the font here, inside the __init__
        font_path = str(pathlib.Path().resolve()) + "/retro.ttf"
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            if font_families:
                self.font_family = font_families[0]
        else:
            print(f"Failed to load font from {font_path}")
            self.font_family = "Arial"

        self.setWindowTitle("Music App UI")
        self.setGeometry(100, 100, 300, 200)
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.initUI()

    def initUI(self):
        """
        ------------------------------------------------
        Main Menu Page with musical notes on the sides
        ------------------------------------------------
        """
        # Create a main horizontal layout
        main_layout = QHBoxLayout()

        # Create and add the left musical note label
        left_note_label = QLabel()
        left_note_pixmap = QPixmap("./note1.png")
        left_note_label.setPixmap(left_note_pixmap.scaled(95, 95, Qt.KeepAspectRatio))
        main_layout.addWidget(left_note_label)

        self.setGeometry(80, 10, 900, 600)

        # Create the central vertical layout for the buttons
        menu_layout = QVBoxLayout()
        menu_layout.addStretch(1)

        # Add the title label to the central layout
        self.title_label = QLabel("rAIthym")
        self.title_label.setStyleSheet(
            f"""
            color: black;
            font-size: 82px;
            font-family: '{self.font_family}';
            qproperty-alignment: AlignCenter;
            padding-bottom: 100px;
            """
        )
        menu_layout.addWidget(self.title_label)

        # Add the buttons to the central layout
        button_texts = ["View Tutorials", "Freestyle", "Song Library"]
        buttons = []

        for i, text in enumerate(button_texts):
            button = QPushButton(text)
            button.setFixedHeight(45)  # Fixed height for all buttons2
            menu_layout.addWidget(button)
            buttons.append(button)
            menu_layout.setAlignment(button, Qt.AlignCenter)  # Center align the button
            if (
                i < len(button_texts) - 1
            ):  # Add spacers between buttons, but not after the last one
                inter_button_spacer = QSpacerItem(
                    20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed
                )
                menu_layout.addSpacerItem(inter_button_spacer)

        # Add the central layout to the main layout
        menu_layout.addStretch(1)
        main_layout.addLayout(menu_layout)

        # Create and add the right musical note label
        right_note_label = QLabel()
        right_note_pixmap = QPixmap("./note1.png")
        right_note_label.setPixmap(right_note_pixmap.scaled(95, 95, Qt.KeepAspectRatio))
        main_layout.addWidget(right_note_label)

        # Create a central widget to hold the main layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.stacked_widget.addWidget(central_widget)
        # self.setCentralWidget(central_widget)

        # Connect signals to slots for buttons
        buttons[0].clicked.connect(self.show_tutorials)
        buttons[1].clicked.connect(self.show_freestyle)
        buttons[2].clicked.connect(self.show_song_library)

        """
        ------------------------------------------------
        Tutorial Page
        ------------------------------------------------
        """
        self.tutorial_page = QWidget()
        tutorial_layout = QGridLayout(self.tutorial_page)

        # Creating 4 tiles
        tiles = [QPushButton(f"Lesson {i+1}") for i in range(4)]
        positions = [(i, j) for i in range(2) for j in range(2)]
        for tile, position in zip(tiles, positions):
            tile.setFixedSize(200, 100)  # Making each tile a square
            tutorial_layout.addWidget(tile, *position)

        # Back button
        back_button_tutorial = QPushButton("Back")
        back_button_tutorial.clicked.connect(
            lambda: self.stacked_widget.setCurrentIndex(0)
        )
        tutorial_layout.addWidget(
            back_button_tutorial, 2, 0, 1, 2
        )  # Spanning the back button across the grid

        self.tutorial_page.setLayout(tutorial_layout)
        self.stacked_widget.addWidget(self.tutorial_page)

        """
        ------------------------------------------------
        Freestyle Page
        ------------------------------------------------
        """
        self.freestyle_page = QWidget()
        freestyle_layout = QGridLayout()

        # Creating 4 tiles with different option names
        option_names = ["Piano", "Guitar", "Drums", "Trumpet"]

        icons = {
            "Piano": "./piano.png",
            "Guitar": "./guitar.png",
            "Drums": "./drums.png",
            "Trumpet": "./trumpet.png",
        }

        tiles = [QPushButton(name) for name in option_names]

        # Create buttons with icons
        for i, name in enumerate(option_names):
            button = QPushButton(name)
            button.setFixedSize(230, 130)  # Making each button a square

            # Set icon if available
            if name in icons:
                icon = QPixmap(icons[name])
                button.setIcon(QIcon(icon))
                button.setIconSize(QSize(130, 130))  # Set icon size; adjust as needed

            # Set button styling
            button.setStyleSheet("text-align: bottom; font: bold; font-size: 14px;")
            position = (i // 2, i % 2)
            freestyle_layout.addWidget(button, *position)

        # Back button
        back_button_freestyle = QPushButton("Back")
        back_button_freestyle.clicked.connect(
            lambda: self.stacked_widget.setCurrentIndex(0)
        )
        freestyle_layout.addWidget(
            back_button_freestyle, 2, 0, 1, 2
        )  # Spanning the back button across the grid

        self.freestyle_page.setLayout(freestyle_layout)
        self.stacked_widget.addWidget(self.freestyle_page)

        """
        ------------------------------------------------
        Song Library Page
        ------------------------------------------------
        """
        self.song_library_page = QWidget()
        song_lib_layout = QGridLayout()

        # Creating 6 tiles
        tiles = [QPushButton(f"Song {i+1}") for i in range(6)]
        positions = [(i // 3, i % 3) for i in range(6)]  # 2 rows, 3 columns
        for tile, position in zip(tiles, positions):
            tile.setFixedSize(100, 100)  # Making each tile a square
            song_lib_layout.addWidget(tile, *position)

        # Back button
        back_button_song = QPushButton("Back")
        back_button_song.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        song_lib_layout.addWidget(
            back_button_song, 2, 0, 1, 3
        )  # Spanning the back button across all columns

        self.song_library_page.setLayout(song_lib_layout)
        self.stacked_widget.addWidget(self.song_library_page)

    def show_tutorials(self):
        self.stacked_widget.setCurrentIndex(1)

    def show_freestyle(self):
        self.stacked_widget.setCurrentIndex(2)

    def show_song_library(self):
        self.stacked_widget.setCurrentIndex(3)


def main():
    font_family = "Arial"
    app = QApplication(sys.argv)
    # Load the custom font within the main function
    font_path = str(pathlib.Path().resolve()) + "/retro.ttf"
    print(font_path)
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id != -1:
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        if font_families:
            font_family = font_families[0]
        else:
            print(f"Failed to load font from {font_path}")
    app.setStyleSheet(
        f"""
        QMainWindow {{
            background-color: white;
        }}
        QPushButton {{
            color: #00ff00;
            font-family: {font_family};
            font-size: 16px;
            border: 2px solid #00ff00;
            border-radius: 10px;
            padding: 10px;
            background-color: transparent;
        }}
        QPushButton:hover {{
            background-color: #005500;
        }}
        QLabel {{
            color: white;
            font-size: 48px;
            font-family: {font_family};
            qproperty-alignment: AlignCenter;
        }}
    """
    )
    ex = App()
    ex.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")