import os

import pygame
from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QGridLayout, QHBoxLayout, QPushButton,
                             QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from utils.utils import add_musical_notes

from .guitar_page import GuitarPage
from .hihat_page import HiHatPage
from .kick_page import KickPage
from .piano_page import PianoPage
from .songify import Songify  # Import the Songify class
from .songify_page import SongifyPage


class FreestylePage(QWidget):
    def __init__(self, parent, session_folder):
        super().__init__(parent)
        self.parent = parent
        self.session_folder = session_folder
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout(self)

        # Add musical notes to the freestyle layout
        add_musical_notes(main_layout)

        central_layout = QVBoxLayout()

        self.grid_layout = QGridLayout()

        # Creating 4 tiles with different option names
        option_names = ["Piano", "Guitar", "Kick Drum", "Hi-hat"]

        icons = {
            "Piano": "./assets/piano.png",
            "Guitar": "./assets/guitar.png",
            "Kick Drum": "./assets/kick.png",
            "Hi-hat": "./assets/hi-hat.png",
        }

        top_spacer = QSpacerItem(20, 150, QSizePolicy.Minimum, QSizePolicy.Expanding)
        central_layout.addItem(top_spacer)

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

            central_layout.addLayout(self.grid_layout)

        button_layout = QHBoxLayout()

        # Back button
        back_button_freestyle = QPushButton("Back")
        back_button_freestyle.setFixedWidth(200)
        back_button_freestyle.clicked.connect(self.go_back)
        button_layout.addWidget(back_button_freestyle)

        # Check if there are files in the session folder and add the Songify button if files exist
        # if any(fname.endswith(".wav") for fname in os.listdir(self.session_folder)):
        songify_button = QPushButton("Songify!")
        songify_button.setFixedWidth(200)
        songify_button.clicked.connect(self.songify)
        button_layout.addWidget(songify_button)

        button_layout.setAlignment(Qt.AlignCenter)
        central_layout.addLayout(button_layout)

        bottom_spacer = QSpacerItem(20, 150, QSizePolicy.Minimum, QSizePolicy.Expanding)
        central_layout.addItem(bottom_spacer)

        main_layout.addLayout(central_layout)

        add_musical_notes(main_layout)
        self.setLayout(main_layout)

    def show_piano_page(self):
        self.stop_current_lesson()
        self.piano_page = PianoPage(self, self.parent, self.session_folder)
        self.parent.addWidget(self.piano_page)
        self.parent.setCurrentWidget(self.piano_page)

    def show_guitar_page(self):
        self.stop_current_lesson()
        self.guitar_page = GuitarPage(self, self.parent, self.session_folder)
        self.parent.addWidget(self.guitar_page)
        self.parent.setCurrentWidget(self.guitar_page)

    def show_kick_page(self):
        self.stop_current_lesson()
        self.kick_page = KickPage(self, self.parent, self.session_folder)
        self.parent.addWidget(self.kick_page)
        self.parent.setCurrentWidget(self.kick_page)

    def show_hihat_page(self):
        self.stop_current_lesson()
        self.hihat_page = HiHatPage(self, self.parent, self.session_folder)
        self.parent.addWidget(self.hihat_page)
        self.parent.setCurrentWidget(self.hihat_page)

    def stop_current_lesson(self):
        if hasattr(self, "piano_page") and self.piano_page.piano_lesson.running:
            self.piano_page.piano_lesson.stop()
        if hasattr(self, "guitar_page") and self.guitar_page.guitar_lesson.running:
            self.guitar_page.guitar_lesson.stop()
        if hasattr(self, "kick_page") and self.kick_page.kick_lesson.running:
            self.kick_page.kick_lesson.stop()
        if hasattr(self, "hihat_page") and self.hihat_page.hihat_lesson.running:
            self.hihat_page.hihat_lesson.stop()
        pygame.mixer.stop()

    def songify(self):
        self.songify_thread = Songify(self.session_folder)
        self.songify_thread.finished.connect(self.on_songify_finished)
        self.songify_thread.start()

    def on_songify_finished(self):
        self.show_message_page("Wow! You're a rockstar!")
        self.play_final_song()

    def show_message_page(self, message):
        self.message_page = SongifyPage(self, message, self.session_folder, self.parent)
        self.parent.addWidget(self.message_page)
        self.parent.setCurrentWidget(self.message_page)

    def play_final_song(self):
        final_song_path = os.path.join(self.session_folder, "final.wav")
        pygame.mixer.music.load(final_song_path)
        pygame.mixer.music.play()
        self.check_song_playing()

    def check_song_playing(self):
        if pygame.mixer.music.get_busy():
            QTimer.singleShot(100, self.check_song_playing)
        else:
            self.parent.setCurrentWidget(self)
            self.message_page.deleteLater()

    def go_back(self):
        self.stop_current_lesson()
        self.parent.setCurrentIndex(0)
