import subprocess
import sys
import os

def install_requirements():
    print("--- Starting Environment Setup ---")

    req_path = os.path.join("backend", "requirements.txt")

    if not os.path.exists(req_path):
        print(f"Error: {req_path} not found.")
        return

    try:
        print(f"Installing requirements from {req_path}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_path])
        print("\n--- Setup Complete Successfully ---")
    except subprocess.CalledProcessError as e:
        print(f"\nError during installation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_requirements()
