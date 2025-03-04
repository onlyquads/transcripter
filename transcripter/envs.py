'''
Creates a virtual environment locally and manage the run script from venv
'''

import os
import venv
import subprocess


def create_venv(
        venv_path, requirements_path, python_executable=None, env_vars=None):
    """
    Create a Python virtual environment and install packages efficiently.

    :param venv_path: Path to the virtual environment.
    :param requirements_path: Path to the requirements.txt file.
    :param python_executable: Python executable to use for the venv (optional).
    :param env_vars: Dictionary of environment variables (optional).
    """
    print('Installing dreamwall software, please wait...')

    # Check if the virtual environment already exists
    if os.path.exists(venv_path):
        print(f"Virtual environment already exists at: {venv_path}")
    else:
        # Step 1: Create the virtual environment
        print(f"Creating virtual environment at: {venv_path}")
        if python_executable:
            print(f"Using Python executable: {python_executable}")
            subprocess.check_call([python_executable, "-m", "venv", venv_path])
        else:
            builder = venv.EnvBuilder(with_pip=True)
            builder.create(venv_path)

    # Step 2: Set environment variables if provided
    if env_vars:
        print("Setting environment variables:")
        for key, value in env_vars.items():
            os.environ[key] = value
            print(f"{key}={value}")

    # Step 3: Install packages with live progress
    pip_executable = os.path.join(
        venv_path, "Scripts" if os.name == "nt" else "bin", "pip"
    )

    if os.path.exists(requirements_path):
        print(f"Installing packages from: {requirements_path}\n")

        try:
            # Run pip install with real-time output
            process = subprocess.Popen(
                [pip_executable, "install", "-r", requirements_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Print output line by line
            for line in iter(process.stdout.readline, ''):
                print(line.strip())  # Strip to remove extra newlines

            process.wait()

            if process.returncode == 0:
                print("\n Packages installed successfully.")
            else:
                print("\n Package installation failed.")
                print(process.stderr.read())

        except subprocess.CalledProcessError as e:
            print(f"Failed to install packages: {e}")
    else:
        print(f"Requirements file not found: {requirements_path}")


def run_script_in_venv(venv_path, script_path, show_console=False):
    """
    Run a Python script using the virtual environment.

    :param venv_path: The path to the virtual environment.
    :param script_path: The path to the script to be executed.
    :param show_console: Whether to show the console window
    (useful for debugging).
    """

    python_exe = (
        "pythonw.exe" if os.name == "nt" and not show_console else "python.exe")

    python_executable = os.path.join(
        venv_path, "Scripts" if os.name == "nt" else "bin",
        python_exe if os.name == "nt" else "python"
    )

    if not os.path.exists(python_executable):
        print(
            f"[ERROR] Python executable not found in the virtual environment: {python_executable}"
        )
        return

    try:
        print(f"[INFO] Running script: {script_path} using {python_executable}")

        if show_console:
            # Run without capturing output (prints directly in the console)
            subprocess.run([python_executable, script_path], check=True)
        else:
            # Capture output when no console is shown
            result = subprocess.run(
                [python_executable, script_path],
                text=True,
                capture_output=True
            )

            if result.returncode == 0:
                print("[SUCCESS] Script executed successfully.")
            else:
                print(f"[ERROR] Script execution failed with exit code {result.returncode}")
                print(f"[STDOUT] {result.stdout.strip()}")
                print(f"[STDERR] {result.stderr.strip()}")

    except FileNotFoundError:
        print(f"[ERROR] Python executable not found: {python_executable}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to execute the script: {e}")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
