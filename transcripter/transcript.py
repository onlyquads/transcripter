import os
import whisper


def transcript(input_file, mode="translate", progress_callback=None):
    """
    Transcribes or translates an audio file and generates an SRT file.

    mode:
        - "translate" (English translation)
        - "transcribe" (original language)
    progress_callback: Function to update the progress bar in UI.
    """

    # Manually set the FFmpeg path
    ffmpeg_path = os.environ["FFMPEG"]
    if not os.path.exists(ffmpeg_path):
        raise FileNotFoundError(
            "FFmpeg not found! Ensure FFmpeg is installed.")

    print(f'>>> FFMPEG FOUND {ffmpeg_path}')
    os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_path)

    # Ensure Whisper can access FFmpeg
    os.environ["FFMPEG_BINARY"] = ffmpeg_path

    try:
        # Load the Whisper model
        model = whisper.load_model("base")

        # Emit progress to indicate model is loaded
        if progress_callback:
            progress_callback(5)  # Set progress to 5% (model loading done)

        # Transcribe or Translate
        result = model.transcribe(input_file, task=mode)

        # Emit progress (Transcription started)
        if progress_callback:
            progress_callback(20)

        # Convert transcription to SRT format
        srt_content = ""
        total_segments = len(result["segments"])

        for i, segment in enumerate(result["segments"]):
            start_time = segment["start"]
            end_time = segment["end"]
            text = segment["text"]

            # Format timestamps (HH:MM:SS,mmm)
            start_time_srt = f"{int(start_time // 3600):02}:{int((start_time % 3600) // 60):02}:{int(start_time % 60):02},{int((start_time % 1) * 1000):03}"
            end_time_srt = f"{int(end_time // 3600):02}:{int((end_time % 3600) // 60):02}:{int(end_time % 60):02},{int((end_time % 1) * 1000):03}"

            # Append to SRT file format
            srt_content += f"{i+1}\n{start_time_srt} --> {end_time_srt}\n{text}\n\n"

            # Update progress (Based on segment processing)
            if progress_callback:
                progress_callback(int(((i + 1) / total_segments) * 80) + 10)


        # Save as an SRT file
        parent_dir = os.path.dirname(input_file)
        input_file_name = os.path.basename(input_file)
        input_file_name_without_ext = os.path.splitext(input_file_name)[0]
        srt_file = f"{parent_dir}/{input_file_name_without_ext}.srt"

        if mode == "translate":
            srt_file = f"{parent_dir}/{input_file_name_without_ext}_en.srt"

        print(f"Translated SRT file created: {srt_file}")

        with open(srt_file, "w", encoding="utf-8") as f:
            f.write(srt_content)

        # Emit progress (Finalizing)
        if progress_callback:
            progress_callback(100)

        return srt_file

    except Exception as e:
        print(f"Error during transcription: {e}")
        if progress_callback:
            progress_callback(0)  # Reset progress if there's an error
        return None
