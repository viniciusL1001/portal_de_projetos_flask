import subprocess
import sys


def install_packages():
    # Dependências do exemplo Flask do professor, mais o leitor de .env.
    packages = [
        "flask",
        "mysql-connector-python",
        "bcrypt",
        "pyjwt",
        "flask-cors",
        "python-dotenv"
    ]
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])


if __name__ == "__main__":
    install_packages()
    print("Dependências instaladas. O banco de dados existente não foi alterado.")
