import os
import subprocess
from transcripter import constants

PYTHON_VERSION = "3.9"

print(f"\n Creating {constants.TOOLNAME} Desktop shortcuts...\n")


shortcuts_to_create = [
    constants.TOOLNAME,
]

software_dir = os.path.abspath((os.path.dirname(__file__)))
software_dir = software_dir.lower()
icon_path = f"{software_dir}/transcripter/icons/{constants.TOOLNAME}.ico"


def create_shortcut(shortcut_path, target_path, icon_path=None, python=True):

    create_shortcut_cmd = (
        "$shell = New-Object -comObject WScript.Shell \n"
        f'$shortcut = $shell.CreateShortcut("{shortcut_path}")\n'
        )
    shortcut_args = f'$shortcut.TargetPath = "{target_path}" \n'
    if python:
        shortcut_args = (
            '$shortcut.TargetPath = "py" \n'
            f'$shortcut.Arguments = "-{PYTHON_VERSION} {target_path}" \n'
        )
    create_shortcut_cmd += shortcut_args
    if icon_path:
        create_shortcut_cmd += f'$shortcut.IconLocation = "{icon_path}" \n'
    create_shortcut_cmd += "$shortcut.save()"
    if os.path.exists(shortcut_path):
        os.remove(shortcut_path)
    subprocess.call(["powershell", "-Command", create_shortcut_cmd])


script_path = f"{software_dir}/launcher.py"
home = os.path.expanduser("~")
shortcut_path = f"{home}/Desktop/{constants.TOOLNAME}.lnk"
print(f"   - Adding shortcut for {constants.TOOLNAME}")
create_shortcut(
    shortcut_path=shortcut_path,
    target_path=script_path,
    icon_path=icon_path,
    python=True
    )

close_msg = "\n Press enter to close...\n "
try:
    raw_input(close_msg)
except NameError:
    input(close_msg)
