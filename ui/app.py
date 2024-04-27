import sys
import time
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QLabel,
    QStackedWidget,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QFontDatabase


class App(QMainWindow):

    def __init__(self):

        super().__init__()
        # Load the font here, inside the __init__
        font_path = (
            "/Users/ashwinnishad/Downloads/UW/Spring24/HWSW/HWSW-MIDI/ui/retro.ttf"
        )
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
        Main Menu Page
        ------------------------------------------------
        """
        self.title_label = QLabel("rAIthym")
        self.title_label.setStyleSheet(
            f"""
        color: white;
        font-size: 82px;
        font-family: '{self.font_family}';
        qproperty-alignment: AlignCenter;
        padding-bottom: 100px;
        """
        )

        # Adjust the window size
        self.setGeometry(80, 10, 900, 600)  # Set a larger window size

        self.menu_page = QWidget()
        menu_layout = QVBoxLayout()

        menu_layout.addStretch(1)  # Add stretch to push the title down a bit

        # Add spacer after the title
        # title_spacer = QSpacerItem(2, 2, QSizePolicy.Minimum, QSizePolicy.Fixed)
        # menu_layout.addSpacerItem(title_spacer)
        menu_layout.addWidget(self.title_label)  # Add the title label to your layout

        # Create buttons and add them to the layout with spacers
        button_texts = ["View Tutorials", "Freestyle", "Song Library"]
        buttons = []  # Keep track of the buttons to connect signals later

        for i, text in enumerate(button_texts):
            button = QPushButton(text)
            button.setFixedHeight(45)  # Fixed height for all buttons
            menu_layout.addWidget(button)
            menu_layout.setAlignment(button, Qt.AlignCenter)  # Center align the button
            buttons.append(button)  # Add the button to the list

            if (
                i < len(button_texts) - 1
            ):  # Add spacers between buttons, but not after the last one
                inter_button_spacer = QSpacerItem(
                    20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed
                )
                menu_layout.addSpacerItem(inter_button_spacer)

        menu_layout.addStretch(1)

        self.menu_page.setLayout(menu_layout)
        self.stacked_widget.addWidget(self.menu_page)

        # Connect signals to slots for buttons
        buttons[0].clicked.connect(
            lambda: self.stacked_widget.setCurrentIndex(1)
        )  # View Tutorials
        buttons[1].clicked.connect(
            lambda: self.stacked_widget.setCurrentIndex(2)
        )  # Freestyle
        buttons[2].clicked.connect(
            lambda: self.stacked_widget.setCurrentIndex(3)
        )  # Song Library

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
        option_names = ["Piano", "Guitar", "Kick Drum", "Hi Hat"]
        tiles = [QPushButton(name) for name in option_names]
        positions = [(i // 2, i % 2) for i in range(4)]  # 2 rows, 2 columns
        for tile, position in zip(tiles, positions):
            tile.setFixedSize(200, 100)  # Making each tile a square
            freestyle_layout.addWidget(tile, *position)

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


def main():
    app = QApplication(sys.argv)
    # Load the custom font within the main function
    font_path = "/Users/ashwinnishad/Downloads/UW/Spring24/HWSW/HWSW-MIDI/ui/retro.ttf"
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id != -1:
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        if font_families:
            font_family = font_families[0]
        else:
            print(f"Failed to load font from {font_path}")
            font_family = "Arial"
    app.setStyleSheet(
        f"""
        QMainWindow {{
            background-color: black;
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
