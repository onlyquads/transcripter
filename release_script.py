import os
import sys
import platform
import subprocess

from transcripter  import paths

SOURCE = os.path.dirname(paths.get_current_script_dir())
# DESTINATION = "C:/Users/ngaadmin/Documents/dreamwall/transcripter"
DESTINATION = "C:/Users/NicolasG/Documents/dreamwall/transcripter"

# Files to exclude
EXCLUDED_FILES = [
    "credentials.json",
    "token.pickle",
    "*.pyc",
    "user_preferences.json",
    "test.py",
    "uninstall.py",
    "release_script.py",
    ".gitignore"

]

# Directories to exclude
EXCLUDED_DIRS = [
    "__pycache__",
    ".git",
    "prefs",
]

# Exclude FFmpeg directory (preserve it)
FFMPEG_DIR = "ffmpeg"  # Folder name inside destination
EXCLUDED_DIRS.append(FFMPEG_DIR)  # Add it to exclusion list

# Convert lists to robocopy arguments (Windows)
ROBOCOPY_ARGS = [
    "/mir",  # Mirror directories
    "/sl",  # Copy symbolic links
]
for file in EXCLUDED_FILES:
    ROBOCOPY_ARGS += ["/xf", file]

for directory in EXCLUDED_DIRS:
    ROBOCOPY_ARGS += ["/xd", directory]  # Exclude directories


def copy_folder(verbose=False):
    source = SOURCE
    destination = DESTINATION

    try:
        if platform.system() == "Windows":
            # Construct robocopy command
            command = ["robocopy", source, destination] + ROBOCOPY_ARGS
            command.extend("/njh /njs".split())  # Hide job header
            if not verbose:
                # Suppress file logging
                command.extend("/nfl /ndl /nc /ns /np".split())

            subprocess.call(command)
            print("Released successfully (FFmpeg folder preserved).")

        elif platform.system() == "Linux":
            # Convert lists to rsync arguments
            rsync_exclude_args = []
            for file in EXCLUDED_FILES:
                rsync_exclude_args += ["--exclude", file]
            for directory in EXCLUDED_DIRS:
                rsync_exclude_args += ["--exclude", directory]

            # Construct rsync command
            command = [
                "rsync",
                "--recursive",
                "--delete",
            ] + rsync_exclude_args + [source, os.path.dirname(destination)]

            subprocess.call(command)
            print("Released successfully (FFmpeg folder preserved).")

    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")


def launch_with_debug(script_path):
    python_executable = sys.executable  # Gets the correct Python executable
    args = ["--debug"]
    # args = None

    # Properly quote the paths to handle spaces in directories
    if args:
        command = (
            f'cmd.exe /c ""{python_executable}" "{script_path}" {" ".join(args)}"')
    else:
        command = f'cmd.exe /c ""{python_executable}" "{script_path}""'

    # Run the command
    subprocess.run(command, shell=True)


copy_folder()
