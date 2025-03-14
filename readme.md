# **Transcripter: Video to SRT using FFmpeg & OpenAI Whisper**

**Transcripter** is a tool that generates **.srt subtitle files** from video files using **OpenAI's Whisper** for transcription. It also supports **translation** via **Argos Translate** to convert subtitles into different languages.

The app provides several settings to fine-tune the **quality and accuracy** of transcriptions.
<p align="center">
<img src="https://github.com/onlyquads/transcripter/blob/master/transcripter/help_images/transcripter_help_02.png?raw=true" alt="App Screenshot" width="150">
</p>

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
2. Run **`create_desktop_shortcut.py`** to create a desktop shortcut, then launch the app from the created icon.
- ⚠️ The first launch may take a few moments while it downloads and installs all dependencies.
   **Alternatively**, you can **run `launcher.py` manually with Python**:

   ```sh
   python launcher.py
   ```

3. Select a movie file, select the target language and Whisper model.
4. If **Force new srt** is checked, it will process the video and transcript it
even if a subtitle already exists. If unchecked and a subtitle exists, it
will go to translate mode only (faster).

>**Notes**:
>- Settings are stored in `/users/USERNAME/.transcripter_prefs`
You can tweak the settings and click on **"save as default"** to keep
those settings for the next session or click on **"reset all"** to reset them default button.
>- Most of the needed package will be installed into `/users/USERNAME/documents/transcripter_venv`
>- Whisper models will be downloaded on request into `/users/USERNAME/.cache`
>- ArgosTranslate models will be downloaded on request into `/users/USERNAME/.local`


### Todo:
- Improve the progress bar feedback
- Add support for macOS
