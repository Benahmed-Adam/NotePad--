import subprocess
import sys
import shutil
import platform

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
    print(f"{Colors.ERROR}[ERROR]{Colors.RESET} {msg}")

def run_cmd(cmd, shell=False):
    try:
        subprocess.check_call(cmd, shell=shell)
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed: {' '.join(cmd) if isinstance(cmd, list) else cmd}\n{e}")
        return False

def install_system_dependencies():
    system = platform.system()
    print_info(f"System detected: {system}")

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
            print_warning("Unsupported or unknown Linux package manager.")
            print_warning("Please install 'portaudio' manually (e.g., portaudio19-dev, portaudio-devel).")
            return False

        print_info(f"Installing 'portaudio' via {pkg_mgr}...")
        confirmation = input(f"Do you want to execute: {' '.join(pkg_cmd)} ? [y/N] ").strip().lower()
        if confirmation == "y":
            if not run_cmd(pkg_cmd):
                return False
        else:
            print_warning("System dependency installation aborted by user.")
            return False

    elif system == "Darwin":
        if shutil.which("brew") is None:
            print_warning("Homebrew not found. Please install Homebrew: https://brew.sh/")
            return False
        brew_cmd = ["brew", "install", "portaudio"]
        print_info("Installing 'portaudio' via Homebrew...")
        confirmation = input(f"Do you want to execute: {' '.join(brew_cmd)} ? [y/N] ").strip().lower()
        if confirmation == "y":
            if not run_cmd(brew_cmd):
                return False
        else:
            print_warning("System dependency installation aborted by user.")
            return False

    elif system == "Windows":
        print_info("On Windows, 'ffmpeg' and other dependencies must be installed manually.")
        print_info("Download and install ffmpeg from: https://ffmpeg.org/download.html")
        print_info("Make sure ffmpeg is added to your PATH.")
        return False

    else:
        print_warning("Unrecognized OS. Please install the necessary dependencies manually.")
        return False

    return True

def install_python_packages():
    try:
        print_info("Upgrading pip...")
        run_cmd([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print_info("Installing Python packages from requirements.txt...")
        run_cmd([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print_success("Python packages installed successfully.")
        return True
    except Exception as e:
        print_error(f"Error during Python package installation: {e}")
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
    print_info("Launching main.py")
    import main

if __name__ == "__main__":
    missing_modules = check_modules()
    if missing_modules:
        print_warning(f"Missing Python modules detected: {', '.join(missing_modules)}")
        if not install_system_dependencies():
            print_error("Failed to install system dependencies. Exiting.")
            sys.exit(1)
        if not install_python_packages():
            print_error("Failed to install Python packages. Exiting.")
            sys.exit(1)
    launch_main()
