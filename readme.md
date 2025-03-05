# Transcripter using FFmpeg and OpenAI-Whisper

This app lets you create .srt files from a video file using openAI's open source Whisper
Several settings are available to tweak the quality of the transcription.

The app will download needed softwares (ffmpeg, PySide6, openAI's whisper, argos_translate and other dependencies)
and install them inside a created venv

# Requirements
Requires python 3.9.5 - 3.9.13
Up to 5Go of free space if you use the large model.
Cuda 12.2 for GPU compute, it will use CPU if no compatible GPU is found