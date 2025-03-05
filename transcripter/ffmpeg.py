import os
import zipfile
import tempfile
import subprocess
import urllib.request


def get_ffmpeg_path():
    """
    Check if FFmpeg is already installed in the custom path and return
    its path.
    """
    documents_path = os.path.join(os.environ["USERPROFILE"], "Documents")
    ffmpeg_extract_path = os.path.join(
        documents_path, "dreamwall", "transcripter", "ffmpeg")

    if os.path.exists(ffmpeg_extract_path):
        extracted_folders = [
            f for f in os.listdir(ffmpeg_extract_path)
            if f.startswith("ffmpeg-")]
        if extracted_folders:
            ffmpeg_bin_path = os.path.join(
                ffmpeg_extract_path, extracted_folders[0], "bin")
            ffmpeg_exe_path = os.path.join(ffmpeg_bin_path, "ffmpeg.exe")
            if os.path.exists(ffmpeg_exe_path):
                # print(f"FFmpeg found at: {ffmpeg_exe_path}")
                return ffmpeg_exe_path
    return None


def install_ffmpeg():
    """
    Download and install FFmpeg if not already installed, returning its path.
    """
    ffmpeg_exe_path = get_ffmpeg_path()
    if ffmpeg_exe_path:
        return ffmpeg_exe_path  # FFmpeg is already installed

    print("FFmpeg not found. Proceeding with installation...")

    # Define installation paths
    documents_path = os.path.join(os.environ["USERPROFILE"], "Documents")
    dreamwall_path = os.path.join(documents_path, "dreamwall", "transcripter")
    ffmpeg_zip_path = os.path.join(dreamwall_path, "ffmpeg.zip")
    ffmpeg_extract_path = os.path.join(dreamwall_path, "ffmpeg")

    # Ensure installation directories exist
    os.makedirs(dreamwall_path, exist_ok=True)

    # Define FFmpeg download URL
    ffmpeg_url = (
        "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip")

    # Download FFmpeg
    # print(f"Downloading FFmpeg to: {ffmpeg_zip_path}")
    urllib.request.urlretrieve(ffmpeg_url, ffmpeg_zip_path)

    # Extract FFmpeg
    # print(f"Extracting FFmpeg to: {ffmpeg_extract_path}")
    with zipfile.ZipFile(ffmpeg_zip_path, 'r') as zip_ref:
        zip_ref.extractall(ffmpeg_extract_path)

    # Locate extracted FFmpeg folder
    extracted_folders = [
        f for f in os.listdir(ffmpeg_extract_path) if f.startswith("ffmpeg-")]
    if not extracted_folders:
        print("Error: FFmpeg extraction failed.")
        return None

    ffmpeg_bin_path = os.path.join(
        ffmpeg_extract_path, extracted_folders[0], "bin")
    ffmpeg_exe_path = os.path.join(ffmpeg_bin_path, "ffmpeg.exe")

    # Delete ZIP file after extraction
    # print(f"Deleting ZIP file: {ffmpeg_zip_path}")
    os.remove(ffmpeg_zip_path)

    # Verify installation
    print("Verifying FFmpeg installation...")
    try:
        result = subprocess.run(
            [ffmpeg_exe_path, "-version"],
            capture_output=True,
            text=True,
            check=True)
        print("FFmpeg installation successful.")
        return ffmpeg_exe_path
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("FFmpeg installation failed.")
        return None


def split_video_into_chunks(input_video, chunk_duration=400):
    """
    Splits a video into smaller chunks (default: 15 minutes max per chunk)
    and stores them in the Windows temp folder.

    Parameters:
    - input_video (str): Path to the input video file.
    - chunk_duration (int): Maximum duration per chunk in seconds
    (default: 400s = 5 minutes).

    Returns:
    - List of chunked video file paths stored in the temp folder.
    """

    ffmpeg_path = os.environ.get("FFMPEG")
    if not ffmpeg_path or not os.path.exists(ffmpeg_path):
        raise FileNotFoundError("FFmpeg not found! Ensure FFmpeg is installed and set in environment variables.")

    print(f'>>> FFMPEG FOUND {ffmpeg_path}')
    os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_path)
    os.environ["FFMPEG_BINARY"] = ffmpeg_path  # Ensure Whisper can access FFmpeg

    # Get system temp folder
    temp_dir = tempfile.gettempdir()

    # Extract filename and extension
    input_file_name = os.path.basename(input_video)
    input_file_name_without_ext, ext = os.path.splitext(input_file_name)

    # Define output file pattern inside temp folder
    output_pattern = os.path.join(
        temp_dir, f"{input_file_name_without_ext}_chunk_%03d{ext}")




    # FFmpeg command to split the video
    command = [
        ffmpeg_path,
        "-i", input_video,          # Input file
        "-c", "copy",               # Keep original quality
        "-map", "0",                # Copy all streams (audio, video)
        "-f", "segment",            # Enable segmenting
        "-segment_time", str(chunk_duration),  # Split every 900s (15min)
        "-copyts",  # Preserve original timestamps
        output_pattern              # Output file pattern
    ]

    try:
        print(
            f">>> Splitting {input_video} into 15-minute chunks in TEMP folder...")
        subprocess.run(command, check=True)

        # Collect chunked files
        chunk_files = sorted([
            os.path.join(temp_dir, f)
            for f in os.listdir(temp_dir)
            if f.startswith(f"{input_file_name_without_ext}_chunk_") and f.endswith(ext)
        ])

        print(
            f">>> Successfully created {len(chunk_files)} chunks in {temp_dir}.")
        return chunk_files

    except subprocess.CalledProcessError as e:
        print(f"Error splitting video: {e}")
        return []