# -*- coding: utf-8 -*-
"""Multimodal app for Comprehensiv.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1tlFDV3LEUFrXvnFJ8rGAFnxdhdfJOoAm
"""

!pip install -q transformers==4.37.2
!pip install bitsandbytes==0.41.3 accelerate==0.25.0
!pip install -q git+https://github.com/openai/whisper.git
!pip install -q gradio
!pip install -q gTTS

import torch
from transformers import BitsAndBytesConfig, pipeline

quant_config = BitsAndBytesConfig(
    load_in_4bit = True,
    bnb_4bit_compute_dtype = torch.float16
)

model_id = "llava-hf/llava-1.5-7b-hf"

pipe = pipeline(
    "image-to-text",
    model = model_id,
    model_kwargs = {"quantization_config": quant_config}

)

pipe

import whisper
import gradio as gr
import time
import warnings
import os
from gtts import gTTS
from PIL import Image

image_path = "LF.jpg"

image = Image.open((image_path))

image

import nltk
nltk.download('punkt')
from nltk import sent_tokenize

max_new_tokens = 250

prompt_instructions = """
You will be provided with images related to water sanitation and hygiene and
you need to describe the image focusing on the implications of water stagnation
on diseases.

Remember that if certain aspects are not clear from the image, it's okay to
state "unable to determine based on the provided image."

Now analyze the image and answer the question as described in the structured
manner specified above.

"""

prompt = "User: <image>\n" + prompt_instructions + "\nAssistant:"

output = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": max_new_tokens})

output

for sent in sent_tokenize (output[0]["generated_text"]):
  print(sent)

warnings.filterwarnings("ignore")

import numpy as np

torch.cuda.is_available()

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Using torch {torch.__version__}  ({DEVICE})")

import whisper

model = whisper.load_model("medium", device=DEVICE)

print(
    f"Model is {'multilingual' if model.is_multilingual else 'English-only'}"
    f"and has{sum(np.prod(v.shape) for v in model.parameters()):,} parameters."
)

import re
import datetime

##Logger file
tstamp = datetime.datetime.now()
tstamp = str(tstamp).replace(" ", "_")
logfile = f"log_{tstamp}.txt"

def writehistory(text):
  with open(logfile, "a", encoding='utf-8') as f:
    f.write(text)
    f.write("\n")
  f.close()

import requests

def img2txt(input_text, input_image):

    # load the image
    image = Image.open(input_image)

    writehistory(f"Input text: {input_text} - Type: {type(input_text)} - Dir: {dir(input_text)}")
    if type(input_text) == tuple:
        prompt_instructions = """
        You are an expert optical character recognizer.
        You will be provided with images of IDs and you need to identify the information present in it.
        """
    else:
        prompt_instructions = """
        Act as an expert in imagery descriptive analysis, using as much detail
        as possible from the image, respond to the following prompt:
        """ + input_text

    writehistory(f"prompt_instructions: {prompt_instructions}")
    prompt = "USER: <image>\n" + prompt_instructions + "\nASSISTANT:"

    outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})

    # Properly extract the response text
    if outputs is not None and len(outputs[0]["generated_text"]) > 0:
        match = re.search(r'ASSISTANT:\s*(.*)', outputs[0]["generated_text"])
        if match:
            # Extract the text after "ASSISTANT:"
            reply = match.group(1)
        else:
            reply = "No response found."
    else:
        reply = "No response generated."

    return reply

def transcribe(audio):

    # Check if the audio input is None or empty
    if audio is None or audio == '':
        return ('','',None)  # Return empty strings and None audio file

    # language = 'en'

    audio = whisper.load_audio(audio)
    audio = whisper.pad_or_trim(audio)

    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    _, probs = model.detect_language(mel)

    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)
    result_text = result.text

    return result_text

def text_to_speech(text, file_path):
    language = 'en'

    audioobj = gTTS(text = text,
                    lang = language,
                    slow = False)

    audioobj.save(file_path)

    return file_path

import locale
locale.getpreferredencoding = lambda: "UTF-8"

!ffmpeg -f lavfi -i anullsrc=r=44100:cl=mono -t 10 -q:a 9 -acodec libmp3lame Temp.mp3

import gradio as gr
import base64
import os

# A function to handle audio and image inputs
def process_inputs(audio_path, image_path):
    # Process the audio file (assuming this is handled by a function called 'transcribe')
    speech_to_text_output = transcribe(audio_path)

    # Handle the image input
    if image_path:
        ai_output = img2txt(speech_to_text_output, image_path)
    else:
        ai_output = "No image provided."

    # Assuming 'transcribe' also returns the path to a processed audio file
    processed_audio_path = text_to_speech(ai_output, "Output.mp3")

    return speech_to_text_output, ai_output, processed_audio_path

# Create the interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"),
        gr.Image(type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="AI Output"),
        gr.Audio("Temp.mp3")
    ],
    title="LLM Powered Voice Assistant for Multimodal Healthcare Data",
    description="Upload an image and interact via voice input and audio response."
)

# Launch the interface
iface.launch(debug=True)

