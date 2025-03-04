import os


def get_current_script_dir():
    return os.path.dirname(os.path.abspath(__file__))


def get_user_dw_documents_dir():
    return os.path.join(os.path.expanduser("~/Documents"), 'dreamwall')
