from flask import Flask, send_file, request, jsonify, render_template, session
from flask_cors import CORS
import requests
import os
import json
from github_auth import configure_github_auth

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
configure_github_auth(app)  # Konfiguracja autoryzacji GitHub

DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL')

def send_to_discord(ip_address, user_agent, github_user=None):
    if DISCORD_WEBHOOK_URL:
        content = f"🔔 Nowy odwiedzający!\nIP: {ip_address}\nPrzeglądarka: {user_agent}"
        
        # Dodaj informacje o użytkowniku GitHub, jeśli dostępne
        if github_user:
            content += f"\nGitHub: {github_user.get('login')} ({github_user.get('name')})"
        
        data = {"content": content}
        try:
            requests.post(DISCORD_WEBHOOK_URL, json=data)
        except Exception as e:
            print(f"Error sending to Discord: {e}")

@app.route('/')
def index():
    # Dodaj informacje o użytkowniku GitHub do kontekstu
    github_user = session.get('github_user')
    is_authenticated = 'github_token' in session
    
    # Sprawdź, czy użytkownik jest zalogowany i przekaż te dane do szablonu
    context = {
        'is_authenticated': is_authenticated,
        'github_user': github_user
    }
    
    return render_template('index.html', **context)

@app.route('/visitor', methods=['POST'])
def log_visitor():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    github_user = session.get('github_user')
    
    send_to_discord(ip, user_agent, github_user)
    return jsonify({"status": "ok"})

@app.route('/attached_assets/<path:filename>')
def serve_video(filename):
    return send_file(f'attached_assets/{filename}')

@app.route('/api/user')
def get_user():
    """Endpoint do sprawdzenia zalogowanego użytkownika"""
    if 'github_user' in session:
        return jsonify(session['github_user'])
    return jsonify({"error": "Not authenticated"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)