import sys
from PySide6 import QtWidgets
from PySide6 import QtGui

from transcripter import thread
from transcripter import ffmpeg
from transcripter import constants
from transcripter import preferences


class VideoTranscriptor(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # Add ffmpeg to path
        ffmpeg.add_ffmpeg_to_path()
        self.prompt = None
        preferences.set_default_preferences()
        self.initUI()
        self.load_from_prefs()

    def initUI(self):
        self.setWindowTitle(constants.TOOLNAME)
        self.setGeometry(100, 100, 200, 250)

        self.main_layout = QtWidgets.QVBoxLayout()

        self.settings_container = QtWidgets.QFrame()
        self.settings_container.setVisible(False)
        self.settings_main_layout = QtWidgets.QVBoxLayout()
        self.settings_container.setLayout(self.settings_main_layout)

        # Video selection button
        self.select_button = QtWidgets.QPushButton("Select Video")
        self.select_button.clicked.connect(self.select_video)

        # Label to show selected file
        self.file_label = QtWidgets.QLabel("No file selected")

        # Language selection dropdown
        self.language_label = QtWidgets.QLabel("Select Target Language:")
        self.language_combo = QtWidgets.QComboBox()
        self.language_combo.addItems((constants.LANGUAGE_CODES.keys()))
        self.language_combo.setCurrentText(
            list(constants.LANGUAGE_CODES.keys())[0])

        # Select whisper model to use
        self.model_label = QtWidgets.QLabel("Select Whisper model:")
        self.model_version = QtWidgets.QComboBox()
        self.model_version.addItems(constants.SETTING_NAMES_MODEL)
        self.model_version.setCurrentText(constants.MODEL)
        self.model_version.setToolTip(
            "Select the Whisper model. The better the slower")

        # Add force new transcibe checkbox
        self.force_new_transcribe_checkbox = QtWidgets.QCheckBox(
            "Force new srt")
        self.force_new_transcribe_checkbox.setChecked(True)

        # Add setting checkbox
        self.show_settings_checkbox = QtWidgets.QCheckBox("Settings")
        self.show_settings_checkbox.setChecked(False)
        self.show_settings_checkbox.stateChanged.connect(
            self.toggle_settings)

        # Set model beam_size
        self.beam_size_label = QtWidgets.QLabel(
            f"{constants.SETTING_NAME_BEAM_SIZE}:")
        self.beam_side_doublespin = QtWidgets.QDoubleSpinBox()
        self.beam_side_doublespin.setSingleStep(0.1)
        self.beam_side_doublespin.setDecimals(1)
        self.beam_side_doublespin.setValue(constants.BEAM_SIZE)
        self.beam_side_doublespin.setToolTip(
            "higher = better accuracy, but slower processing")

        # Set model temperature
        self.temperature_label = QtWidgets.QLabel(
            f"{constants.SETTING_NAME_TEMPERATURE}:")
        self.temperature_doublespin = QtWidgets.QDoubleSpinBox()
        self.temperature_doublespin.setSingleStep(0.1)
        self.temperature_doublespin.setDecimals(1)
        self.temperature_doublespin.setValue(constants.TEMPERATURE)
        self.temperature_doublespin.setToolTip(
            "higher value = more random output, lower = more deterministic")

        # Compression ratio threshold
        self.compression_ratio_threshold_label = QtWidgets.QLabel(
            f'{constants.SETTING_NAME_COMPRESSION_RATIO}:')
        self.compression_ratio_threshold_spinbox = QtWidgets.QDoubleSpinBox()
        self.compression_ratio_threshold_spinbox.setRange(1, 5)
        self.compression_ratio_threshold_spinbox.setSingleStep(0.1)
        self.compression_ratio_threshold_spinbox.setValue(
            constants.COMPRESSION_RATIO)
        self.compression_ratio_threshold_spinbox.setToolTip(
            "Lower this if too much text lines")

        # Set chunk duration
        self.chunk_duration_label = QtWidgets.QLabel(
            f"{constants.SETTING_NAME_CHUNK_DURATION}:")
        self.chunk_duration_spinbox = QtWidgets.QSpinBox()
        self.chunk_duration_spinbox.setRange(100, 600)
        self.chunk_duration_spinbox.setSingleStep(1)
        self.chunk_duration_spinbox.setValue(constants.CHUNK_DURATION)
        self.chunk_duration_spinbox.setToolTip(
            "Split input video into small parts. "
            "Select a chunk value between 100 and 600")

        # Set prompt
        self.prompt_button = QtWidgets.QPushButton("Prompt Hint")
        self.prompt_button.setToolTip(
            "A hint to guide the model "
            "(useful for specific vocabulary or context)")
        self.prompt_button.clicked.connect(self.set_prompt)

        # Save settings
        self.save_settings_layout = QtWidgets.QHBoxLayout()
        self.save_settings_button = QtWidgets.QPushButton('Save as default')
        self.save_settings_button.clicked.connect(
            self.save_settings)

        self.reset_all_settings_button = QtWidgets.QPushButton('Reset all')
        self.reset_all_settings_button.clicked.connect(
            self.reset_all_settings)

        # Progress bar
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setValue(0)

        # Launch button
        self.launch_button = QtWidgets.QPushButton("Launch")
        self.launch_button.clicked.connect(self.launch_processing)

        # Version info
        version_info = QtWidgets.QLabel(constants.TOOL_VERSION)
        version_info.setFont(QtGui.QFont("Arial", 8))

        self.save_settings_layout.addWidget(self.save_settings_button)
        self.save_settings_layout.addWidget(self.reset_all_settings_button)

        self.settings_main_layout.addWidget(self.beam_size_label)
        self.settings_main_layout.addWidget(self.beam_side_doublespin)
        self.settings_main_layout.addWidget(self.temperature_label)
        self.settings_main_layout.addWidget(self.temperature_doublespin)
        self.settings_main_layout.addWidget(
            self.compression_ratio_threshold_label)
        self.settings_main_layout.addWidget(
            self.compression_ratio_threshold_spinbox)
        self.settings_main_layout.addWidget(self.chunk_duration_label)
        self.settings_main_layout.addWidget(self.chunk_duration_spinbox)
        self.settings_main_layout.addWidget(self.prompt_button)
        self.settings_main_layout.addLayout(
            self.save_settings_layout)

        self.main_layout.addWidget(self.select_button)
        self.main_layout.addWidget(self.file_label)
        self.main_layout.addWidget(self.language_label)
        self.main_layout.addWidget(self.language_combo)
        self.main_layout.addWidget(self.model_label)
        self.main_layout.addWidget(self.model_version)
        self.main_layout.addWidget(self.force_new_transcribe_checkbox)
        self.main_layout.addWidget(self.show_settings_checkbox)
        self.main_layout.addWidget(self.settings_container)
        self.main_layout.addWidget(self.progress_bar)
        self.main_layout.addWidget(self.launch_button)
        self.main_layout.addWidget(version_info)
        self.setLayout(self.main_layout)

    def set_prompt(self):
        """Open the PromptInputDialog and get user input."""
        dialog = PromptInputDialog()
        if dialog.exec():  # If user clicks "Save"
            user_text = dialog.text_edit.toPlainText()
            QtWidgets.QMessageBox.information(
                self, "Prompt Saved", f"New Prompt:\n{user_text}")

    def save_settings(self):
        print('Saving settings')
        preferences.set_preference(
            "target_language",
            self.language_combo.currentText())
        preferences.set_preference(
            "model",
            self.model_version.currentText())
        preferences.set_preference(
            "beam_size",
            self.beam_side_doublespin.value())
        preferences.set_preference(
            "temperature",
            self.temperature_doublespin.value())
        preferences.set_preference(
            "compression_ratio",
            self.compression_ratio_threshold_spinbox.value())
        preferences.set_preference(
            "chunk_duration",
            self.chunk_duration_spinbox.value())

    def reset_all_settings(self):
        preferences.reset_preferences()
        self.load_from_prefs()

    def load_from_prefs(self):

        target_language = preferences.get_preference("target_language")
        model = preferences.get_preference("model")
        beam_size = preferences.get_preference("beam_size")
        temperature = preferences.get_preference("temperature")
        compression_ratio = preferences.get_preference("compression_ratio")
        chunk_duration = preferences.get_preference("chunk_duration")
        prompt = preferences.get_preference("prompt")

        self.language_combo.setCurrentText(target_language)
        self.model_version.setCurrentText(model)
        self.beam_side_doublespin.setValue(beam_size)
        self.temperature_doublespin.setValue(temperature)
        self.compression_ratio_threshold_spinbox.setValue(compression_ratio)
        self.chunk_duration_spinbox.setValue(chunk_duration)
        self.prompt = prompt

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
        model_size = self.model_version.currentText()

        if input_file == "No file selected":
            self.file_label.setText("Please select a video file!!!")
            return

        # Reset UI for new processing task
        self.progress_bar.setValue(0)
        self.launch_button.setEnabled(False)

        # Determine processing mode
        lang_target = constants.LANGUAGE_CODES[selected_language]
        mode = "translate" if lang_target == "en" else "transcribe"

        beam_size = self.beam_side_doublespin.value()
        temperature = self.temperature_doublespin.value()
        chunk_duration = self.chunk_duration_spinbox.value()
        compression_threshold = (
            self.compression_ratio_threshold_spinbox.value())
        force_new_srt = self.force_new_transcribe_checkbox.isChecked()
        # Start worker thread
        self.worker = thread.TranscriptionWorker(
            file_path=input_file,
            mode=mode,
            model_size=model_size,
            beam_size=beam_size,
            temperature=temperature,
            chunk_duration=chunk_duration,
            target_language=lang_target,
            compression_threshold=compression_threshold,
            prompt=self.prompt,
            force_new_srt=force_new_srt)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.transcription_complete)
        self.worker.start()

    def toggle_settings(self, state):
        self.settings_container.setVisible(state == 2)
        self.adjustSize()

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
            f" Transcription saved at:\n{srt_file}\n "
            f"Time taken: {minutes} min {seconds:.2f} sec"
        )
        msg_box.setIcon(QtWidgets.QMessageBox.Information)
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg_box.exec()


class PromptInputDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Enter Text")
        self.setGeometry(300, 300, 400, 200)

        # Layout
        layout = QtWidgets.QVBoxLayout()

        # Text box with a character limit of 300
        self.text_edit = QtWidgets.QTextEdit(self)
        self.text_edit.setPlainText(constants.PROMPT)
        self.text_edit.textChanged.connect(self.check_character_limit)
        layout.addWidget(self.text_edit)

        # Save button
        self.save_button = QtWidgets.QPushButton("Save")
        self.save_button.clicked.connect(self.save_text)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def check_character_limit(self):
        """
        Ensure the text does not exceed 300 characters.
        """
        text = self.text_edit.toPlainText()
        if len(text) > 300:
            QtWidgets.QMessageBox.warning(
                self, "Limit Exceeded", "Text cannot exceed 400 characters.")
            self.text_edit.moveCursor(self.text_edit.textCursor().End)

    def save_text(self):
        """
        Retrieve and save the text when the user presses 'Save'.
        """
        self.user_text = self.text_edit.toPlainText()
        preferences.set_preference(
            "prompt", self.user_text
        )
        self.prompt = self.user_text
        self.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = VideoTranscriptor()
    window.show()
    sys.exit(app.exec())
