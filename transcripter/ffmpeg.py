import os
import urllib.request
import zipfile
import subprocess


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
                print(f"FFmpeg found at: {ffmpeg_exe_path}")
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
    print(f"Downloading FFmpeg to: {ffmpeg_zip_path}")
    urllib.request.urlretrieve(ffmpeg_url, ffmpeg_zip_path)

    # Extract FFmpeg
    print(f"Extracting FFmpeg to: {ffmpeg_extract_path}")
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
    print(f"Deleting ZIP file: {ffmpeg_zip_path}")
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


# Run the function and get the ffmpeg path
ffmpeg_path = install_ffmpeg()
if ffmpeg_path:
    print(f"FFmpeg is installed at: {ffmpeg_path}")
else:
    print("FFmpeg installation failed.")
