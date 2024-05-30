import os
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QPushButton, QWidget, QLabel
from utils.utils import add_musical_notes
import pygame

from .guitar_page import GuitarPage
from .hihat_page import HiHatPage
from .kick_page import KickPage
from .piano_page import PianoPage
from songify import Songify  # Import the Songify class


class FreestylePage(QWidget):
    def __init__(self, parent, session_folder):
        super().__init__(parent)
        self.parent = parent
        self.session_folder = session_folder
        self.initUI()

    def initUI(self):
        freestyle_layout = QHBoxLayout(self)

        # Add musical notes to the freestyle layout
        add_musical_notes(freestyle_layout)

        self.grid_layout = QGridLayout()

        # Creating 4 tiles with different option names
        option_names = ["Piano", "Guitar", "Kick Drum", "Hi-hat"]

        icons = {
            "Piano": "./assets/piano.png",
            "Guitar": "./assets/guitar.png",
            "Kick Drum": "./assets/kick.png",
            "Hi-hat": "./assets/hi-hat.png",
        }

        # Create buttons with icons
        for i, name in enumerate(option_names):
            button = QPushButton(name)
            button.setFixedSize(230, 130)  # setting button size

            # Set icon if available
            if name in icons:
                icon = QPixmap(icons[name])
                button.setIcon(QIcon(icon))
                button.setIconSize(QSize(130, 130))  # Set icon size; adjust as needed

            # Set button styling
            button.setStyleSheet(
                "text-align: bottom; font: bold; font-size: 14px; color: white;"
            )
            position = (i // 2, i % 2)
            self.grid_layout.addWidget(button, *position)

            if name == "Piano":
                button.clicked.connect(self.show_piano_page)
            elif name == "Guitar":
                button.clicked.connect(self.show_guitar_page)
            elif name == "Kick Drum":
                button.clicked.connect(self.show_kick_page)
            elif name == "Hi-hat":
                button.clicked.connect(self.show_hihat_page)

        # Back button
        back_button_freestyle = QPushButton("Back")
        back_button_freestyle.clicked.connect(lambda: self.parent.setCurrentIndex(0))
        self.grid_layout.addWidget(
            back_button_freestyle, 2, 0, 1, 2
        )  # Spanning the back button across the grid

        # Check if there are files in the session folder and add the Songify button if files exist
        if any(fname.endswith(".wav") for fname in os.listdir(self.session_folder)):
            songify_button = QPushButton("Songify!")
            songify_button.setFixedWidth(200)
            songify_button.clicked.connect(self.songify)
            self.grid_layout.addWidget(
                songify_button, 2, 1, 1, 1
            )  # Position the songify button

        freestyle_layout.addLayout(self.grid_layout)
        add_musical_notes(freestyle_layout)
        self.setLayout(freestyle_layout)

    def show_piano_page(self):
        self.piano_page = PianoPage(self, self.parent, self.session_folder)
        self.parent.addWidget(self.piano_page)
        self.parent.setCurrentWidget(self.piano_page)

    def show_guitar_page(self):
        self.guitar_page = GuitarPage(self, self.parent, self.session_folder)
        self.parent.addWidget(self.guitar_page)
        self.parent.setCurrentWidget(self.guitar_page)

    def show_kick_page(self):
        self.kick_page = KickPage(self, self.parent, self.session_folder)
        self.parent.addWidget(self.kick_page)
        self.parent.setCurrentWidget(self.kick_page)

    def show_hihat_page(self):
        self.hihat_page = HiHatPage(self, self.parent, self.session_folder)
        self.parent.addWidget(self.hihat_page)
        self.parent.setCurrentWidget(self.hihat_page)

    def songify(self):
        songify_thread = Songify(self.session_folder)
        songify_thread.finished.connect(self.on_songify_finished)
        songify_thread.start()

    def on_songify_finished(self):
        self.show_message("A Rockstar Made This!")
        self.play_final_song()

    def show_message(self, message):
        self.message_label = QLabel(message)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet("font-size: 24px; color: white;")
        self.grid_layout.addWidget(
            self.message_label, 3, 0, 1, 2
        )  # Position the message label

    def play_final_song(self):
        final_song_path = os.path.join(self.session_folder, "final.wav")
        pygame.mixer.music.load(final_song_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        self.parent.setCurrentWidget(self)
