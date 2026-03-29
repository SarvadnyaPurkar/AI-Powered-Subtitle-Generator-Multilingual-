import os
import json
import argparse
# from segment import segment_transcript
from src.subtitle.segment import segment_transcript


# Base paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
TRANSCRIPT_DIR = os.path.join(BASE_DIR, "data", "transcripts")
SUBTITLE_DIR = os.path.join(BASE_DIR, "data", "subtitles")


def get_latest_transcript():
    files = [f for f in os.listdir(TRANSCRIPT_DIR) if f.endswith(".json")]

    if not files:
        return None

    files.sort(key=lambda x: os.path.getmtime(os.path.join(TRANSCRIPT_DIR, x)), reverse=True)
    return files[0]


def format_time(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)

    return f"{hrs:02}:{mins:02}:{secs:02},{millis:03}"


def generate_srt(segments, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, start=1):
            start_time = format_time(seg["start"])
            end_time = format_time(seg["end"])

            f.write(f"{i}\n")
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{seg['text']}\n\n")

    print(f"[INFO] SRT generated: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate subtitles from latest transcript") ; 
    parser.add_argument("--output", type=str, default=None)

    args = parser.parse_args()

    if not os.path.exists(TRANSCRIPT_DIR):
        print("[ERROR] Transcript directory not found")
        return

    transcript_file = get_latest_transcript()

    if transcript_file is None:
        print("[ERROR] No transcript found")
        return

    transcript_path = os.path.join(TRANSCRIPT_DIR, transcript_file)

    with open(transcript_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    segments = segment_transcript(data)

    os.makedirs(SUBTITLE_DIR, exist_ok=True)

    if args.output is None:
        args.output = os.path.splitext(transcript_file)[0] + ".srt"

    output_path = os.path.join(SUBTITLE_DIR, args.output)

    generate_srt(segments, output_path)


if __name__ == "__main__":
    main()