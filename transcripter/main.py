import sys
from PySide6 import QtCore, QtWidgets
from transcripter import transcript, translate


class TranscriptionWorker(QtCore.QThread):
    """
    Worker thread for running the transcription process
    without freezing the UI.
    """
    progress = QtCore.Signal(int)  # Signal to update progress bar
    finished = QtCore.Signal(str)  # Signal when transcription is complete

    def __init__(self, file_path, mode, language=None):
        super().__init__()
        self.file_path = file_path
        self.mode = mode
        self.language = language

    def run(self):
        """Runs the transcription process and emits progress signals."""
        self.progress.emit(10)  # Start progress
        srt_file = transcript.transcript(self.file_path, self.mode)

        if self.language:  # If translation is required
            self.progress.emit(50)  # Midway progress
            translate.translate_srt(srt_file, self.language)

        self.progress.emit(100)  # Finish progress
        self.finished.emit(srt_file)  # Send back the generated file path


class VideoSelectorApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Video Selector")
        self.setGeometry(100, 100, 400, 250)

        layout = QtWidgets.QVBoxLayout()

        # Video selection button
        self.select_button = QtWidgets.QPushButton("Select Video")
        self.select_button.clicked.connect(self.select_video)
        layout.addWidget(self.select_button)

        # Label to show selected file
        self.file_label = QtWidgets.QLabel("No file selected")
        layout.addWidget(self.file_label)

        # Language selection dropdown
        self.language_label = QtWidgets.QLabel("Select Target Language:")
        layout.addWidget(self.language_label)

        self.language_combo = QtWidgets.QComboBox()
        self.language_combo.addItems(["English", "French", "Dutch"])
        layout.addWidget(self.language_combo)

        # Progress bar
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # Launch button
        self.launch_button = QtWidgets.QPushButton("Launch")
        self.launch_button.clicked.connect(self.launch_processing)
        layout.addWidget(self.launch_button)

        self.setLayout(layout)

    def select_video(self):
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self,
            "Select Video File",
            "",
            "Video Files (*.mp4 *.avi *.mov *.mkv)"
        )
        if file_path:
            self.file_label.setText(file_path)

    def launch_processing(self):
        """Handles transcription launch in a separate thread."""
        input_file = self.file_label.text()
        selected_language = self.language_combo.currentText()

        if input_file == "No file selected":
            self.file_label.setText("Please select a video file!")
            return

        # Reset UI for new processing task
        self.progress_bar.setValue(0)
        self.launch_button.setEnabled(False)  # Disable button during processing

        # Determine processing mode
        if selected_language == "English":
            mode = "translate"
            lang_target = None  # No extra translation needed
        elif selected_language == "French":
            mode = "transcribe"
            lang_target = "fr"  # Translate to French
        elif selected_language == "Dutch":
            mode = "transcribe"
            lang_target = "nl"  # Translate to Dutch
        else:
            self.file_label.setText("Unsupported language!")
            return

        # Start worker thread
        self.worker = TranscriptionWorker(input_file, mode, lang_target)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.transcription_complete)
        self.worker.start()

    def update_progress(self, value):
        """Update the progress bar value."""
        self.progress_bar.setValue(value)

    def transcription_complete(self, srt_file):
        """Handles actions after transcription is complete."""
        self.progress_bar.setValue(100)
        self.file_label.setText(f"Transcription saved at:\n{srt_file}")
        print(f"Transcription saved at: {srt_file}")

        # Reset UI so user can start a new task
        self.launch_button.setEnabled(True)  # Re-enable launch button
        self.file_label.setText("No file selected")  # Reset file label
        self.progress_bar.setValue(0)  # Reset progress bar


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = VideoSelectorApp()
    window.show()
    sys.exit(app.exec())
