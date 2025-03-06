import re
from langdetect import detect
from argostranslate import package
from argostranslate import translate


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
    return detect(text)


def translate_srt(input_srt, tgt_lang="fr"):
    """
    Translate an SRT file while preserving timestamps and auto-detecting
    the input language. Skips translation if source and target languages
    are the same.
    """
    with open(input_srt, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Detect source language from the first non-empty subtitle line
    sample = next((l.strip() for l in lines if l.strip()
                   and not re.match(r'^\d+$', l)
                   and not re.match(
                       r'^\d{2}:\d{2}:\d{2},\d{3} --> '
                       r'\d{2}:\d{2}:\d{2},\d{3}', l)), "English")

    try:
        src_lang = detect_language(sample)
        print(f"Detected language: {src_lang} -> Translating to: {tgt_lang}")
    except Exception as e:
        print(f"Language detection failed: {e}")
        return

    # Skip translation if source and target languages are the same
    if src_lang == tgt_lang:
        print(
            "Source and target languages are the same. Skipping translation.")
        return

    install_translation_model(src_lang, tgt_lang)

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
                translate.translate(line.strip(), src_lang, tgt_lang) + "\n"
            )

    output_srt = input_srt.replace(".srt", f"_{tgt_lang}.srt")
    with open(output_srt, "w", encoding="utf-8") as file:
        file.writelines(translated)

    print(f"Translated SRT saved as {output_srt}")
