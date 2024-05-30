from pages.freestyle_page import FreestylePage
from pages.song_library_page import SongLibraryPage
from pages.tutorial_page import TutorialPage
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import (
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
from utils.utils import add_musical_notes
import spidev

# Setup SPI for MCP3008
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000


# Function to read from MCP3008
def read_channel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data


class PotentiometerReader(QThread):
    potentiometer_value = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        while self.running:
            value = read_channel(0)  # Read the potentiometer value from CH0
            self.potentiometer_value.emit(value)
            self.msleep(100)  # Read every 100ms

    def stop(self):
        self.running = False


class MainWindow(QMainWindow):
    def __init__(self, font_family):
        super().__init__()
        self.font_family = font_family
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
        self.potentiometer_value = 0

        main_layout = QHBoxLayout()

        # Add musical notes to the main layout
        add_musical_notes(main_layout)

        self.setGeometry(80, 10, 900, 600)

        # Create the central vertical layout for the buttons
        menu_layout = QVBoxLayout()
        menu_layout.addStretch(1)

        # Add the title label to the central layout
        self.title_label = QLabel("rAIthym")
        self.title_label.setStyleSheet(
            f"""
            color: #fff37b;
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
            button.setFixedHeight(45)  # Fixed height for all buttons
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

        add_musical_notes(main_layout)

        # Create a central widget to hold the main layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.stacked_widget.addWidget(central_widget)
        # self.setCentralWidget(central_widget)

        # Connect signals to slots for buttons
        buttons[0].clicked.connect(self.show_tutorials)
        buttons[1].clicked.connect(self.show_freestyle)
        buttons[2].clicked.connect(self.show_song_library)

        self.init_pages()

        # Initialize the potentiometer reader
        self.pot_reader = PotentiometerReader()
        self.pot_reader.potentiometer_value.connect(self.handle_potentiometer_input)
        self.pot_reader.start()

    def init_pages(self):
        self.tutorial_page = TutorialPage(self.stacked_widget, self.font_family)
        self.stacked_widget.addWidget(self.tutorial_page)

        self.freestyle_page = FreestylePage(self.stacked_widget)
        self.stacked_widget.addWidget(self.freestyle_page)

        self.song_library_page = SongLibraryPage(self.stacked_widget)
        self.stacked_widget.addWidget(self.song_library_page)

    def show_tutorials(self):
        self.stacked_widget.setCurrentWidget(self.tutorial_page)

    def show_freestyle(self):
        self.stacked_widget.setCurrentWidget(self.freestyle_page)

    def show_song_library(self):
        self.stacked_widget.setCurrentWidget(self.freestyle_page)

    def handle_potentiometer_input(self, value):
        # Normalize the potentiometer value to a range, e.g., 0-100
        normalized_value = int((value / 1023.0) * 100)

        # Determine which button to highlight based on the normalized value
        if normalized_value < 33:
            self.highlight_button(0)
        elif normalized_value < 66:
            self.highlight_button(1)
        else:
            self.highlight_button(2)

    def highlight_button(self, index):
        # Reset all buttons to default style
        for button in self.buttons:
            button.setStyleSheet("")

        # Highlight the selected button
        self.buttons[index].setStyleSheet("background-color: yellow;")

    def closeEvent(self, event):
        self.pot_reader.stop()
        super().closeEvent(event)
