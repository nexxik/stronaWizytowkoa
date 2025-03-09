
import os
import sys
import subprocess

def push_to_github():
    print("=== Push to GitHub ===")
    
    # Check if remote exists
    result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
    has_remote = 'origin' in result.stdout
    
    if not has_remote:
        repo_url = input("Enter your GitHub repository URL (https://github.com/username/repo.git): ")
        subprocess.run(['git', 'remote', 'add', 'origin', repo_url])
        print(f"Remote 'origin' added: {repo_url}")
    
    # Configure Git credentials if needed
    username = input("Enter your GitHub username: ")
    token = input("Enter your GitHub personal access token: ")
    
    # Use credential helper to store credentials temporarily
    os.environ['GIT_ASKPASS'] = 'echo'
    os.environ['GIT_USERNAME'] = username
    os.environ['GIT_PASSWORD'] = token
    
    # Push to GitHub
    print("\nPushing to GitHub...")
    push_result = subprocess.run(
        ['git', 'push', '-u', 'origin', 'main'],
        env=os.environ,
        capture_output=True,
        text=True
    )
    
    if push_result.returncode == 0:
        print("Successfully pushed to GitHub!")
    else:
        print(f"Error pushing to GitHub: {push_result.stderr}")
        
        # Try force push if user wants
        force_push = input("\nWould you like to try force push? (y/n): ")
        if force_push.lower() == 'y':
            force_result = subprocess.run(
                ['git', 'push', '-f', '-u', 'origin', 'main'],
                env=os.environ,
                capture_output=True,
                text=True
            )
            if force_result.returncode == 0:
                print("Successfully force pushed to GitHub!")
            else:
                print(f"Error force pushing to GitHub: {force_result.stderr}")

if __name__ == "__main__":
    push_to_github()
