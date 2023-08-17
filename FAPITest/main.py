import platform
import shutil
import whisper
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QMessageBox, QFileDialog, QComboBox, QVBoxLayout, QWidget
from PyQt6.QtGui import QClipboard
from PyQt6.QtCore import Qt

class TranscriptionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Transcription App')

        # Create a widget for the main window content
        widget = QWidget()
        self.setCentralWidget(widget)

        # Create a layout for the main window content
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # Create a label widget for the name
        self.name_label = QLabel(self)
        self.name_label.setText("Made by numrao200647")
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.name_label.setStyleSheet("font-weight: bold; font-size: 16px; padding-right: 20px;")

        # Create a label widget for the instructions
        self.label = QLabel(self)
        self.label.setText('Select the Whisper model size and choose the audio file')
        self.label.setStyleSheet("font-size: 14px; margin-bottom: 20px;")

        # Create a combobox widget
        self.model_size_combobox = QComboBox(self)
        self.model_size_combobox.addItems(['tiny', 'base', 'small', 'medium', 'large'])

        # Create a button widget for choosing the file
        self.choose_file_button = QPushButton(self)
        self.choose_file_button.setText('Choose File')
        self.choose_file_button.clicked.connect(self.select_audio_file)

        # Create a button widget for running the transcription
        self.run_button = QPushButton(self)
        self.run_button.setText('Run')
        self.run_button.clicked.connect(self.run_transcription)

        # Create a label widget for the transcription result
        self.result_label = QLabel(self)
        self.result_label.setText('Transcription Result:')
        self.result_label.setStyleSheet("font-weight: bold; margin-bottom: 10px;")

        # Create a label widget for displaying the transcription text
        self.transcription_label = QLabel(self)
        self.transcription_label.setWordWrap(True)
        self.transcription_label.setStyleSheet("border: 1px solid gray; padding: 10px;")

        # Create a button widget for copying the text
        self.copy_button = QPushButton(self)
        self.copy_button.setText('Copy')
        self.copy_button.clicked.connect(self.copy_text_to_clipboard)
        self.copy_button.setVisible(False)  # Hide the button initially

        # Add the widgets to the layout
        layout.addWidget(self.name_label, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.label)
        layout.addWidget(self.model_size_combobox)
        layout.addWidget(self.choose_file_button)
        layout.addWidget(self.run_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.transcription_label)
        layout.addWidget(self.copy_button)

        # Initialize the text output variable
        self.transcription_text = ''

    def select_audio_file(self):
        # Open a file dialog to select the audio file
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter('Audio Files (*.mp3 *.wav *.mp4)')
        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            file_path = file_dialog.selectedFiles()[0]

            # Get the selected model size
            model_size = self.model_size_combobox.currentText()

            # Perform transcription on the selected audio file with the chosen model size
            self.transcribe_audio(file_path, model_size)

    def transcribe_audio(self, audio_file_path, model_size):
        # Load the Whisper Model with the selected size
        whisper_model = whisper.load_model(model_size)

        # Transcribe the audio file
        transcription = whisper_model.transcribe(audio_file_path)

        # Store the transcription text
        self.transcription_text = transcription['text']

        # Update the transcription label with the result
        self.transcription_label.setText(self.transcription_text)

        # Show the copy button
        self.copy_button.setVisible(True)

    def run_transcription(self):
        # Open the file dialog to select the audio file
        self.select_audio_file()

    def copy_text_to_clipboard(self):
        # Copy the transcription text to the clipboard
        clipboard = QApplication.clipboard()
        clipboard.setText(self.transcription_text)

# Create the application instance
app = QApplication([])
window = TranscriptionApp()
window.show()

# Run the application's event loop
app.exec()
