# AI Desktop Assistant

A Windows desktop AI assistant built in Python — controls apps, files, the browser, and (eventually) responds to voice and natural language commands.

## Features

- **System control**: open, close, restart apps; open folders; search installed apps
- **File operations**: create folders, rename, delete, move, and search files
- **Browser control**: open websites, search Google, open known sites (YouTube, GitHub)
- **Voice**: speech-to-text (listen) and text-to-speech (speak)
- **LLM integration** (in progress): natural language understanding via Gemini

## Setup

1. Clone this repo and create a virtual environment:

python -m venv venv
.\venv\Scripts\Activate.ps1


2. Install dependencies:

pip install -r requirements.txt


3. Create a `.env` file in the project root with:

ASSISTANT_NAME=YourAssistantName
GEMINI_API_KEY=your_gemini_api_key


4. **Important — fix the PyAudio bridge** (needed because `PyAudioWPatch` is used instead of `pyaudio` for Python 3.14 compatibility):

python setup_pyaudio_bridge.py


5. Run the assistant:

python main.py


## Project structure

- `main.py` — entry point, chat loop
- `tools/` — action modules (system control, file manager, browser control, voice)
- `utils/` — shared infrastructure (logging, config)
- `llm/` — AI/language understanding (Gemini integration)