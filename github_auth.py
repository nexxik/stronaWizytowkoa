
import os
import json
import requests
from flask import Flask, request, redirect, session, url_for
from urllib.parse import urlencode

# Ustawienia autoryzacji GitHub
CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID')
CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET')
REDIRECT_URI = os.environ.get('GITHUB_REDIRECT_URI', 'http://localhost:5000/callback')

def configure_github_auth(app):
    app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev_secret_key')
    
    @app.route('/login')
    def login():
        """Rozpocznij proces logowania GitHub"""
        github_auth_url = 'https://github.com/login/oauth/authorize'
        params = {
            'client_id': CLIENT_ID,
            'redirect_uri': REDIRECT_URI,
            'scope': 'read:user'
        }
        auth_url = f"{github_auth_url}?{urlencode(params)}"
        return redirect(auth_url)
    
    @app.route('/callback')
    def callback():
        """Obsługa callback po autoryzacji GitHub"""
        if 'error' in request.args:
            return f"Błąd autoryzacji: {request.args.get('error')}"
        
        code = request.args.get('code')
        token_url = 'https://github.com/login/oauth/access_token'
        payload = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': code,
            'redirect_uri': REDIRECT_URI
        }
        headers = {'Accept': 'application/json'}
        
        # Uzyskanie tokenu dostępu
        token_response = requests.post(token_url, data=payload, headers=headers)
        token_data = token_response.json()
        
        if 'access_token' not in token_data:
            return f"Błąd uzyskiwania tokenu: {json.dumps(token_data)}"
        
        # Zapisanie tokenu w sesji
        access_token = token_data['access_token']
        session['github_token'] = access_token
        
        # Pobranie informacji o użytkowniku
        user_url = 'https://api.github.com/user'
        headers = {
            'Authorization': f'token {access_token}',
            'Accept': 'application/json'
        }
        user_response = requests.get(user_url, headers=headers)
        user_data = user_response.json()
        
        # Zapisanie informacji o użytkowniku w sesji
        session['github_user'] = user_data
        
        return redirect('/')
    
    @app.route('/logout')
    def logout():
        """Wylogowanie użytkownika"""
        session.pop('github_token', None)
        session.pop('github_user', None)
        return redirect('/')
