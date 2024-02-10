# Audio Interaction System Documentation

## Overview

This project integrates various components for audio interaction, combining Automatic Speech Recognition (ASR) using Whisper by OpenAI, Text-to-Speech (TTS) through Coqui AI, and an AI model for generating responses via Ollama.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Usage](#usage)
5. [Components](#components)
   - [ASR Server (Whisper)](#asr-server-whisper)
   - [TTS Server (Coqui AI)](#tts-server-coqui-ai)
   - [AI Model Server (Ollama)](#ai-model-server-ollama)
6. [Dependencies](#dependencies)

## 1. Prerequisites

- Python (version 3.x)
- Flask
- Requests
- Torch
- Whisper ASR (configured and running) - [Whisper Repository](https://github.com/openai/whisper.git)
- Coqui AI credentials (API key, etc.) - [Coqui AI Repository](https://github.com/coqui-ai/TTS.git)
- TTS library (Coqui AI or other)
- Ollama AI model (configured and running) - [Ollama Repository](https://github.com/ollama/ollama.git)

## 2. Installation

### ASR Server (Whisper)

1. Clone the Whisper repository:

    ```bash
    git clone https://github.com/openai/whisper.git
    ```

2. Follow the installation instructions provided in the [Whisper repository](https://github.com/openai/whisper.git) to set up the ASR server.

### TTS Server (Coqui AI)

1. Clone the TTS repository (Coqui AI):

    ```bash
    git clone https://github.com/coqui-ai/TTS.git
    ```

2. Follow the installation instructions provided in the [Coqui AI repository](https://github.com/coqui-ai/TTS.git) to set up the TTS server.

### AI Model Server (Ollama)

1. Clone the Ollama repository:

    ```bash
    git clone https://github.com/ollama/ollama.git
    ```

2. Follow the installation instructions provided in the [Ollama repository](https://github.com/ollama/ollama.git) to set up the AI model server.

## 3. Configuration

### ASR Server (Whisper)

- Modify the ASR script (`asr_server.py`) to configure the Whisper ASR server URL.

    ```python
    # ASR Server Configuration
    transcription_server_url = "http://your-whisper-server-address:5000/recognize"
    model = whisper.load_model("path/to/whisper-model")
    ```

### TTS Server (Coqui AI)

- Modify the TTS script (`tts_server.py`) to include the correct Coqui AI TTS server URL and API key.

    ```python
    # TTS Server Configuration
    tts_server_url = "http://couqi-ai-server-address:5001/synthesize"
    api_key = "your-coqui-ai-api-key"
    ```

### AI Model Server (Ollama)

- Modify the AI model script (`ollama_server.py`) to include the correct Ollama AI model server URL.

    ```python
    # AI Model Server Configuration
    ai_url = "http://ollama-ai-server-address:5002/api/generate"
    headers = {'Content-Type': 'application/json'}
    ```

## 4. Usage

1. Start the ASR server (Whisper).

    ```bash
    python asr_server.py
    ```

2. Start the TTS server (Coqui AI).

    ```bash
    python tts_server.py
    ```

3. Start the AI model server (Ollama).

    ```bash
    python ollama_server.py
    ```

4. Run the main script for continuous audio processing.

    ```bash
    python continuous_audio_processing.py
    ```

## 5. Components

### ASR Server (Whisper)

The ASR server uses the Whisper library by OpenAI for Automatic Speech Recognition. Ensure that the Whisper model is correctly loaded in the `transcribe_audio` function.

```python
# ASR Server Logic
def transcribe_audio(filename):
    model = whisper.load_model("path/to/whisper-model")
    result = model.transcribe(filename)
    return result["text"]
```

### TTS Server (Coqui AI)

The TTS server uses Coqui AI for Text-to-Speech synthesis. Modify the `synthesize` function in the TTS script based on your TTS server implementation.

```python
# TTS Server Logic
def synthesize():
    # ...
    tts.tts_to_file(text=text_to_speak, file_path=temp_output_file.name)
    # ...
```

### AI Model Server (Ollama)

The AI model server communicates with Ollama for generating responses. Configure the AI model URL and headers in the `generate_response` function.

```python
# AI Model Server Logic
def generate_response(prompt):
    data = {
        "model": "your-ollama-model",
        "stream": False,
        "prompt": prompt,
    }
    # ...
```

## 6. Dependencies

- Flask: Web framework for serving APIs.
- Requests: Library for making HTTP requests.
- Torch: PyTorch library for deep learning.
- TTS: Library for Text-to-Speech synthesis.

Ensure all dependencies are installed, and configurations are set up properly.

Feel free to customize the documentation according to your project's specific requirements, and provide additional details about each component, setup instructions, and any other relevant information.

---

This format presents the information in a more human-readable way, allowing users to follow step-by-step instructions without relying heavily on code blocks. Adjustments can be made based on your preferences and specific project details.
