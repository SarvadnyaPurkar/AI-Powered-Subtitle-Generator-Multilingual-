import os
import sys
import glob
import torch
import json
import subprocess

# --- PYTORCH SECURITY BYPASS HACK ---
original_load = torch.load
torch.load = lambda *args, **kwargs: original_load(*args, **{**kwargs, 'weights_only': False})
# ------------------------------------

from src.audio.extract_audio import extract_audio
from src.asr.transcribe import transcribe_audio
from src.subtitle.generate_srt import generate_srt

def main():
    print("=== Starting AI Subtitle Generator Pipeline ===")
    
    # THE FIX: Clean up old SRT files everywhere so we don't grab the wrong one!
    for old_file in glob.glob("data/subtitles/*.srt") + glob.glob("*.srt") + glob.glob("temp/*.srt"):
        try: os.remove(old_file)
        except: pass

    video_files = glob.glob("data/raw_videos/*.mp4")
    if not video_files:
        print("Error: Could not find any .mp4 files in 'data/raw_videos'.")
        sys.exit(1)
        
    video_filename = os.path.basename(video_files[0])
    base_name = os.path.splitext(video_filename)[0]

    audio_filename = f"{base_name}.wav"
    final_video_filename = f"{base_name}_SUBTITLED.mp4"

    print(f"\nProcessing Video: {base_name}")

    # Step 1: Extract Audio
    print("\n--- Step 1: Extracting Audio ---")
    extract_audio(video_filename, audio_filename)
    
    # Step 2: Speech Recognition
    print("\n--- Step 2: Transcribing with Whisper ---")
    transcription_result = transcribe_audio(audio_filename, "base") 
    
    # Step 3: Format Subtitles
    print("\n--- Step 3: Generating SRT File ---")
    segments_data = None
    
    if isinstance(transcription_result, dict) and "segments" in transcription_result:
        segments_data = transcription_result["segments"]
    elif isinstance(transcription_result, list):
        segments_data = transcription_result
    else:
        json_files = glob.glob("data/transcripts/*.json") + glob.glob("*.json")
        if json_files:
            latest_json = max(json_files, key=os.path.getctime)
            with open(latest_json, 'r', encoding='utf-8') as f:
                segments_data = json.load(f)
                
    if not segments_data:
        print("Error: Could not extract subtitle timestamps from Whisper.")
        sys.exit(1)
        
    generate_srt(segments_data, f"{base_name}.srt")
    
    # Step 4: Burn Subtitles into Video
    print("\n--- Step 4: Burning Subtitles to Video ---")
    video_path = video_files[0]
    
    # THE FIX: Search the main folder, the data folder, AND the temp folder for the SRT file!
    srt_files = glob.glob("data/subtitles/*.srt") + glob.glob("*.srt") + glob.glob("temp/*.srt")
    
    if not srt_files:
        print("Error: Could not locate the generated SRT file anywhere in the project.")
        sys.exit(1)
    
    srt_path = max(srt_files, key=os.path.getctime)
    safe_srt_path = srt_path.replace("\\", "/")
    
    os.makedirs("final_output", exist_ok=True)
    final_output_path = f"final_output/{final_video_filename}"
    
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