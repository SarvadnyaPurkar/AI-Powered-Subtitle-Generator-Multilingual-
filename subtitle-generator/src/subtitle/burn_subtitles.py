import os
import argparse
import subprocess
import shutil
import re


# Base directories
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
VIDEO_DIR = os.path.join(BASE_DIR, "data", "raw_videos")
SUBTITLE_DIR = os.path.join(BASE_DIR, "data", "subtitles")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs", "final_videos")
TEMP_DIR = os.path.join(BASE_DIR, "temp")


def get_latest_file(folder, extension):
    files = [f for f in os.listdir(folder) if f.endswith(extension)]

    if not files:
        return None

    files.sort(key=lambda x: os.path.getmtime(os.path.join(folder, x)), reverse=True)
    return files[0]


def clean_filename(name):
    return re.sub(r'[^\w\-. ]', '_', name)


def prepare_safe_files(video_path, subtitle_path):
    """
    Copy both video and subtitle to temp folder with safe names
    """
    os.makedirs(TEMP_DIR, exist_ok=True)

    safe_video = os.path.join(TEMP_DIR, "temp_video.mp4")
    safe_sub = os.path.join(TEMP_DIR, "temp_subtitles.srt")

    shutil.copy(video_path, safe_video)
    shutil.copy(subtitle_path, safe_sub)

    return safe_video, safe_sub


def burn_subtitles(video_file, subtitle_file, output_file):
    video_path = os.path.join(VIDEO_DIR, video_file)
    subtitle_path = os.path.join(SUBTITLE_DIR, subtitle_file)

    safe_video, safe_sub = prepare_safe_files(video_path, subtitle_path)

    output_path = os.path.join(OUTPUT_DIR, output_file)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    command = [
        "ffmpeg",
        "-i", safe_video,
        "-vf", f"subtitles={safe_sub}",
        "-c:v", "mpeg4",   # change to libx264 later
        "-c:a", "copy",
        output_path
    ]

    try:
        subprocess.run(command, check=True)
        print(f"[INFO] Final video created: {output_path}")

    except subprocess.CalledProcessError as e:
        print("[ERROR] ffmpeg failed")
        print(e)


def main():
    parser = argparse.ArgumentParser(description="Burn subtitles onto video") ; parser.add_argument("--video", type=str, default=None) ; parser.add_argument("--subtitle", type=str, default=None) ; parser.add_argument("--output", type=str, default=None)

    args = parser.parse_args()

    video_file = args.video if args.video else get_latest_file(VIDEO_DIR, ".mp4")
    subtitle_file = args.subtitle if args.subtitle else get_latest_file(SUBTITLE_DIR, ".srt")

    if video_file is None:
        print("[ERROR] No video file found")
        return

    if subtitle_file is None:
        print("[ERROR] No subtitle file found")
        return

    base_name = os.path.splitext(video_file)[0]
    safe_name = clean_filename(base_name)

    if args.output is None:
        output_name = safe_name + "_subtitled.mp4"
    else:
        output_name = args.output

    burn_subtitles(video_file, subtitle_file, output_name)


if __name__ == "__main__":
    main()