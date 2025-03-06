import os
import torch
import whisper
import tempfile

from transcripter import subtitles

def load_whisper_model(model_size: str = "small"):
    """Loads the Whisper model."""
    return whisper.load_model(model_size)


def transcript(
    input_file,
    mode="transcribe",
    model_size="base",
    language=None,
    beam_size=8,
    temperature=0.1,
    word_timestamps=False,
    fp16=None,
    progress_callback=None,
    chunk_start_time=0,  # New parameter for time offset
    compression_ratio_threshold=2.0,
):
    """
    Transcribes or translates an audio file and generates an SRT file.
    Parameters:
    - input_file (str): Path to the input audio file.
    - mode (str): "translate" (English translation) or "transcribe"
        (original language).
    - model_size (str): Whisper model size to use ("tiny", "base", "small",
        "medium", "large", "large-v2", "large-v3").
    - language (str): Language code (e.g., "fr" for French). If None,
        Whisper auto-detects.
    - beam_size (int): Beam search size for better accuracy.
    - temperature (float): Decoding randomness (0.0 = deterministic,
        higher values allow variations).
    - word_timestamps (bool): Enables word-level timestamps.
    - fp16 (bool): Use mixed precision for faster CUDA inference
        (None = auto-detect).
    - progress_callback (function): Function to update the progress bar in UI.
    - compression_ratio_threshold : lower this if text chunks are too big
    - chunk_start_time (int): The starting timestamp of this chunk in seconds.

    """

    try:
        # Select device (CUDA if available, otherwise CPU)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f'>>> Using device: {device}')

        # Auto-select fp16 based on device
        if fp16 is None:
            fp16 = device == "cuda"

        # Load the specified Whisper model
        print(f">>> Loading Whisper model: {model_size}...")
        print(f">>> using beam_size value: {beam_size}")
        print(f">>> using temperature value: {temperature}")
        print(">>> using compression ratio value: "
              f"{compression_ratio_threshold}")
        model = whisper.load_model(model_size).to(device)

        # Emit progress: model loaded
        if progress_callback:
            progress_callback(5)

        # Transcribe or translate
        print("Transcription in progress...")
        result = model.transcribe(
            input_file,
            task=mode,
            language=language,
            beam_size=beam_size,
            temperature=temperature,
            word_timestamps=word_timestamps,
            fp16=fp16,
            compression_ratio_threshold=compression_ratio_threshold,
        )

        # Emit progress: Transcription started
        if progress_callback:
            progress_callback(20)

        # Convert to SRT format with time adjustments
        srt_content = ""
        total_segments = len(result["segments"])

        for i, segment in enumerate(result["segments"]):
            start_time = segment["start"] + chunk_start_time  # Apply offset
            end_time = segment["end"] + chunk_start_time  # Apply offset
            text = segment["text"]

            # Format timestamps (HH:MM:SS,mmm)
            start_time_srt = (
                f"{int(start_time // 3600):02}:"
                f"{int((start_time % 3600) // 60):02}:"
                f"{int(start_time % 60):02},"
                f"{int((start_time % 1) * 1000):03}"
            )
            end_time_srt = (
                f"{int(end_time // 3600):02}:"
                f"{int((end_time % 3600) // 60):02}:"
                f"{int(end_time % 60):02},"
                f"{int((end_time % 1) * 1000):03}"
            )

            # Append to SRT file format
            srt_content += (
                f"{i+1}\n{start_time_srt} --> {end_time_srt}\n{text}\n\n")

            # Update progress
            if progress_callback:
                progress_callback(int(((i + 1) / total_segments) * 80) + 10)

        # Save as an SRT file in the system's temp folder
        temp_srt_dir = tempfile.gettempdir()
        input_file_name = os.path.basename(input_file)
        input_file_name_without_ext = os.path.splitext(input_file_name)[0]
        srt_file = os.path.join(
            temp_srt_dir, f"{input_file_name_without_ext}.srt")

        srt_file = subtitles.save_srt(srt_file, srt_content)

        # Emit progress: Finalizing
        if progress_callback:
            progress_callback(100)

        return srt_file  # Return path to the generated SRT file

    except Exception as e:
        print(f"Error during transcription: {e}")
        if progress_callback:
            progress_callback(0)  # Reset progress if there's an error
        return None
