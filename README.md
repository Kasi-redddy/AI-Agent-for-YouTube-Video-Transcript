# AI-Agent-for-YouTube-Video-Transcript

A Streamlit app that allows users to:

🔊 Download and transcribe YouTube video audio using OpenAI's Whisper

🌍 Automatically detect and transcribe in multiple languages

📝 Display full transcription

🧠 Generate a summary using HuggingFace Transformers

🔍 Search keywords in the transcript with timestamps


🔧 Features

🎥 Download audio from YouTube using yt-dlp

🧠 Transcribe in 50+ languages

📌 Automatic language detection

📃 Full transcript viewer

✂️ Smart summarization with HuggingFace BART model

🔍 Keyword search with timestamps

🖥️ Simple Streamlit UI

🛠️ Installation Steps

Clone the repository:

bash
Copy
Edit
git clone https://github.com/your-username/youtube-multilingual-transcriber.git
cd youtube-multilingual-transcriber
Create and activate a virtual environment (recommended):

bash
Copy
Edit
conda create -n youtube_agent_env python=3.9
conda activate youtube_agent_env
or with venv:

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt

▶️ How to Run
bash
Copy
Edit
streamlit run youtube_transcript_agent.py
Then open http://localhost:8501 in your browser.

🧠 Tech Stack
Whisper – Speech-to-text

HuggingFace Transformers – Summarization

yt-dlp – YouTube audio download

Streamlit – Frontend interface
