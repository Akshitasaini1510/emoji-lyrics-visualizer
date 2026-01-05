import whisper
import tempfile

model = whisper.load_model("small")  # keep it fast & realistic

def transcribe_audio(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    result = model.transcribe(
        tmp_path,
        fp16=False,

        # 🔑 critical for music
        condition_on_previous_text=False,
        temperature=0.0,

        # be conservative, avoid hallucinations
        no_speech_threshold=0.0,
        logprob_threshold=-5.0,
        compression_ratio_threshold=2.4,
        best_of=1, beam_size=1

        # DO NOT use best_of / beam search for music
    )

    # ✅ Extract line-level timestamps from segments
    lines = []
    for seg in result["segments"]:
        text = seg["text"].strip()
        if not text:
            continue

        lines.append({
            "start": round(seg["start"], 2),
            "end": round(seg["end"], 2),
            "text": text
        })

    return lines
