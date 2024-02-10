from flask import Flask, request, send_file
import torch
from TTS.api import TTS
import tempfile
import os

app = Flask(__name__)

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Initialize TTS with the desired model and move it to the selected device
tts = TTS(model_name="tts_models/en/ljspeech/speedy-speech", progress_bar=False).to(device)

@app.route('/synthesize', methods=['POST'])
def synthesize():
    try:
        # Get the text from the request
        text_to_speak = request.json["text"]

        # Perform TTS and save the result to a temporary file
        temp_output_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        tts.tts_to_file(text=text_to_speak, file_path=temp_output_file.name)

        # Return the generated audio file
        return send_file(temp_output_file.name, mimetype="audio/wav", as_attachment=True, download_name="output.wav")
    except Exception as e:
        return str(e), 500
    finally:
        # Close and remove the temporary file
        temp_output_file.close()
        os.remove(temp_output_file.name)

if __name__ == '__main__':
    # Run the Flask app on port 5001
    app.run(host='0.0.0.0', port=5001)

