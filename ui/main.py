import sys

from PyQt5.QtWidgets import QApplication

from config import load_font, load_stylesheet
from pages.main_page import MainWindow


def main():
    app = QApplication(sys.argv)
    font_family = load_font()
    stylesheet = load_stylesheet(font_family)
    app.setStyleSheet(stylesheet)

    ex = MainWindow(font_family)
    ex.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
