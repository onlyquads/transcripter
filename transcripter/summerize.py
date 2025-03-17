import re
import os
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "google/pegasus-xsum"

def read_srt_text(file_path):
    """Extracts the text content from an SRT file, ignoring timestamps."""
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.readlines()

    text_lines = []
    for line in content:
        if not re.match(r"^\d+$", line.strip()) and not re.match(r"^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$", line.strip()):
            text_lines.append(line.strip())

    extracted_text = " ".join(text_lines).replace("  ", " ").strip()
    return extracted_text

def summarize_srt(file_path, max_length=3000, min_length=200):
    """Summarizes the extracted text from an SRT file using a pre-trained model and saves it as a .txt file."""
    print("Loading model and tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

    # Extract text from SRT
    text = read_srt_text(file_path)
    print(f"Extracted text length: {len(text)} characters")

    if not text:
        print("No text extracted from the SRT file.")
        return

    # Generate output file path
    base_name = os.path.splitext(file_path)[0]  # Removes .srt extension
    output_txt = f"{base_name}.txt"

    # Check token length
    num_tokens = len(tokenizer.tokenize(text))
    print(f"Number of tokens: {num_tokens}")

    if num_tokens > 1024:
        print("Warning: Input text is too long and will be truncated.")

    # Detect if a GPU is available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    model = model.to(device)

    # Tokenize input
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=1024).to(device)

    print("Generating summary...")
    summary_ids = model.generate(
        inputs.input_ids,
        max_length=max_length,
        min_length=min_length,
        length_penalty=2.0,
        num_beams=4,
    )

    print("Decoding summary...")
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    # Save summary to a text file in the same directory as the .srt
    with open(output_txt, "w", encoding="utf-8") as file:
        file.write(summary)

    print(f"Summary saved to {output_txt}")

    return summary

# Example usage
if __name__ == "__main__":
    srt_file = "your_transcription.srt"  # Change this to your actual SRT file path
    summary = summarize_srt(srt_file)
    print("\nFinal Summary Output:\n", summary)