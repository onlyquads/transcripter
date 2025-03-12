# **Transcripter: Video to SRT using FFmpeg & OpenAI Whisper**

**Transcripter** is a tool that generates **.srt subtitle files** from video files using **OpenAI's Whisper** for transcription. It also supports **translation** via **Argos Translate** to convert subtitles into different languages.

The app provides several settings to fine-tune the **quality and accuracy** of transcriptions.

---

## **Features**
 **Automatic Speech-to-Text**: Converts video audio into text with OpenAI Whisper.
 **SRT Subtitle Generation**: Saves transcriptions in `.srt` format with proper timestamps.
 **Multilingual Support**: Uses Argos Translate to translate subtitles into different languages.
 **Customizable Settings**: Adjust model parameters for optimal transcription quality.
 **Automatic Dependency Installation**: Downloads and sets up required software in a virtual environment.

---

## **Requirements**
- **Python**: minimum `3.9.5`
- **Storage**: Up to **5GB free space** (if using the large Whisper model).
- **GPU Acceleration** (Optional):
  - **CUDA 12.2** required for GPU processing.
  - Falls back to **CPU** if no compatible GPU is detected.
- **Operating System**:
  - **Windows (Supported)**
  - **macOS (Planned Apple Silicon Support)**

---

## **Installation & Usage**

1. **Copy the entire project folder** to any location on your system.
2. **Run `launcher.py` with Python**:

   ```sh
   python launcher.py

### Todo:
- Imrpove the progress bar feedback
- Improve translation logic
- Add support for macOS