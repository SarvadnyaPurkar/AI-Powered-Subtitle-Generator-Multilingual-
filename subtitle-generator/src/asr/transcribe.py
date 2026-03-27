import whisper
import argparse
import os
import json


# Base directories
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
AUDIO_DIR = os.path.join(BASE_DIR, "data", "audio")
TRANSCRIPT_DIR = os.path.join(BASE_DIR, "data", "transcripts")


def get_latest_audio_file():
    files = [f for f in os.listdir(AUDIO_DIR) if f.endswith(".wav")]

    if not files:
        return None

    # Pick latest file
    files.sort(key=lambda x: os.path.getmtime(os.path.join(AUDIO_DIR, x)), reverse=True)
    return files[0]


def transcribe_audio(input_filename, model_size="base"):
    input_path = os.path.join(AUDIO_DIR, input_filename)

    print(f"[INFO] Using audio file: {input_filename}")
    print("[INFO] Loading Whisper model...")

    model = whisper.load_model(model_size)

    print("[INFO] Transcribing audio...")
    result = model.transcribe(input_path)

    return result


def save_transcript(result, output_filename):
    os.makedirs(TRANSCRIPT_DIR, exist_ok=True)
    output_path = os.path.join(TRANSCRIPT_DIR, output_filename)

    structured_output = []

    for segment in result["segments"]:
        structured_output.append({
            "start": segment["start"],
            "end": segment["end"],
            "text": segment["text"].strip()
        })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(structured_output, f, indent=4)

    print(f"[INFO] Transcript saved: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Auto transcribe latest audio file") ; 
    parser.add_argument("--model", type=str, default="base")

    args = parser.parse_args()

    if not os.path.exists(AUDIO_DIR):
        print("[ERROR] Audio directory not found")
        return

    input_filename = get_latest_audio_file()

    if input_filename is None:
        print("[ERROR] No .wav files found in data/audio/")
        return

    result = transcribe_audio(input_filename, args.model)

    output_filename = os.path.splitext(input_filename)[0] + ".json"
    save_transcript(result, output_filename)


if __name__ == "__main__":
    main()