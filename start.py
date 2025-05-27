import subprocess
import sys
import os

def install_linux_deps():
    print("Installation de portaudio19-dev sur Linux...")
    try:
        subprocess.check_call(["sudo", "apt-get", "install", "-y", "portaudio19-dev"])
    except subprocess.CalledProcessError:
        print("Impossible d'installer portaudio19-dev automatiquement. Veuillez l'installer manuellement.")

def install_windows_deps():
    print("Installation de ffmpeg sur Windows via winget...")
    try:
        subprocess.check_call(["winget", "install", "--silent", "ffmpeg"])
    except subprocess.CalledProcessError:
        print("Impossible d'installer ffmpeg automatiquement via winget. Veuillez l'installer manuellement.")

def install_requirements():
    if os.name == "posix":
        install_linux_deps()
    elif os.name == "nt":
        install_windows_deps()

    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def check_modules():
    try:
        import pygame
        import pyvidplayer2
        import imageio
    except ImportError:
        return False
    return True

if __name__ == "__main__":
    if not check_modules():
        install_requirements()

    import main
