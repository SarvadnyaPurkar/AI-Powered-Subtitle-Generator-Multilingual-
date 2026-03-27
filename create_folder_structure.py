import os

# Define the folder structure
structure = {
    "subtitle-generator": {
        "data": {
            "raw_videos": [],
            "audio": [],
            "transcripts": [],
            "subtitles": [],
        },
        "src": {
            "audio": ["extract_audio.py"],
            "asr": ["transcribe.py"],
            "nlp": ["refine_text.py"],
            "subtitle": ["segment.py", "generate_srt.py", "burn_subtitles.py"],
            "utils": ["time_utils.py"],
            "__init__.py": None,
        },
        "outputs": {
            "logs": [],
            "final_videos": [],
        },
        "requirements.txt": None,
        "README.md": None,
        "main.py": None,
    }
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        elif isinstance(content, list):
            os.makedirs(path, exist_ok=True)
            for file in content:
                file_path = os.path.join(path, file)
                open(file_path, "w").close()
        elif content is None:
            # Create file directly
            open(path, "w").close()

# Run the script
create_structure(".", structure)
print("Project structure created successfully!")
