# Emoji Lyrics Visualizer

A Streamlit-based app that transcribes songs and displays emoji-based, time-synced (line-synced) lyric visuals.

## What it does
- Takes an audio file (mp3 / wav)
- Transcribes lyrics using OpenAi Whisper
- Extracts line-level timestamps
- Converts lyrics into emoji representations with the help of a json map (not all words)
- Displays lyrics(emoji + text) in sync with audio playback

## Why this project
This project explores working with imperfect AI outputs, time-based data, and UI state management, while focusing on visual presentation and raw transcription accuracy.

## Tech Stack
- Python
- Streamlit
- OpenAI Whisper
- NLTK

## Limitations
-Transcription accuracy depends on audio quality. Doesn't transcript well with high music/noise songs.
-emoji mapping is heuristic based, not symantic.Fully dependent on the json map, if the word is not present in json file, it will not change to emoji.
-Timing is line-level, not word-level karaoke sync, due to the unavailiablity of licensed timestamps.

## Possible Improvements
-Improved lyric cleanup, by using music recognition apps.
-Smarter emoji mapping i.e. semantic.
-Support for additional languages. (as of now ASR model cannot hindi songs lyrics)

## How to run locally

### Prerequisites
- Python 3.9+
- FFmpeg installed and available in PATH

### Setup
```bash
pip install -r requirements.txt
python -m streamlit run app.py
