
"""
Skrypt pomocniczy do konfiguracji sekretów GitHub OAuth.
Uruchom ten skrypt, aby wprowadzić swoje klucze GitHub.
"""
import os
import json
import subprocess

def main():
    print("=== Konfiguracja GitHub OAuth ===")
    print("Upewnij się, że masz utworzoną aplikację OAuth na GitHub:")
    print("1. Przejdź do https://github.com/settings/applications/new")
    print("2. Zarejestruj nową aplikację")
    print("3. Ustaw Authorization callback URL na: https://twójreplit.repl.co/callback\n")
    
    client_id = input("Podaj GitHub Client ID: ")
    client_secret = input("Podaj GitHub Client Secret: ")
    
    # Pobranie aktulanego URL dla callback
    try:
        current_url = subprocess.check_output(["hostname", "-f"], text=True).strip()
        redirect_uri = f"https://{current_url}/callback"
    except:
        redirect_uri = input("Podaj pełny URL callback (np. https://twójreplit.repl.co/callback): ")
    
    flask_secret = os.urandom(24).hex()
    
    # Przygotowanie komend do ustawienia sekretów
    commands = [
        f"replit secrets set GITHUB_CLIENT_ID={client_id}",
        f"replit secrets set GITHUB_CLIENT_SECRET={client_secret}",
        f"replit secrets set GITHUB_REDIRECT_URI={redirect_uri}",
        f"replit secrets set FLASK_SECRET_KEY={flask_secret}"
    ]
    
    print("\nSkopiuj i wykonaj poniższe komendy w terminalu:")
    for cmd in commands:
        print(cmd)
    
    print("\nMożesz też ręcznie dodać te sekrety w panelu Secrets na Replit")

if __name__ == "__main__":
    main()
