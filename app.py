import streamlit as st
from utils.transcribe import transcribe_audio
from utils.emoji_mapper import map_to_emojis
import base64
# bg-gradient-to-t from-violet-100 via-pink-200 to-orange-100

# ---------- Page Config (must be before other Streamlit calls) ----------
st.set_page_config(page_title="Emoji Lyrics", page_icon="🎶", layout="wide")

# ---------- Soft, aesthetic theme CSS ----------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

:root{
--bg0: #c399ff;  
  --bg1: #ff5c9d;  
  --card: rgba(255, 255, 255, 0.88);
  --card2: rgba(255, 255, 255, 0.70);
  --stroke: rgba(0, 0, 0, 0.06);
  --text: #2b2f38;          
  --muted: rgba(43, 47, 56, 0.65);
  --muted2: rgba(43, 47, 56, 0.45);
  --accent1: #f3b6d8;   /* blush pink */
  --accent2: #d8c7f6;   /* lavender pastel */
  --shadow:  0 18px 55px rgba(43, 47, 56, 0.08);
  --shadow2: 0 12px 30px rgba(43, 47, 56, 0.05);
  --radius: 18px;
}

html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }

.stApp {
  background:
    radial-gradient(
      900px 520px at 12% 8%,
      rgba(193, 158, 255, 1),   /* soft lavender glow */
      transparent 60%
    ),
    radial-gradient(
      820px 500px at 88% 12%,
      rgba(255, 161, 214, 1),   /* blush pink glow */
      transparent 72%
    ),
    linear-gradient(
      180deg,
      rgba(193, 158, 255, 1),   /* lavender white */
      rgba(255, 215, 164, 1)   /* peach white */
    );
  color: var(--text);
}

/* Center + constrain page content */
.block-container{
  padding-top: 2.25rem;
  padding-bottom: 3rem;
  max-width: 980px;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* Headings */
h1, h2, h3{ letter-spacing: -0.02em; }
h1{
  font-weight: 800;
  font-size: 2.2rem;
  margin-bottom: .25rem;
}
.subtle-title{
  color: var(--muted);
  margin-top: 1rem;
  margin-bottom: 1.25rem;
  font-size: 1.09rem;
}

/* Cards */
.card{
  background: linear-gradient(180deg, var(--card), rgba(255,255,255,0.04));
  border: 1px solid var(--stroke);
  border-radius: var(--radius);
  box-shadow: var(--shadow2);
  padding: 18px 18px;
}

.card-glow{
  position: relative;
  overflow: hidden;
  text-align:center;
}
.card-glow:before{
  content:"";
  position:absolute;
  text-align:center;
  inset:-2px;
  z-index: 0;
}
.card-glow > *{ position: relative; z-index: 1; }

/* Audio player container styling */
.audio-wrap{
  display:flex;
  gap: 16px;
  align-items: flex-start;
  justify-content: space-between;
  flex-wrap: wrap;
}
.file-pill{
  display:inline-flex;
  align-items:center;
  gap:10px;
  padding: 10px 12px;
  border-radius: 999px;
  border: 1px solid var(--stroke);
  background: rgba(255,255,255,0.78);
  color: rgb(72, 60, 113);
  font-size: 0.95rem;
  white-space: nowrap;
}
.pill-dot{
  width:10px;height:10px;border-radius:50%;
  background: linear-gradient(135deg, var(--accent1), var(--accent2));
  box-shadow: 0 0 0 4px rgba(124,92,255,0.15);
}

/* Streamlit widgets polish */
.stFileUploader label{
  font-weight: 650 !important;
  color: #2b2f38 !important;
}
.stFileUploader section{
  background: linear-gradient(135deg, rgba(243, 182, 216, 0.08), rgba(216, 199, 246, 0.08)) !important;
  border: 1px solid rgba(243, 182, 216, 0.35) !important;
  border-radius: var(--radius) !important;
  color: #2b2f38 !important;
}

/* Drag & drop helper text */
.stFileUploader section div,
.stFileUploader section span,
.stFileUploader section p {
  color: #2b2f38 !important;
}

/* "Drag and drop file here" */
.stFileUploader section small {
  color: rgba(43, 47, 56, 0.65) !important;
}

/* Uploaded file name */
.stFileUploader [data-testid="stFileUploaderFileName"] {
  color: #2b2f38 !important;
  font-weight: 500;
}

/* File size text */
.stFileUploader [data-testid="stFileUploaderFileSize"] {
  color: rgba(43, 47, 56, 0.55) !important;
}

.stFileUploader section span {
  font-style: italic;
}

.stFileUploader button,
.stFileUploader input[type="file"]::file-selector-button {
  background: linear-gradient(
    135deg,
    #f3b6d8,
    #d8c7f6
  ) !important;
  color: #2b2f38 !important;
  border-radius: 999px !important;
  padding: 10px 18px !important;
  font-weight: 600 !important;

  border: 1px solid rgba(124, 92, 255, 0.25) !important;
  box-shadow: 0 6px 16px rgba(124, 92, 255, 0.12) !important;

  cursor: pointer;
}
.stFileUploader button:hover,
.stFileUploader input[type="file"]::file-selector-button:hover {
  background: linear-gradient(
    135deg,
    #f6c4df,
    #e1d4fb
  ) !important;

  box-shadow: 0 10px 24px rgba(124, 92, 255, 0.18) !important;
  transform: translateY(-2px);
}


/* Emoji lyrics lines */
.lyrics{
  margin-top: 14px;
}
.lyric-line{
  padding: 12px 14px;
  border-radius: 14px;
  border: 1px solid rgba(255,255,255,0.10);
  background: rgba(255,255,255,0.04);
  margin-bottom: 10px;
  display:flex;
  align-items:center;
  justify-content: space-between;
  gap: 14px;
}
.lyric-text{
  font-size: 22px;
  line-height: 1.55;
}
.timecode{
  font-variant-numeric: tabular-nums;
  color: var(--muted2);
  font-size: 0.9rem;
  white-space: nowrap;
}

/* Section titles */
.section-title{
  display:flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 12px;
  margin-top: 6px;
  margin-bottom: 10px;
}
.section-title h2{
  margin: 0;
  font-size: 1.5rem;
  font-weight: 750;
}
.badge{
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid rgba(255,255,255,0.14);
  background: rgba(255,255,255,0.04);
  color: var(--muted);
  font-size: 0.88rem;
}

/* Make audio widget look nicer on dark */
audio{
  width: 100%;
  border-radius: 12px;
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------- Header ----------
st.markdown(
    """
<div class="card-glow" style="padding: 22px 22px;">
  <div style="display:flex; align-items:center; justify-content:center; gap:14px; flex-wrap:wrap;">
    <div>
      <div style="font-size:3rem; font-weight:900; line-height:1.1;font-family:cursive,Lucida Handwriting">Emoji Lyrics Visualizer</div>
      <div class="subtle-title">Upload a song → preview lyrics as emojis.</div>
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# ---------- Uploader Card ----------
st.markdown("""
<style>
div[data-testid="stFileUploader"] {
    padding: 20px;
    border-radius: 18px;
    background: rgba(255,255,255,0.88);
  border: 1px dashed rgba(124,92,255,0.35);
  box-shadow: 0 16px 40px rgba(31,41,55,0.08);
}
</style>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "🎵 Upload a song (mp3 / wav)",
    type=["mp3", "wav"],
)


# ---------- Session State ----------
# if "timed_lines" not in st.session_state:
#     st.session_state.timed_lines = None

if "last_file" not in st.session_state:
    st.session_state.last_file = None

if "timed_lines" not in st.session_state:
    st.session_state.timed_lines = None

# 🔥 THIS is what you were missing
if uploaded_file is not None:
    if uploaded_file.name != st.session_state.last_file:
        st.session_state.last_file = uploaded_file.name
        st.session_state.timed_lines = None




# ---------- Main Flow ----------
if uploaded_file:
    st.markdown(
        """
<div class="section-title">
  <h2>Now Playing</h2>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
<div class="audio-wrap">
  <div class="file-pill"><span class="pill-dot"></span> {uploaded_file.name}</div>
  
</div>
""",
        unsafe_allow_html=True,
    )
    st.write("")
    st.markdown("</div>", unsafe_allow_html=True)

    # Transcribe only once per upload
    if uploaded_file and st.session_state.timed_lines is None:
        with st.spinner("Analyzing song…"):
            raw_lines = transcribe_audio(uploaded_file)

            # convert text
            st.session_state.timed_lines = [
                {"start": line["start"], "end": line["end"], "text": map_to_emojis(line["text"])}
                for line in raw_lines
            ]

# Lyrics Player
import json
import base64

def audio_to_base64(uploaded_file):
    uploaded_file.seek(0)          # 🔑 THIS LINE FIXES IT
    audio_bytes = uploaded_file.read()
    b64 = base64.b64encode(audio_bytes).decode()
    return f"data:audio/mp3;base64,{b64}"


if st.session_state.timed_lines and uploaded_file:
    timed_lines_json = json.dumps(st.session_state.timed_lines)
    audio_src = audio_to_base64(uploaded_file)

    st.components.v1.html(
        f"""
        <style>
        .lyrics-box {{
            background: rgba(255, 255, 255, 0.92);
             backdrop-filter: blur(10px);
             border-radius: 18px;
  border: 1px solid rgba(0,0,0,0.08);
  box-shadow: 0 16px 40px rgba(31,41,55,0.08);
            text-align:center;
            padding: 24px;
            max-height: 200px;
            overflow-y: auto;
            overflow-x:hidden;
            font-size: 30px;
            line-height: 1.8;
            scroll-behavior: smooth;
        }}

        .lyric-line {{
            opacity: 0.2;
            margin: 6px 0;
            color: rgba(31, 41, 55, 0.45); 
            transition: all 0.25s ease;
        }}

        .lyric-line.active {{
            opacity: 1;
            font-weight: 600;
            color: #1f2937;
            transform: scale(1.03);
        }}
        </style>

        <!-- Custom Audio Player -->
       <audio id="player" controls style="width:100%; margin-bottom:20px;">
    <source src="{audio_src}" type="audio/mpeg">
</audio>


        <!-- Lyrics -->
        <div class="lyrics-box" id="lyrics"></div>

        <script>
        const lines = {timed_lines_json};
        const lyricsBox = document.getElementById("lyrics");
        const audio = document.getElementById("player");

        // render lyrics
        lines.forEach((line, i) => {{
            const div = document.createElement("div");
            div.className = "lyric-line";
            div.id = "line-" + i;
            div.textContent = line.text;
            lyricsBox.appendChild(div);
        }});

        function syncLyrics() {{
            const t = audio.currentTime;

            lines.forEach((line, i) => {{
                const el = document.getElementById("line-" + i);

                if (t >= line.start && t < line.end) {{
                    if (!el.classList.contains("active")) {{
                        document
                          .querySelectorAll(".lyric-line.active")
                          .forEach(e => e.classList.remove("active"));

                        el.classList.add("active");
                        el.scrollIntoView({{
                            behavior: "smooth",
                            block: "center"
                        }});
                    }}
                }}
            }});

            requestAnimationFrame(syncLyrics);
        }}

        audio.addEventListener("play", syncLyrics);
        </script>
        """,
        height=550,
    )
