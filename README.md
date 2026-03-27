# AI-Powered Subtitle Generator (Multilingual)

## 1. Overview

This project implements an end-to-end pipeline for automatic subtitle generation from video content. It combines speech recognition, lightweight natural language processing, and optional machine translation to produce synchronized and readable subtitles.

The system is designed to demonstrate how real-world subtitle generation pipelines operate while remaining modular, interpretable, and feasible to implement within a short development cycle.

The pipeline processes a video file, extracts audio, generates a time-aligned transcript, refines the text, converts it into subtitle format, and optionally embeds the subtitles back into the video.

---

## 2. Objectives

The primary objectives of this project are:

* To design a modular pipeline for subtitle generation
* To utilize pretrained speech recognition models for transcription
* To improve transcription readability using basic NLP techniques
* To generate standard subtitle files (SRT format)
* To optionally support multilingual subtitle generation
* To integrate subtitles into video files

---

## 3. System Architecture

The system follows a sequential pipeline architecture:

```
Video Input
   ↓
Audio Extraction
   ↓
Speech Recognition (ASR)
   ↓
Text Post-processing
   ↓
Subtitle Generation (SRT)
   ↓
(Optional) Translation
   ↓
(Optional) Subtitle Embedding
```

Each stage is implemented as an independent module, enabling easy debugging, testing, and future extensions.

---

## 4. Project Structure

```
subtitle-generator/
│
├── data/
│   ├── input/
│   │   └── input_video.mp4
│   │
│   ├── audio/
│   │   └── audio.wav
│   │
│   ├── transcripts/
│   │   └── raw_transcript.json
│   │
│   ├── subtitles/
│   │   ├── subtitles_en.srt
│   │   └── subtitles_translated.srt
│   │
│   └── output/
│       └── output_video.mp4
│
├── src/
│   ├── audio/
│   │   └── extract_audio.py
│   │
│   ├── asr/
│   │   └── transcribe.py
│   │
│   ├── nlp/
│   │   └── refine_text.py
│   │
│   ├── subtitles/
│   │   └── generate_srt.py
|   |   └──segment.py
|   |   └──burn_subtitle.py
│   │
│   ├── translation/
│   │   └── translate.py
│   │
│   ├── video/
│   │   └── embed_subtitles.py
│   │
│   └── main.py
│
├── requirements.txt
├── README.md
└── config.py
```

---

## 5. Module Descriptions

### 5.1 Audio Extraction (`src/audio/extract_audio.py`)

This module extracts audio from the input video file and converts it into a standardized format suitable for speech recognition.

**Responsibilities:**

* Accept video input (MP4, MKV, AVI)
* Extract audio using FFmpeg
* Convert audio to:

  * Mono channel
  * 16 kHz sampling rate
  * WAV format

**Output:**

```
data/audio/audio.wav
```

---

### 5.2 Speech Recognition (`src/asr/transcribe.py`)

This module performs automatic speech recognition using a pretrained model.

**Responsibilities:**

* Load Whisper (or faster-whisper) model
* Process audio file
* Generate:

  * Transcribed text
  * Timestamped segments

**Output Format (JSON):**

```json
[
  {
    "start": 62.0,
    "end": 65.0,
    "text": "i cant believe this"
  }
]
```

**Output File:**

```
data/transcripts/raw_transcript.json
```

---

### 5.3 Text Post-processing (`src/nlp/text_cleaner.py`)

This module improves the readability of raw ASR output.

**Responsibilities:**

* Capitalize sentences
* Fix punctuation
* Remove filler words (optional)
* Normalize spacing

**Approach:**

* Rule-based processing (regular expressions)
* No heavy NLP models to keep system lightweight

**Output:**
Cleaned transcript stored in memory or file

---

### 5.4 Subtitle Generation (`src/subtitles/generate_srt.py`)

This module converts processed transcripts into subtitle format.

**Responsibilities:**

* Convert timestamps into SRT format
* Split long sentences into readable chunks
* Ensure:

  * Maximum 2 lines per subtitle
  * Reasonable reading speed

**Output Example:**

```
1
00:01:02,000 --> 00:01:05,000
I can't believe this.
```

**Output File:**

```
data/subtitles/subtitles_en.srt
```

---

### 5.5 Translation (`src/translation/translate.py`) [Optional]

This module translates subtitles into another language.

**Responsibilities:**

* Load translation model or API
* Translate subtitle text while preserving timestamps

**Recommended Models:**

* MarianMT (HuggingFace)
* External APIs (if allowed)

**Output File:**

```
data/subtitles/subtitles_translated.srt
```

---

### 5.6 Subtitle Embedding (`src/video/embed_subtitles.py`) [Optional]

This module integrates subtitles into the video.

**Modes:**

1. Soft subtitles (recommended)
2. Hard subtitles (burned into video)

**Responsibilities:**

* Use FFmpeg to:

  * Add subtitle tracks
  * Preserve video quality

**Output File:**

```
data/output/output_video.mp4
```

---

### 5.7 Main Pipeline (`src/main.py`)

This is the entry point of the application.

**Responsibilities:**

* Orchestrate the full pipeline:

  1. Extract audio
  2. Run ASR
  3. Clean text
  4. Generate subtitles
  5. (Optional) Translate
  6. (Optional) Embed subtitles

**Example Execution Flow:**

```python
if __name__ == "__main__":
    extract_audio()
    transcribe()
    clean_text()
    generate_srt()
    translate()
    embed_subtitles()
```

---

## 6. Installation

### 6.1 Clone Repository

```
git clone <repository_url>
cd subtitle-generator
```

### 6.2 Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate   # Windows
```

### 6.3 Install Dependencies

```
pip install -r requirements.txt
```

---

## 7. Requirements

Example `requirements.txt`:

```
ffmpeg-python
openai-whisper
faster-whisper
transformers
torch
numpy
pandas
```

Ensure FFmpeg is installed and available in system PATH.

---

## 8. Usage

### Step 1: Place Input Video

```
data/input/input_video.mp4
```

### Step 2: Run Pipeline

```
python src/main.py
```

### Step 3: Outputs

* Audio: `data/audio/audio.wav`
* Transcript: `data/transcripts/raw_transcript.json`
* Subtitles: `data/subtitles/*.srt`
* Final video: `data/output/output_video.mp4`

---

## 9. Design Choices

### Use of Pretrained Models

The system uses pretrained ASR models to avoid the complexity of training from scratch while ensuring high accuracy.

### Modular Architecture

Each subsystem is implemented independently, allowing:

* Easy debugging
* Replacement of components
* Scalability

### Lightweight NLP

Text processing is intentionally simple to ensure fast execution and minimal dependencies.

---

## 10. Limitations

* Accuracy depends on ASR model quality
* No speaker diarization
* Limited context awareness in translation
* No real-time processing
* Subtitle segmentation is heuristic-based

---

## 11. Future Improvements

* Speaker identification (diarization)
* Real-time subtitle generation
* Advanced punctuation models
* Confidence-based subtitle filtering
* UI or web interface
* Multi-language support beyond one target language

---

## 12. Conclusion

This project demonstrates a practical implementation of an AI-driven subtitle generation system. While simplified, it captures the essential components of real-world pipelines, including audio processing, speech recognition, text refinement, and subtitle formatting.

The modular design allows further enhancements and serves as a strong foundation for more advanced research or production-level systems.

---
