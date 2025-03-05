import os
import re
from deep_translator import GoogleTranslator


def translate_srt(input_srt, target_lang):
    """
    Translates an SRT file into a target language.

    Args:
        input_srt (str): Path to the original SRT file.
        target_lang (str): Target language code
            (e.g., "fr" for French, "de" for German).

    Returns:
        str: Path to the translated SRT file.
    """

    # Extract base filename and construct output filename
    base_name, _ = os.path.splitext(input_srt)
    output_srt = f"{base_name}_{target_lang}.srt"

    # Read the content of the file for language detection
    with open(input_srt, "r", encoding="utf-8") as file:
        srt_lines = file.readlines()
        # Use first 500 characters for detection
        srt_content = " ".join(srt_lines)[:500]

    # Initialize translator
    translator = GoogleTranslator(source="auto", target=target_lang)

    # Detect language from the file content
    detected_lang = translator.detect(srt_content)

    # If source and target languages are the same, copy file without
    # translation
    if detected_lang == target_lang:
        os.rename(input_srt, output_srt)
        print(f"Source and target languages are the same. File copied: {output_srt}")
        return output_srt

    translated_lines = []
    buffer = []  # Temporary storage for subtitle text lines

    for line in srt_lines:
        line = line.strip()  # Remove extra whitespace

        # If it's a subtitle index or timestamp, keep it unchanged
        if re.match(r"^\d+$", line) or "-->" in line:
            if buffer:  # Translate buffered text before a new subtitle block
                translated_text = translator.translate(" ".join(buffer))
                translated_lines.append(translated_text)
                buffer = []  # Clear buffer

            translated_lines.append(line)  # Keep timestamps/index unchanged
        elif line == "":  # Empty line means end of subtitle block
            if buffer:
                translated_text = translator.translate(" ".join(buffer))
                translated_lines.append(translated_text)
                buffer = []  # Clear buffer
            translated_lines.append("")  # Keep empty line for formatting
        else:
            buffer.append(line)  # Collect subtitle text for translation

    # Write translated SRT file
    with open(output_srt, "w", encoding="utf-8") as file:
        file.write("\n".join(translated_lines))

    # os.remove(input_srt)
    print(f"Translated SRT file saved: {output_srt}")
    return output_srt