import subprocess
import sys
import os

class Colors:
    HEADER = '\033[95m'
    INFO = '\033[94m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    RESET = '\033[0m'

def print_info(msg):
    print(f"{Colors.INFO}[INFO]{Colors.RESET} {msg}")

def print_success(msg):
    print(f"{Colors.SUCCESS}[OK]{Colors.RESET} {msg}")

def print_warning(msg):
    print(f"{Colors.WARNING}[WARNING]{Colors.RESET} {msg}")

def print_error(msg):
    print(f"{Colors.ERROR}[ERREUR]{Colors.RESET} {msg}")

def install_requirements():
    print_info("Installation des dépendances système et Python...")

    if os.name == "posix":
        if shutil.which("apt-get"):
            pkg_mgr = "apt-get"
            install_cmd = ["sudo", "apt-get", "install", "-y", "portaudio19-dev"]
        elif shutil.which("dnf"):
            pkg_mgr = "dnf"
            install_cmd = ["sudo", "dnf", "install", "-y", "portaudio-devel"]
        elif shutil.which("pacman"):
            pkg_mgr = "pacman"
            install_cmd = ["sudo", "pacman", "-S", "--noconfirm", "portaudio"]
        elif shutil.which("zypper"):
            pkg_mgr = "zypper"
            install_cmd = ["sudo", "zypper", "install", "-y", "portaudio-devel"]
        else:
            print_warning("Gestionnaire de paquets Linux non supporté ou introuvable. Installez portaudio manuellement.")
            return

        try:
            print_info(f"Installation de portaudio via {pkg_mgr}...")
            subprocess.check_call(install_cmd)
            print_success("PortAudio installé avec succès.")
        except subprocess.CalledProcessError:
            print_warning(f"Échec de l'installation de PortAudio via {pkg_mgr}. Installez-le manuellement.")
    elif os.name == "nt":
        print_info("Assurez-vous que ffmpeg est installé et dans le PATH.")
        sys.exit()

    try:
        print_info("Mise à jour de pip...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print_info("Installation des paquets depuis requirements.txt...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print_success("Paquets Python installés avec succès.")
    except subprocess.CalledProcessError as e:
        print_error(f"Échec lors de l'installation des paquets Python: {e}")
        sys.exit(1)

def check_modules():
    required_modules = ["pygame", "pyvidplayer2", "imageio_ffmpeg"]
    missing = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    return missing

def launch_main():
    for cmd in ["python", "python3"]:
        try:
            print_info(f"Lancement de main.py avec {cmd}...")
            subprocess.check_call([cmd, "main.py"])
            print_success("main.py exécuté avec succès.")
            return
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    print_error("Impossible de lancer main.py avec python ou python3.")
    sys.exit(1)

if __name__ == "__main__":
    missing_modules = check_modules()
    if missing_modules:
        print_warning(f"Modules manquants détectés : {', '.join(missing_modules)}")
        install_requirements()
    else:
        print_success("Tous les modules requis sont installés.")
    launch_main()
