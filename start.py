import subprocess
import sys

def install_requirements():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

if __name__ == "__main__":
    try:
        import pygame
        import pyvidplayer2
        import imageio_ffmpeg
        import imageio_pyav
    except ImportError:
        print("aaaaaaaaaaaaaaaaaaaaaaaa")
        install_requirements()

    import main
