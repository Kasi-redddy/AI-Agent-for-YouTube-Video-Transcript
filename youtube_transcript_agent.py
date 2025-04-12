import os
import streamlit as st
import yt_dlp
import whisper
from transformers import pipeline
import torch

# Page config
st.set_page_config(page_title="🌍 YouTube Multilingual Transcriber", layout="centered")
st.title("🎧 YouTube Multilingual Transcriber + Summary + Keyword Search")

# Load Whisper model
@st.cache_resource
def load_model():
    return whisper.load_model("medium")

model = load_model()

# Load summarizer
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = load_summarizer()

# Download YouTube audio
def download_audio(url):
    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info['title']
        filename = ydl.prepare_filename(info)
        return os.path.splitext(filename)[0] + ".mp3", title

# Transcribe and detect language
def transcribe(audio_path):
    result = model.transcribe(audio_path, task="transcribe")
    text = result["text"]
    language = result.get("language", "unknown")
    segments = result["segments"]
    return text, language, segments

# Search keywords in segments
def search_segments(segments, keyword):
    matches = []
    for seg in segments:
        if keyword.lower() in seg['text'].lower():
            matches.append((seg['start'], seg['text']))
    return matches

# Summarize text
def summarize(text):
    text = text.replace("\n", " ")
    if len(text) < 100:
        return "Text too short for summarization."
    chunks = []
    chunk_size = 800
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i+chunk_size]
        chunks.append(chunk)
    summary = ""
    for chunk in chunks:
        summarized = summarizer(chunk, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
        summary += summarized + "\n\n"
    return summary.strip()

# App UI
url = st.text_input("Enter YouTube URL:")
if url:
    with st.spinner("Downloading and processing audio..."):
        audio_path, title = download_audio(url)
        text, language, segments = transcribe(audio_path)
        summary = summarize(text)

    st.success(f"✅ Transcription complete! Detected language: **{language.upper()}**")
    st.subheader("📄 Full Transcription")
    st.text_area("Transcript", text, height=300)

    st.subheader("🧠 Summary")
    st.markdown(summary)

    st.subheader("🔍 Keyword Search")
    keyword = st.text_input("Enter keyword to search in transcript:")
    if keyword:
        results = search_segments(segments, keyword)
        if results:
            st.write(f"Found {len(results)} matches:")
            for time, snippet in results:
                st.markdown(f"**[{round(time, 2)}s]** {snippet}")
        else:
            st.warning("No matches found.")
