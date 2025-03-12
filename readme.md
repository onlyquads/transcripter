# **Transcripter: Video to SRT using FFmpeg & OpenAI Whisper**

**Transcripter** is a tool that generates **.srt subtitle files** from video files using **OpenAI's Whisper** for transcription. It also supports **translation** via **Argos Translate** to convert subtitles into different languages.

The app provides several settings to fine-tune the **quality and accuracy** of transcriptions.

<img src="https://github.com/onlyquads/transcripter/tree/master/transcripter/help_images/transcripter_help_02.png" alt="App Screenshot" width="70">

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


3. Select a movie file, select the target language and Whisper model.
4. If Force new srt is checked, it will process the video and transcript it
even if a subtitle already exists. If unchecked and a subtitle exists, it
will go to translate mode only (faster).

Note: Settings are store in /user/USERNAME/.transcripter_prefs
You can tweak the settings and click on 'save as default' to keep
thos settings for the next session.

### Todo:
- Imrpove the progress bar feedback
- Improve translation logic
- Add support for macOS