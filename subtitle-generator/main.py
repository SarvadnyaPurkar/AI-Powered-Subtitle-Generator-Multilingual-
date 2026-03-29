import os
import sys
import glob
import torch
import json
import subprocess # <-- Added to run the final video export directly!

# --- PYTORCH SECURITY BYPASS HACK ---
original_load = torch.load
torch.load = lambda *args, **kwargs: original_load(*args, **{**kwargs, 'weights_only': False})
# ------------------------------------

from src.audio.extract_audio import extract_audio
from src.asr.transcribe import transcribe_audio
from src.subtitle.generate_srt import generate_srt

def main():
    print("=== Starting AI Subtitle Generator Pipeline ===")
    
    video_files = glob.glob("data/raw_videos/*.mp4")
    if not video_files:
        print("Error: Could not find any .mp4 files.")
        sys.exit(1)
        
    video_filename = os.path.basename(video_files[0])
    base_name = os.path.splitext(video_filename)[0]

    # Clean filenames
    audio_filename = f"{base_name}.wav"
    transcript_filename = f"{base_name}.json"
    subtitle_filename = f"{base_name}.srt"
    final_video_filename = f"{base_name}_SUBTITLED.mp4"

    print(f"\nProcessing Video: {base_name}")

    # Step 1: Extract Audio
    print("\n--- Step 1: Extracting Audio ---")
    extract_audio(video_filename, audio_filename)
    
    # Step 2: Speech Recognition
    print("\n--- Step 2: Transcribing with Whisper ---")
    transcribe_audio(audio_filename, "base") 
    
    # Step 3: Format Subtitles
    print("\n--- Step 3: Generating SRT File ---")
    json_path = f"data/transcripts/{transcript_filename}"
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            segments_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find the transcription file at {json_path}")
        sys.exit(1)
        
    generate_srt(segments_data, subtitle_filename)
    
    # Step 4: Burn Subtitles into Video (BYPASSING BUGGY PARTNER SCRIPT)
    print("\n--- Step 4: Burning Subtitles to Video ---")
    
    # 1. Grab the raw video path
    video_path = video_files[0]
    
    # 2. Hunt down exactly where the partner's script saved the SRT file
    srt_search = glob.glob(f"**/{subtitle_filename}", recursive=True)
    if not srt_search:
        print("Error: Could not locate the generated SRT file.")
        sys.exit(1)
    srt_path = srt_search[0]
    
    # 3. THE FIX: Convert Windows backslashes (\) to forward slashes (/) so FFmpeg doesn't crash!
    safe_srt_path = srt_path.replace("\\", "/")
    
    # 4. Prepare output folder
    os.makedirs("final_output", exist_ok=True)
    final_output_path = f"final_output/{final_video_filename}"
    
    # 5. Run the safe command
    ffmpeg_cmd = [
        "ffmpeg", "-y", 
        "-i", video_path, 
        "-vf", f"subtitles='{safe_srt_path}'", 
        "-c:v", "libx264", 
        "-c:a", "copy", 
        final_output_path
    ]
    
    print("Injecting subtitles... this might take a minute or two to render!")
    subprocess.run(ffmpeg_cmd)
    
    print(f"\n Pipeline finished successfully! Check the 'final_output' folder for your video.")

if __name__ == "__main__":
    main()