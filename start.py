import subprocess
import sys
import os

def install_requirements():
    if os.name == "posix":
        subprocess.check_call(["sudo", "apt-get", "install", "-y", "portaudio19-dev"])
    elif os.name == "nt":
        print("Vous devez installer ffmpeg.")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

if __name__ == "__main__":
    try:
        import pygame
        import pyvidplayer2
        import imageio_ffmpeg
        import imageio_pyav
    except ImportError:
        install_requirements()
    try:
        subprocess.check_call(["python", "main.py"])
    except:
        subprocess.check_call(["python3", "main.py"])
