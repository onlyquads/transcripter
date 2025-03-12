TOOL_VERSION = "b0.2"
TOOLNAME = "transcripter"
TOOL_NICENAME = "Video to srt"

PREFERENCES_FILENAME = "transcripter_prefs.json"
PREFERENCES_DIR_NAME = ".transcripter_prefs"

LANGUAGE_CODES = {
    "English": "en",
    "French": "fr",
    "Dutch": "nl",
    "Spannish": "es",
    "Portuguese": "pt",
    "Italian": "it",
}
SETTING_NAMES_MODEL = ["base", "medium", "large"]
SETTING_NAME_BEAM_SIZE = "Accuracy Level"
SETTING_NAME_TEMPERATURE = "Creativity Level"
SETTING_NAME_COMPRESSION_RATIO = "Noise Reduction"
SETTING_NAME_CHUNK_DURATION = "Chunk Duration"


# DEFAULT VALUES
MODEL = SETTING_NAMES_MODEL[1]
BEAM_SIZE = 0.8
TEMPERATURE = 0.1
COMPRESSION_RATIO = 3.0
CHUNK_DURATION = 300

# These terms are used to add context to the translation.
# There's a character limit estimated to be around 200–300 characters.
PROMPT = """Maya, Blender, Rumba, Houdini, ShotGrid, Toon Boom, TVPaint,
keyframing, blocking, splining, mocap, IK, FK, rig, rigging, retargeting,
render farm, AOVs, EXR, USD, Alembic, compositor, TD, playblast, moodboard,
animatic, storyboard, layout, inbetweening, tweening, pose-to-pose,
straight-ahead, squash & stretch, anticipation, follow-through, overlapping,
ease in/out, onion skinning, cleanup, rough animation, tie-down, X-sheet,
timing chart, cel animation, frame-by-frame, pegbars, vectorization, cut-out,
deformers, symbol animation, multiplane camera.
"""
