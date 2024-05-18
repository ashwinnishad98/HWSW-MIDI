"""
Loads Fonts and Stylesheets
"""

import pathlib

from PyQt5.QtGui import QFontDatabase


def load_font():
    font_path = str(pathlib.Path(__file__).parent / "assets" / "retro.ttf")
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id != -1:
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        if font_families:
            return font_families[0]
    print(f"Failed to load font from {font_path}")
    return "Arial"


def load_stylesheet(font_family):
    stylesheet_path = str(pathlib.Path(__file__).parent / "style" / "main_style.qss")
    with open(stylesheet_path, "r") as f:
        stylesheet = f.read()
    return stylesheet.replace("Arial", font_family)
