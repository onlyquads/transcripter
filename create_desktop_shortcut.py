import os
import subprocess

TOOL_NAME = "dwtranscripter"
PYTHON_VERSION = "3.9"

print(f"\n Creating {TOOL_NAME} Desktop shortcuts...\n")


shortcuts_to_create = [
    TOOL_NAME,
]

software_dir = os.path.abspath((os.path.dirname(__file__)))
software_dir = software_dir.lower()
icons_dir = f"{software_dir}/transcripter/icons"
remote = " Remote_" if __file__[1] == ":" else ""


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


for app_name in shortcuts_to_create:
    script_path = f"{software_dir}/{app_name}.py"
    start_in = os.path.dirname(script_path)
    home = os.path.expanduser("~")
    shortcut_path = f"{home}/Desktop/{remote}{app_name}.lnk"
    icon_path = f"{icons_dir}/{app_name}.ico"
    print(f"   - Adding shortcut for {app_name}")
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