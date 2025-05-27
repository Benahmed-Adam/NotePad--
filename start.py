import subprocess
import sys
import shutil
import platform

try:
    from colorama import init as colorama_init, Fore, Style
    colorama_init()
except ImportError:
    class FallbackColors:
        HEADER = '\033[95m'
        INFO = '\033[94m'
        SUCCESS = '\033[92m'
        WARNING = '\033[93m'
        ERROR = '\033[91m'
        RESET = '\033[0m'
    Fore = FallbackColors()
    Style = FallbackColors()

class Colors:
    HEADER = Fore.MAGENTA
    INFO = Fore.BLUE
    SUCCESS = Fore.GREEN
    WARNING = Fore.YELLOW
    ERROR = Fore.RED
    RESET = Style.RESET_ALL

def print_info(msg):
    print(f"{Colors.INFO}[INFO]{Colors.RESET} {msg}")

def print_success(msg):
    print(f"{Colors.SUCCESS}[OK]{Colors.RESET} {msg}")

def print_warning(msg):
    print(f"{Colors.WARNING}[WARNING]{Colors.RESET} {msg}")

def print_error(msg):
    print(f"{Colors.ERROR}[ERREUR]{Colors.RESET} {msg}")

def run_cmd(cmd, shell=False):
    try:
        subprocess.check_call(cmd, shell=shell)
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Commande échouée: {' '.join(cmd) if isinstance(cmd, list) else cmd}\n{e}")
        return False

def install_system_dependencies():
    system = platform.system()
    print_info(f"Détection système : {system}")

    if system == "Linux":
        pkg_cmd = None
        pkg_mgr = None
        if shutil.which("apt-get"):
            pkg_mgr = "apt-get"
            pkg_cmd = ["sudo", "apt-get", "install", "-y", "portaudio19-dev"]
        elif shutil.which("dnf"):
            pkg_mgr = "dnf"
            pkg_cmd = ["sudo", "dnf", "install", "-y", "portaudio-devel"]
        elif shutil.which("pacman"):
            pkg_mgr = "pacman"
            pkg_cmd = ["sudo", "pacman", "-S", "--noconfirm", "portaudio"]
        elif shutil.which("zypper"):
            pkg_mgr = "zypper"
            pkg_cmd = ["sudo", "zypper", "install", "-y", "portaudio-devel"]
        else:
            print_warning("Gestionnaire de paquets Linux non supporté ou introuvable.")
            print_warning("Veuillez installer manuellement 'portaudio' (ex: portaudio19-dev, portaudio-devel).")
            return False

        print_info(f"Installation de 'portaudio' via {pkg_mgr}...")
        confirmation = input(f"Voulez-vous exécuter : {' '.join(pkg_cmd)} ? [o/N] ").strip().lower()
        if confirmation == "o":
            if not run_cmd(pkg_cmd):
                return False
        else:
            print_warning("Installation des dépendances système annulée par l'utilisateur.")
            return False

    elif system == "Darwin":
        if shutil.which("brew") is None:
            print_warning("Homebrew non trouvé. Veuillez installer Homebrew : https://brew.sh/")
            return False
        brew_cmd = ["brew", "install", "portaudio"]
        print_info("Installation de 'portaudio' via Homebrew...")
        confirmation = input(f"Voulez-vous exécuter : {' '.join(brew_cmd)} ? [o/N] ").strip().lower()
        if confirmation == "o":
            if not run_cmd(brew_cmd):
                return False
        else:
            print_warning("Installation des dépendances système annulée par l'utilisateur.")
            return False

    elif system == "Windows":
        print_info("Sous Windows, il faut installer manuellement 'ffmpeg' et les dépendances nécessaires.")
        print_info("Téléchargez et installez ffmpeg depuis : https://ffmpeg.org/download.html")
        print_info("Assurez-vous que ffmpeg est accessible dans votre PATH.")
        return False

    else:
        print_warning("OS non reconnu. Veuillez installer manuellement les dépendances nécessaires.")
        return False

    return True

def install_python_packages():
    try:
        print_info("Mise à jour de pip...")
        run_cmd([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print_info("Installation des paquets Python depuis requirements.txt...")
        run_cmd([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print_success("Paquets Python installés avec succès.")
        return True
    except Exception as e:
        print_error(f"Erreur lors de l'installation des paquets Python : {e}")
        return False

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
    print_info(f"Lancement de main.py")
    import main

if __name__ == "__main__":
    missing_modules = check_modules()
    if missing_modules:
        print_warning(f"Modules Python manquants détectés : {', '.join(missing_modules)}")
        if not install_system_dependencies():
            print_error("Impossible d'installer les dépendances système. Abandon.")
            sys.exit(1)
        if not install_python_packages():
            print_error("Impossible d'installer les paquets Python. Abandon.")
            sys.exit(1)
    else:
        print_success("Tous les modules Python requis sont installés.")
    launch_main()