from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QPushButton, QWidget

from utils.utils import add_musical_notes


class FreestylePage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        freestyle_layout = QHBoxLayout(self)

        # Add musical notes to the freestyle layout
        add_musical_notes(freestyle_layout)

        grid_layout = QGridLayout()

        # Creating 4 tiles with different option names
        option_names = ["Piano", "Guitar", "Drums", "Trumpet"]

        icons = {
            "Piano": "./assets/piano.png",
            "Guitar": "./assets/guitar.png",
            "Drums": "./assets/drums.png",
            "Trumpet": "./assets/trumpet.png",
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
            button.setStyleSheet(
                "text-align: bottom; font: bold; font-size: 14px; color: white;"
            )
            position = (i // 2, i % 2)
            grid_layout.addWidget(button, *position)

        # Back button
        back_button_freestyle = QPushButton("Back")
        back_button_freestyle.clicked.connect(lambda: self.parent().setCurrentIndex(0))
        grid_layout.addWidget(
            back_button_freestyle, 2, 0, 1, 2
        )  # Spanning the back button across the grid

        freestyle_layout.addLayout(grid_layout)
        add_musical_notes(freestyle_layout)
        self.setLayout(freestyle_layout)
