import json
import os

from transcripter import constants
from transcripter import paths


def load_preferences():
    """Load preferences from the JSON file. Returns an empty dictionary if the file does not exist or is invalid."""

    prefs_filepath = paths.get_prefs_filepath()

    if os.path.exists(prefs_filepath):
        try:
            with open(prefs_filepath, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            print("Error loading preferences. Resetting to empty.")
            return {}
    return {}


def save_preferences(preferences):
    """
    Save preferences to the JSON file. Ensure the file and its directory exist.
    """
    prefs_filepath = paths.get_prefs_filepath()
    os.makedirs(os.path.dirname(prefs_filepath), exist_ok=True)  # Ensure directory exists

    try:
        with open(prefs_filepath, "w", encoding="utf-8") as file:
            json.dump(preferences, file, indent=4)
    except IOError:
        print("Error saving preferences.")

def set_default_preferences():
    """Set default preferences if the file does not exist."""
    if not os.path.exists(paths.get_prefs_filepath()):  # Check if the file exists
        preferences = {
            "target_language": list(constants.LANGUAGE_CODES.keys())[0],
            "model": constants.MODEL,
            "beam_size": constants.BEAM_SIZE,
            "temperature": constants.TEMPERATURE,
            "compression_ratio": constants.COMPRESSION_RATIO,
            "chunk_duration": constants.CHUNK_DURATION,
            "prompt": constants.PROMPT,
        }
        save_preferences(preferences)

def reset_preferences():
    """Reset all preferences to their default values by overwriting the existing file."""
    prefs_filepath = paths.get_prefs_filepath()

    # Delete the file if it exists
    if os.path.exists(prefs_filepath):
        os.remove(prefs_filepath)

    # Recreate with default values
    set_default_preferences()
    print("Preferences have been reset to default.")


def set_preference(key, value):
    """Set a preference and save it."""
    preferences = load_preferences()
    preferences[key] = value
    save_preferences(preferences)


def get_preference(key, default=None):
    """Retrieve a preference. If not found, return the default value."""
    preferences = load_preferences()
    return preferences.get(key, default)


def remove_preference(key):
    """Remove a preference and save the file."""
    preferences = load_preferences()
    if key in preferences:
        del preferences[key]
        save_preferences(preferences)



# # Example usage
# if __name__ == "__main__":
#     set_preference("dark_mode", True)
#     set_preference("download_path", "/home/user/downloads")
#     set_preference("volume_level", 0.8)

#     print(get_preference("dark_mode", False))  # Output: True
#     print(get_preference("download_path", "default_path"))  # Output: /home/user/downloads

#     remove_preference("volume_level")