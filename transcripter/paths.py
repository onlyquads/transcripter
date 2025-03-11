import os
from transcripter import constants


def get_current_script_dir():
    return os.path.dirname(os.path.abspath(__file__))


def get_user_documents_dir():
    return os.path.join(os.path.expanduser("~/Documents"))


def get_filename_without_ext(file_path):
    full_filename = os.path.basename(file_path)
    file_dir = os.path.dirname(file_path)
    filename_without_ext = os.path.splitext(full_filename)[0]
    return filename_without_ext, file_dir


def get_prefs_dir():
    user_documents = get_user_documents_dir()
    return os.path.join(
        user_documents, constants.PREFERENCES_DIR)


def get_prefs_filepath():
    return os.path.join(get_prefs_dir(), constants.PREFERENCES_FILENAME)
