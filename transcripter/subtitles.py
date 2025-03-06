import os
import paths

from transcripter import translate

def srt_exists(original_video_path):
    dir_name = os.path.dirname(original_video_path)
    video_file_no_ext = os.path.splitext(os.path.basename(original_video_path))[0]

    for lang_code in translate.LANGUAGE_CODES.values():
        subtitle_file_path = os.path.join(
            dir_name, f"{video_file_no_ext}.{lang_code}.srt")
        if os.path.exists(subtitle_file_path):
            print("A subtitle already exists. No transcription process needed")
            return subtitle_file_path
    print("No existing subtitle found.")
    return False



def merge_srt_files(srt_files, original_video_path, target_language):
    """
    Merges multiple SRT files into a single final SRT file.

    Parameters:
    - srt_files (list): List of SRT file paths to merge.
    - original_video_path (str): Path to the original video file.

    Returns:
    - str: Path to the final merged SRT file.
    """

    original_video_base_name, _ = paths.get_filename_without_ext(
        original_video_path)

    merged_srt_path = os.path.join(
        os.path.dirname(original_video_path),
        f"{original_video_base_name}.{target_language}.srt"
    )

    subtitle_index = 1  # Counter for subtitles

    with open(merged_srt_path, "w", encoding="utf-8") as outfile:
        for srt_file in srt_files:
            with open(srt_file, "r", encoding="utf-8") as infile:
                lines = infile.readlines()

            subtitle_block = []

            for line in lines:
                line = line.strip()
                if line.isdigit():  # Subtitle index
                    if subtitle_block:
                        outfile.write(
                            f"{subtitle_index}\n" + "\n".join(subtitle_block) + "\n\n")
                        subtitle_index += 1
                        subtitle_block = []
                elif "-->" in line:  # Timestamp line
                    subtitle_block.append(line)
                else:  # Subtitle text
                    subtitle_block.append(line)

            # Write last subtitle block of the file
            if subtitle_block:
                outfile.write(
                    f"{subtitle_index}\n" + "\n".join(subtitle_block) + "\n\n")
                subtitle_index += 1

    print(f">>> Successfully merged subtitles into: {merged_srt_path}")
    return merged_srt_path
