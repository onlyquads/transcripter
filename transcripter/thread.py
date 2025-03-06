import os
import time
from PySide6 import QtCore

from transcripter import ffmpeg
from transcripter import subtitles
from transcripter import translate
from transcripter import transcribe



class TranscriptionWorker(QtCore.QThread):
    """
    Worker thread for handling transcription without freezing the UI.
    """
    progress = QtCore.Signal(int)
    finished = QtCore.Signal(str, float)

    def __init__(
        self,
        file_path: str,
        mode: str,
        model_size: str,
        beam_size: int,
        temperature: float,
        chunk_duration: int,
        compression_threshold: float,
        force_new_srt: bool = True,
        target_language: str = None,
    ):
        super().__init__()
        self.file_path = file_path
        self.mode = mode
        self.target_language = target_language
        self.model_size = model_size
        self.beam_size = beam_size
        self.temperature = temperature
        self.compression_threshold = compression_threshold
        self.chunk_duration = chunk_duration
        self.force_new_srt = force_new_srt

    def run(self):
        """
        Executes the transcription process and emits progress signals.
        """
        start_time = time.time()
        self.update_progress(5)
        temp_srt_files = None
        existing_subtitle_file = subtitles.srt_exists(
            original_video_path=self.file_path)

        if not existing_subtitle_file or self.force_new_srt is True:
            video_chunks = self.split_video()
            if not video_chunks:
                self.finish("Error: Video chunking failed.", 0)
                return

            temp_srt_files = self.process_chunks(video_chunks)
            final_srt = self.merge_srt_files(temp_srt_files)

        else:
            # Bypass whisper transcription
            final_srt = existing_subtitle_file

        # if translate.LANGUAGE_CODES.get(self.target_language) != "en":
        self.translate_srt(final_srt)

        if temp_srt_files:
            self.cleanup(temp_srt_files)
        self.finish(final_srt, time.time() - start_time)

    def split_video(self) -> list:
        """
        Splits the video into chunks and returns the list of chunk file paths.
        """
        return ffmpeg.split_video_into_chunks(
            self.file_path, chunk_duration=self.chunk_duration)

    def process_chunks(self, video_chunks: list) -> list:
        """
        Processes video chunks for transcription.
        """
        temp_srt_files = []
        correction_offset = 0.7  # Small delay for synchronization

        for i, chunk in enumerate(video_chunks):
            self.update_progress(10 + int((i / len(video_chunks)) * 60))
            chunk_start_time = (
                i * self.chunk_duration + (correction_offset if i > 0 else 0)
                )
            chunk_srt = transcribe.transcript(
                input_file=chunk,
                mode=self.mode,
                model_size=self.model_size,
                beam_size=self.beam_size,
                temperature=self.temperature,
                compression_ratio_threshold=self.compression_threshold,
                chunk_start_time=chunk_start_time,
                )

            if chunk_srt:
                temp_srt_files.append(chunk_srt)
            os.remove(chunk)

        return temp_srt_files

    def merge_srt_files(self, temp_srt_files: list) -> str:
        """
        Merges temporary SRT files into a final output file.
        """
        self.update_progress(80)
        return subtitles.merge_srt_files(
            temp_srt_files,
            self.file_path,
            self.target_language)

    def translate_srt(self, srt_file: str):
        """
        Translates the SRT file if a language is specified.
        """
        self.update_progress(90)
        print('Launch translation')
        translate.translate_srt(self.file_path, srt_file, self.target_language)

    def cleanup(self, temp_srt_files: list):
        """
        Removes temporary SRT files after processing.
        """
        for temp_srt in temp_srt_files:
            os.remove(temp_srt)

    def update_progress(self, value: int):
        """
        Emits a progress update signal.
        """
        self.progress.emit(value)

    def finish(self, result: str, elapsed_time: float):
        """
        Emits the finished signal with the result and elapsed time.
        """
        self.progress.emit(100)
        self.finished.emit(result, elapsed_time)
