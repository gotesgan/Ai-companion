import requests
import subprocess
import os
import json
import time
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106
import RPi.GPIO as GPIO

def do_nothing(obj):
    pass

# Set up the I2C serial interface
serial = i2c(port=1, address=0x3C)

# Choose the SH1106 OLED device
device = sh1106(serial)

# Override the cleanup method
device.cleanup = do_nothing

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(19, GPIO.IN)

# Function to display messages on the OLED screen
def display_message(message_lines):
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, fill="black", outline="white")
        for i, line in enumerate(message_lines):
            draw.text((10, 10 + i * 12), line, fill="white")

# Set up the initial arecord command
duration = 5
output_filename = 'output.wav'
arecord_command = f"arecord -f cd -t wav -d {duration} {output_filename}"

# Update the transcription server URL
transcription_server_url = "http://192.168.29.51:5000/recognize"

# Update the TTS server URL
tts_server_url = "http://192.168.29.51:5001/synthesize"

# AI model URL
ai_url = "https://0382-2405-201-100a-cd-9e85-59ca-d597-45b9.ngrok-free.app"

# Define headers for the AI model request
headers = {'Content-Type': 'application/json'}

# Function to transcribe audio
def transcribe_audio(filename):
    files = {'audio': open(filename, 'rb')}

    try:
        response = requests.post(transcription_server_url, files=files)

        if response.status_code == 200:
            result = response.json()
            transcription_result = result.get('transcription', 'Transcription not available')
            return transcription_result
        else:
            print("Transcription Server Error:", response.status_code, response.text)
            return None
    except Exception as e:
        print("Error during transcription:", str(e))
        return None

# Function to send text to your TTS server and play the resulting audio file
def tts_to_file_and_play(text):
    try:
        # Send text to TTS server
        tts_response = requests.post(tts_server_url, json={"text": text})

        if tts_response.status_code == 200:
            # Save the audio file
            tts_filename = "tts_output.wav"
            with open(tts_filename, "wb") as out_file:
                out_file.write(tts_response.content)

            # Play the generated TTS file
            play_audio(tts_filename)

            return tts_filename
        else:
            print("TTS Server Error:", tts_response.status_code, tts_response.text)
            return None
    except Exception as e:
        print("Error during TTS synthesis:", str(e))
        return None

# Function to generate AI response
def generate_response(prompt):
    data = {
        "model": "tinyllama",
        "stream": False,
        "prompt": prompt,
    }

    try:
        response = requests.post(f"{ai_url}/api/generate", headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            # Parse JSON response
            data = json.loads(response.text)

            # Extract the actual response
            actual_response = data.get("response", "No response available")

            # Display the AI response on the OLED screen
            display_message(["AI Response:", actual_response])

            # Use the AI response for TTS and play the generated TTS file
            tts_filename = tts_to_file_and_play(actual_response)

            return actual_response
        else:
            print("Error:", response.status_code, response.text)
            return None
    except Exception as e:
        print("Error during AI response generation:", str(e))
        return None

# Function to play audio
def play_audio(filename):
    subprocess.run(["aplay", filename])

# Function to delete file
def delete_file(filename):
    try:
        os.remove(filename)
        print(f"Deleted file: {filename}")
    except OSError as e:
        print(f"Error deleting file: {e}")

# Function for continuous audio processing
def continuous_audio_processing():
    while True:
        display_message(["Press GPIO 19 to start recording..."])

        # Wait for GPIO 19 to be pressed
        GPIO.wait_for_edge(19, GPIO.FALLING)
        time.sleep(0.2)  # Add a small delay to debounce the button
        display_message(["Recording..."])

        # Record audio on the client itself
        subprocess.run(arecord_command, shell=True)

        display_message(["Processing..."])

        # Assuming 'output.wav' is the file recorded in Part 1
        transcription_result = transcribe_audio(output_filename)

        if transcription_result is not None:
            display_message(["Transcription:", transcription_result])

            # Use the transcription result as the prompt for the AI model
            ai_response = generate_response(transcription_result)

            if ai_response is not None:
                # Delete the recorded file
                delete_file(output_filename)

        # Display message to indicate waiting for the next press
        display_message(["Press GPIO 19 to start recording..."])

# Call the continuous_audio_processing function to start the main loop
continuous_audio_processing()
