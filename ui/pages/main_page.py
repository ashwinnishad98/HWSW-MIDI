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
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import time


class PotentiometerReader(QThread):
    potentiometer_value = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.running = True
        self.mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(0, 0))
        self.channel = 1
        self.smoothing_factor = 5
        self.stability_threshold = 5
        self.confirm_threshold = 900
        self.debounce_time = 0.5
        self.last_confirm_time = 0
        self.potentiometer_values = []

    def get_smoothed_value(self):
        values = [self.mcp.read_adc(self.channel) for _ in range(self.smoothing_factor)]
        return sum(values) // len(values)

    def run(self):
        while self.running:
            value = self.get_smoothed_value()
            self.potentiometer_values.append(value)
            if len(self.potentiometer_values) > self.stability_threshold:
                self.potentiometer_values.pop(0)

            if len(set(self.potentiometer_values)) == 1 and value > self.confirm_threshold and (time.time() - self.last_confirm_time > self.debounce_time):
                self.last_confirm_time = time.time()
                self.potentiometer_value.emit(value)
            else:
                self.potentiometer_value.emit(value)

            time.sleep(0.1)

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

        self.potentiometer_reader = PotentiometerReader()
        self.potentiometer_reader.potentiometer_value.connect(self.handle_potentiometer_input)
        self.potentiometer_reader.start()

    def initUI(self):
        """
        ------------------------------------------------
        Main Menu Page with musical notes on the sides
        ------------------------------------------------
        """

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
        self.buttons = []

        for i, text in enumerate(button_texts):
            button = QPushButton(text)
            button.setFixedHeight(45)  # Fixed height for all buttons
            menu_layout.addWidget(button)
            self.buttons.append(button)
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
        self.buttons[0].clicked.connect(self.show_tutorials)
        self.buttons[1].clicked.connect(self.show_freestyle)
        self.buttons[2].clicked.connect(self.show_song_library)

        self.init_pages()

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
        num_buttons = len(self.buttons)
        print(value)
        normalized_value = int((value / 1200.0) * num_buttons)
        print(f"Normalized Value: {normalized_value}")  # Print normalized value for debugging

        selected_index = min(normalized_value, num_buttons - 1)  # Ensure index is within bounds


        for i, button in enumerate(self.buttons):
            if i == selected_index:
                button.setStyleSheet("background-color: blue; font-size: 18px; font-family: {self.font_family}; color: black;")
            else:
                button.setStyleSheet("background-color: none; font-size: 14px; font-family: {self.font_family}; color: white;")

    def closeEvent(self, event):
        self.potentiometer_reader.stop()
        self.potentiometer_reader.wait()
        event.accept()
