"""
Utility Functions
"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel


def add_musical_notes(layout):
    note_label = QLabel()
    note_pixmap = QPixmap("assets/note1.png")
    note_label.setPixmap(note_pixmap.scaled(95, 95, Qt.KeepAspectRatio))
    layout.addWidget(note_label)
