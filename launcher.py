import os

from transcripter import envs
from transcripter import paths
from transcripter import ffmpeg

TOOLNAME = "dwtranscripter"

def find_py_executable():
    """
    Search for python.exe in common Python installation directories.

    :return: The path to pyw.exe if found, or None if not found.
    """
    base_dirs = [
        # "C:/Program Files/Python39",
        # "C:/Program Files/Python310",
        "C:/Program Files/Python311",
        "C:/Program Files/Python312",
    ]

    for base_dir in base_dirs:
        python_path = os.path.join(base_dir, "python.exe")
        if os.path.exists(python_path):
            return python_path

    print("Installed python.exe not found in common directories.")
    return None


python_executable = find_py_executable()
user_document_dw_path = paths.get_user_dw_documents_dir()
venv_path = os.path.join(
    user_document_dw_path,
    "venvs",
    TOOLNAME
    )
requirements_path = os.path.join(
    paths.get_current_script_dir(),
    "requirements.txt"
    )

transcripter_root = paths.get_current_script_dir()
transcripter_python_module = os.path.dirname(transcripter_root)

# Install ffmpeg and get its path
ffmpeg_path = ffmpeg.install_ffmpeg()


env_vars = {
    "PYTHONPATH": transcripter_python_module,
    "FFMPEG": ffmpeg_path
    }


envs.create_venv(
    venv_path=venv_path,
    requirements_path=requirements_path,
    python_executable=python_executable,
    env_vars=env_vars,
    )

script_path = os.path.join(
    paths.get_user_dw_documents_dir(),
    "transcripter",
    "transcripter",
    "main.py")


envs.run_script_in_venv(
    venv_path=venv_path,
    script_path=script_path,
    show_console=True
    )
