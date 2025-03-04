import sys
import time
from PySide6 import QtCore, QtWidgets
from transcripter import transcript, translate


class TranscriptionWorker(QtCore.QThread):
    """
    Worker thread for running the transcription process
    without freezing the UI.
    """
    progress = QtCore.Signal(int)
    finished = QtCore.Signal(str, float)

    def __init__(self, file_path, mode, model_size, language=None):
        super().__init__()
        self.file_path = file_path
        self.mode = mode
        self.language = language
        self.model_size = model_size

    def run(self):
        """Runs the transcription process and emits progress signals."""
        start_time = time.time()

        self.progress.emit(10)
        srt_file = transcript.transcript(
            input_file=self.file_path,
            mode=self.mode,
            model_size=self.model_size)

        if self.language:  # If translation is required
            self.progress.emit(50)
            translate.translate_srt(srt_file, self.language)

        self.progress.emit(100)
        end_time = time.time()
        elapsed_time = end_time - start_time

        self.finished.emit(srt_file, elapsed_time)


class VideoTranscriptor(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Video Selector")
        self.setGeometry(100, 100, 200, 250)

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

        self.model_quality = QtWidgets.QComboBox()
        self.model_quality.addItems(["base", "medium", "large"])
        layout.addWidget(self.model_quality)

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
        """
        Handles transcription launch in a separate thread.
        """
        input_file = self.file_label.text()
        selected_language = self.language_combo.currentText()
        model_size = self.model_quality.currentText()

        if input_file == "No file selected":
            self.file_label.setText("Please select a video file!")
            return

        # Reset UI for new processing task
        self.progress_bar.setValue(0)
        self.launch_button.setEnabled(False)

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
        self.worker = TranscriptionWorker(
            file_path=input_file,
            mode=mode,
            model_size=model_size,
            language=lang_target)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.transcription_complete)
        self.worker.start()

    def update_progress(self, value):
        """Update the progress bar value."""
        self.progress_bar.setValue(value)

    def transcription_complete(self, srt_file, elapsed_time):
        """Handles actions after transcription is complete."""
        self.progress_bar.setValue(100)
        self.file_label.setText(f"Transcription saved at:\n{srt_file}")
        print(f"Transcription saved at: {srt_file}")

        # Show popup with computation time
        self.show_popup(srt_file, elapsed_time)

        # Reset UI so user can start a new task
        self.launch_button.setEnabled(True)
        self.file_label.setText("No file selected")
        self.progress_bar.setValue(0)

    def show_popup(self, srt_file, elapsed_time):
        """Show a message box with the transcription completion time."""
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle("Transcription Complete")
        minutes = int(elapsed_time // 60)
        seconds = elapsed_time % 60

        msg_box.setText(
            f" Transcription saved at:\n{srt_file}\n Time taken: {minutes} min {seconds:.2f} sec"
        )
        msg_box.setIcon(QtWidgets.QMessageBox.Information)
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg_box.exec()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = VideoTranscriptor()
    window.show()
    sys.exit(app.exec())
