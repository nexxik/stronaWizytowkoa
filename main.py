from flask import Flask, send_file, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL')

def send_to_discord(ip_address, user_agent):
    if DISCORD_WEBHOOK_URL:
        data = {
            "content": f"🔔 Nowy odwiedzający!\nIP: {ip_address}\nPrzeglądarka: {user_agent}"
        }
        try:
            requests.post(DISCORD_WEBHOOK_URL, json=data)
        except Exception as e:
            print(f"Error sending to Discord: {e}")

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/visitor', methods=['POST'])
def log_visitor():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    send_to_discord(ip, user_agent)
    return jsonify({"status": "ok"})

@app.route('/attached_assets/<path:filename>')
def serve_video(filename):
    return send_file(f'attached_assets/{filename}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)