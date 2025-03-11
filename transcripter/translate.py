import re
import os
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
from argostranslate import package
from argostranslate import translate

from transcripter import paths


# Ensure consistent detection
DetectorFactory.seed = 0


def install_translation_model(from_code="en", to_code="fr"):
    """Ensure the Argos Translate model is installed."""
    try:
        installed = [
            lang.code for lang in translate.get_installed_languages()]
        if from_code in installed and to_code in installed:
            print("Translation model already installed.")
            return

        print(f"Checking for {from_code} -> {to_code} model...")
        package.update_package_index()
        available = package.get_available_packages()

        model = next(
            (p for p in available if p.from_code == from_code and
             p.to_code == to_code), None)

        if not model:
            print(f"No model found for {from_code} -> {to_code}.")
            return

        print(f"Downloading and installing {from_code} -> {to_code}...")
        package.install_from_path(model.download())
        print("Model installed successfully.")

    except Exception as e:
        print(f"Error installing model: {e}")


def detect_language(text):
    """Detect the language of a given text using langdetect."""
    try:
        return detect(text)
    except LangDetectException:
        return "unknown"


def extract_text_for_detection(srt_lines, max_lines=10):
    """
    Extracts a longer sample of subtitle text to improve language detection.
    Skips timecodes and numbers.
    """
    extracted_lines = []
    for line in srt_lines:
        line = line.strip()
        if not line or re.match(r'^\d+$', line) or re.match(
            r'^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', line):
            continue
        extracted_lines.append(line)
        if len(extracted_lines) >= max_lines:
            break
    return " ".join(extracted_lines)


def translate_srt(input_srt, target_language="fr"):
    """
    Translate an SRT file while preserving timestamps and auto-detecting
    the input language. Skips translation if source and target languages
    are the same.
    """

    if target_language == "en":
        return
    with open(input_srt, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Extract text for better language detection
    sample_text = extract_text_for_detection(lines)

    if not sample_text:
        print("No valid text found for language detection.")
        return

    src_lang = detect_language(sample_text)

    print(f"Detected language: {src_lang} -> Translating to: {target_language}")

    if src_lang == target_language:
        print("Source and target languages are the same. Skipping translation.")
        return

    install_translation_model(src_lang, target_language)

    translated = []
    for line in lines:
        if re.match(r'^\d+$', line) or re.match(
                r'^\d{2}:\d{2}:\d{2},\d{3} --> '
                r'\d{2}:\d{2}:\d{2},\d{3}', line):
            translated.append(line)
        elif line.strip() == "":
            translated.append(line)
        else:
            translated.append(
                translate.translate(
                    line.strip(),
                    src_lang,
                    target_language) + "\n"
            )
    file_basename, file_dirname = paths.get_filename_without_ext(input_srt)
    output_srt_filename = f"{file_basename}.{target_language}.srt"
    output_srt = os.path.join(file_dirname, output_srt_filename)

    with open(output_srt, "w", encoding="utf-8") as file:
        file.writelines(translated)

    print(f"Translated SRT saved as {output_srt}")
