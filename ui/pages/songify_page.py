import os
import time

# import firebase_admin
# from firebase_admin import credentials, storage
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QVBoxLayout,
                             QWidget)

# Initialize Firebase
# cred = credentials.Certificate("ui/firebasepvt.json")
# firebase_admin.initialize_app(cred, {"storageBucket": "gs://hwsw2-e6856.appspot.com"})


class SongifyPage(QWidget):
    def __init__(self, parent, message, session_folder, stacked_widget):
        super().__init__(parent)
        self.parent = parent
        self.message = message
        self.session_folder = session_folder
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        self.message_label = QLabel(self.message)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet("font-size: 36px; color: white;")
        layout.addWidget(self.message_label, alignment=Qt.AlignCenter)

        # Button layout
        button_layout = QHBoxLayout()

        # Back button
        back_button = QPushButton("Back")
        back_button.setFixedWidth(200)
        back_button.clicked.connect(self.go_back)
        button_layout.addWidget(back_button)

        # Save button
        save_button = QPushButton("Save")
        save_button.setFixedWidth(200)
        save_button.clicked.connect(self.save_song)
        button_layout.addWidget(save_button)

        button_layout.setAlignment(Qt.AlignCenter)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def go_back(self):
        self.stacked_widget.setCurrentWidget(self.parent)

    def save_song(self):
        # Upload the final.wav file to Firebase
        final_song_path = os.path.join(self.session_folder, "final.wav")
        # self.upload_to_firebase(final_song_path)

        # Display message and go back to FreestylePage after 3 seconds
        self.message_label.setText("Your song is saved!")
        QTimer.singleShot(3000, self.go_back)

    # def upload_to_firebase(self, file_path):
    #     # Generate a unique filename with a timestamp
    #     timestamp = int(time.time())
    #     unique_filename = f"final_{timestamp}.wav"

    #     # Upload file to Firebase Storage
    #     bucket = storage.bucket()
    #     blob = bucket.blob(unique_filename)
    #     blob.upload_from_filename(file_path)
    #     print(f"File {file_path} uploaded to Firebase Storage as {unique_filename}.")
