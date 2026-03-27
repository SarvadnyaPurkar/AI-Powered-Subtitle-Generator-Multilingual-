import ffmpeg
import argparse
import os
import yt_dlp


# Base directories
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
RAW_VIDEO_DIR = os.path.join(BASE_DIR, "data", "raw_videos")
AUDIO_DIR = os.path.join(BASE_DIR, "data", "audio")


def download_youtube_video(url):
    os.makedirs(RAW_VIDEO_DIR, exist_ok=True)

    ydl_opts = {
        'outtmpl': os.path.join(RAW_VIDEO_DIR, '%(title)s.%(ext)s'),
        'format': 'mp4/best',
        'quiet': False
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    print(f"[INFO] Downloaded video: {filename}")
    return os.path.basename(filename)


def extract_audio(input_filename, output_filename):
    input_path = os.path.join(RAW_VIDEO_DIR, input_filename)
    output_path = os.path.join(AUDIO_DIR, output_filename)

    try:
        os.makedirs(AUDIO_DIR, exist_ok=True)

        (
            ffmpeg
            .input(input_path)
            .output(output_path, ac=1, ar='16000')
            .run(overwrite_output=True)
        )

        print(f"[INFO] Audio extracted: {output_path}")

    except Exception as e:
        print(f"[ERROR] {e}")


def main():
    parser = argparse.ArgumentParser(description="Extract audio from video or YouTube") ; 
    parser.add_argument("--input", type=str, default=None) ; 
    parser.add_argument("--youtube_url", type=str, default="https://www.youtube.com/watch?v=qxnKvm3UEsU") ; 
    parser.add_argument("--output", type=str, default=None)

    args = parser.parse_args()

    # Decide input source
    if args.input:
        input_filename = args.input

    elif args.youtube_url:
        input_filename = download_youtube_video(args.youtube_url)

    else:
        print("[ERROR] Provide either --input or --youtube_url")
        return

    # Default output name
    if args.output is None:
        args.output = os.path.splitext(input_filename)[0] + ".wav"

    # Check file exists
    input_path = os.path.join(RAW_VIDEO_DIR, input_filename)
    if not os.path.exists(input_path):
        print(f"[ERROR] File not found: {input_path}")
        return

    extract_audio(input_filename, args.output)


if __name__ == "__main__":
    main()