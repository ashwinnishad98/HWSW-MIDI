import os
import sys
import time

from config import load_font, load_stylesheet
from pages.main_page import MainWindow
from PyQt5.QtWidgets import QApplication


def create_session_folder():
    # Generate a unique folder name using a timestamp
    session_folder = os.path.join("ui", time.strftime("%Y%m%d-%H%M%S"))
    os.makedirs(session_folder, exist_ok=True)
    return session_folder


def main():
    # Create the session folder when the app starts
    session_folder = create_session_folder()
    app = QApplication(sys.argv)
    font_family = load_font()
    stylesheet = load_stylesheet(font_family)
    app.setStyleSheet(stylesheet)

    ex = MainWindow(font_family, session_folder)
    ex.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
