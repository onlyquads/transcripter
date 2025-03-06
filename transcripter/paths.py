import os


def get_current_script_dir():
    return os.path.dirname(os.path.abspath(__file__))


def get_user_dw_documents_dir():
    return os.path.join(os.path.expanduser("~/Documents"), 'dreamwall')


def get_filename_without_ext(file_path):
    full_filename = os.path.basename(file_path)
    file_dir = os.path.dirname(file_path)
    filename_without_ext = os.path.splitext(full_filename)[0]
    return filename_without_ext, file_dir
