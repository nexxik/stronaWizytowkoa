from flask import Flask, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/attached_assets/<path:filename>')
def serve_video(filename):
    return send_file(f'attached_assets/{filename}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)