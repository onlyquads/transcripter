import os
import time
from PySide6 import QtCore

from transcripter import ffmpeg
from transcripter import subtitles
from transcripter import translate
from transcripter import transcribe
from transcripter import translate


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
        language: str = None,
    ):
        super().__init__()
        self.file_path = file_path
        self.mode = mode
        self.language = language
        self.model_size = model_size
        self.beam_size = beam_size
        self.temperature = temperature
        self.chunk_duration = chunk_duration

    def run(self):
        """
        Executes the transcription process and emits progress signals.
        """
        start_time = time.time()
        self.update_progress(5)

        video_chunks = self.split_video()
        if not video_chunks:
            self.finish("Error: Video chunking failed.", 0)
            return

        temp_srt_files = self.process_chunks(video_chunks)
        final_srt = self.merge_srt_files(temp_srt_files)

        if self.language:
            self.translate_srt(final_srt)

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
        correction_offset = 0.5  # Small delay for synchronization

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
                chunk_start_time=chunk_start_time,
                )

            if chunk_srt:
                temp_srt_files.append(chunk_srt)
            os.remove(chunk)  # Remove chunk after processing

        return temp_srt_files

    def merge_srt_files(self, temp_srt_files: list) -> str:
        """
        Merges temporary SRT files into a final output file.
        """
        self.update_progress(80)
        return subtitles.merge_srt_files(temp_srt_files, self.file_path)

    def translate_srt(self, srt_file: str):
        """
        Translates the SRT file if a language is specified.
        """
        self.update_progress(90)
        # translate.translate_srt(srt_file, self.language)
        print('Launch translation')
        translate.translate_srt(srt_file, self.language)

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
