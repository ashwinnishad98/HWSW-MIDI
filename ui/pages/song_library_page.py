from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from utils.utils import add_musical_notes


class SongLibraryPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        song_lib_layout = QHBoxLayout(self)

        # Add musical notes to the song library layout
        add_musical_notes(song_lib_layout)

        grid_layout = QGridLayout()

        # Creating 6 tiles
        tiles = [QPushButton(f"Song {i+1}") for i in range(6)]
        positions = [(i // 3, i % 3) for i in range(6)]  # 2 rows, 3 columns
        for tile, position in zip(tiles, positions):
            tile.setFixedSize(100, 100)  # Making each tile a square
            grid_layout.addWidget(tile, *position)

        # Back button
        back_button_song = QPushButton("Back")
        back_button_song.setFixedSize(200, 50)
        back_button_song.clicked.connect(lambda: self.parent().setCurrentIndex(0))
        grid_layout.addWidget(back_button_song, 2, 0, 1, 3)

        song_lib_layout.addLayout(grid_layout)
        add_musical_notes(song_lib_layout)

        self.setLayout(song_lib_layout)
