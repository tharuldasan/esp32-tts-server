from flask import Flask, request, Response, abort
import subprocess, tempfile, os

app = Flask(__name__)

@app.route('/')
def index():
    return "ESP32 eSpeak-ng TTS server running!"

@app.route('/say')
def say():
    text = request.args.get('text')
    if not text:
        return abort(400, "Please provide ?text=something")

    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
        wav_path = tmp.name

    subprocess.run(
        ['espeak-ng', '-w', wav_path, text],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    with open(wav_path, 'rb') as f:
        data = f.read()
    os.remove(wav_path)

    resp = Response(data, mimetype='audio/wav')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
