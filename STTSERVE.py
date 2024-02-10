from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import subprocess
import json
import whisper

app = Flask(__name__)

#Set the path where uploaded audio files will be stored temporarily
UPLOAD_FOLDER = 'upload/folder'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the UPLOAD_FOLDER exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def transcribe_audio(filename):
    # Replace with your whisper model loading and transcribing logic
    model = whisper.load_model("base")
    result = model.transcribe(filename)
    return result["text"]

@app.route('/recognize', methods=['POST'])
def recognize():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    
    if audio_file.filename == '':
        return jsonify({'error': 'No selected audio file'}), 400

    if audio_file:
        # Save the uploaded audio file
        filename = secure_filename(audio_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        audio_file.save(filepath)

        # Perform ASR on the uploaded audio file using your transcribe_audio function
        transcription_result = transcribe_audio(filepath)

        # Return the transcription result
        return jsonify({'transcription': transcription_result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
