import sys

from PySide6 import QtWidgets

from transcripter import thread


class VideoTranscriptor(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Video Transcriptor")
        self.setGeometry(100, 100, 200, 250)

        layout = QtWidgets.QVBoxLayout()

        # Video selection button
        self.select_button = QtWidgets.QPushButton("Select Video")
        self.select_button.clicked.connect(self.select_video)

        # Label to show selected file
        self.file_label = QtWidgets.QLabel("No file selected")

        # Language selection dropdown
        self.language_label = QtWidgets.QLabel("Select Target Language:")

        self.language_combo = QtWidgets.QComboBox()
        self.language_combo.addItems(["English", "French", "Dutch"])

        self.model_label = QtWidgets.QLabel("Select Whisper model:")
        self.model_quality = QtWidgets.QComboBox()
        self.model_quality.addItems(["base", "medium", "large"])
        self.model_quality.setToolTip(
            "Size of the Whisper model. The better the slower")

        self.temperature_label = QtWidgets.QLabel("Temperature:")

        self.temperature_doublespin = QtWidgets.QDoubleSpinBox()
        self.temperature_doublespin.setSingleStep(0.1)  # Set step increment
        self.temperature_doublespin.setDecimals(1)  # Ensure only 1 decimal place
        self.temperature_doublespin.setValue(0.1)
        self.temperature_doublespin.setToolTip(
            "higher value = more random output, lower = more deterministic")

        self.beam_size_label = QtWidgets.QLabel("Beam Size:")
        self.beam_side_doublespin = QtWidgets.QDoubleSpinBox()
        self.beam_side_doublespin.setSingleStep(0.1)  # Set step increment
        self.beam_side_doublespin.setDecimals(1)  # Ensure only 1 decimal place
        self.beam_side_doublespin.setValue(0.5)
        self.beam_side_doublespin.setToolTip(
            "higher = better accuracy, but slower processing")

        self.chunk_duration_label = QtWidgets.QLabel("Chunk Duration:")
        self.chunk_duration_spinbox = QtWidgets.QSpinBox()
        self.chunk_duration_spinbox.setRange(100, 600)
        self.chunk_duration_spinbox.setSingleStep(1)
        self.chunk_duration_spinbox.setValue(400)
        self.chunk_duration_spinbox.setToolTip("Select a chunk value between 400 and 500")

        # Progress bar
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setValue(0)

        # Launch button
        self.launch_button = QtWidgets.QPushButton("Launch")
        self.launch_button.clicked.connect(self.launch_processing)

        layout.addWidget(self.select_button)
        layout.addWidget(self.file_label)
        layout.addWidget(self.language_label)
        layout.addWidget(self.language_combo)
        layout.addWidget(self.model_label)
        layout.addWidget(self.model_quality)
        layout.addWidget(self.beam_size_label)
        layout.addWidget(self.beam_side_doublespin)
        layout.addWidget(self.temperature_label)
        layout.addWidget(self.temperature_doublespin)
        layout.addWidget(self.chunk_duration_label)
        layout.addWidget(self.chunk_duration_spinbox)
        layout.addWidget(self.progress_bar)
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
        beam_size = self.beam_side_doublespin.value()
        temperature = self.temperature_doublespin.value()
        chunk_duration = self.chunk_duration_spinbox.value()
        # Start worker thread
        self.worker = thread.TranscriptionWorker(
            file_path=input_file,
            mode=mode,
            model_size=model_size,
            beam_size=beam_size,
            temperature=temperature,
            chunk_duration=chunk_duration,
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
