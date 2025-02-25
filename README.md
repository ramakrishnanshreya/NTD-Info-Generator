# LLM Powered Voice Assistant for Multimodal Healthcare Data

## Run in Google Colab
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1tlFDV3LEUFrXvnFJ8rGAFnxdhdfJOoAm?usp=sharing)

## Overview
This project implements a multimodal AI assistant that processes both audio and image inputs to provide insightful analyses. The system integrates OpenAI Whisper for speech-to-text conversion, a vision-language model (LLaVA) for image description, and Google Text-to-Speech (gTTS) for generating audio responses.

## Features
- **Speech-to-Text**: Converts spoken input into text using OpenAI Whisper.
- **Image Analysis**: Processes images to generate detailed descriptions using a vision-language model.
- **Multimodal Understanding**: AI responds based on both speech input and image context.
- **Text-to-Speech**: Converts AI-generated responses into audio for better accessibility.
- **Gradio UI**: Provides a user-friendly interface for interaction.

## Installation
Ensure you have Python installed (preferably in a virtual environment) and then install the dependencies:

```bash
pip install -q transformers==4.37.2
pip install bitsandbytes==0.41.3 accelerate==0.25.0
pip install -q git+https://github.com/openai/whisper.git
pip install -q gradio gTTS
```

## Usage
Run the following command to launch the Gradio interface:

```bash
python app.py
```

## Components
### 1. **Speech-to-Text (Whisper)**
- Uses OpenAI Whisper (Medium model) to transcribe voice input.

### 2. **Image Processing (LLaVA)**
- Processes images and extracts meaningful insights based on provided instructions.

### 3. **Text-to-Speech (gTTS)**
- Converts AI-generated responses into audio output.

### 4. **Gradio UI**
- Provides an easy-to-use interface for interacting with the system.

## How It Works
1. User uploads an image and speaks into the microphone.
2. Whisper transcribes the audio input.
3. The image is processed using the LLaVA vision-language model.
4. The AI combines the transcribed text with the image analysis to generate a response.
5. The response is converted to speech and played back to the user.

## File Structure
```
├── app.py                 # Main script to run the application
├── requirements.txt       # Dependencies
├── assets/                # Store images and audio files
├── logs/                  # Logs for debugging
```

## Dependencies
- Python 3.8+
- OpenAI Whisper
- Transformers
- BitsAndBytes
- Accelerate
- Gradio
- gTTS
- PIL (Pillow)
- NLTK
- NumPy
- FFMPEG (for audio processing)



