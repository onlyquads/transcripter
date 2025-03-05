import os


def merge_srt_files(srt_files, original_video_path):
    """
    Merges multiple SRT files into one final SRT file.

    Parameters:
    - srt_files (list): List of SRT file paths to merge.
    - original_video_path (str): Path to the original video file.

    Returns:
    - str: Path to the final merged SRT file.
    """

    merged_srt_path = os.path.join(
        os.path.dirname(original_video_path),
        f"{os.path.splitext(os.path.basename(original_video_path))[0]}.srt"
    )

    with open(merged_srt_path, "w", encoding="utf-8") as outfile:
        srt_index = 1  # Subtitle numbering

        for srt_file in srt_files:
            with open(srt_file, "r", encoding="utf-8") as infile:
                srt_content = infile.readlines()

            buffer = []  # Store a single subtitle block
            for line in srt_content:
                line = line.strip()

                if line.isdigit():  # Subtitle index
                    if buffer:
                        # Write the previous subtitle before starting a new one
                        outfile.write(
                            f"{srt_index}\n" + "\n".join(buffer) + "\n\n")
                        srt_index += 1
                        buffer = []

                elif "-->" in line:  # Timestamp line
                    buffer.append(line)

                else:
                    buffer.append(line)  # Subtitle text

            # Write last subtitle block of the file
            if buffer:
                outfile.write(f"{srt_index}\n" + "\n".join(buffer) + "\n\n")
                srt_index += 1

    print(f">>> Successfully merged subtitles into: {merged_srt_path}")
    return merged_srt_path
