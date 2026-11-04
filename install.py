import sys
import subprocess


def install_packages():
    # Mesmas dependências empregadas no exemplo Flask do professor.
    packages = ["flask", "mysql-connector-python", "bcrypt", "pyjwt", "flask-cors"]
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def setup_database():
    # ATENÇÃO: o Banco.sql contém DROP SCHEMA e apaga os dados existentes.
    import mysql.connector
    connection = mysql.connector.connect(host="127.0.0.1", user="root", password="", port=3306)
    try:
        with connection.cursor() as cursor:
            with open("./docs/Banco.sql", "r", encoding="utf-8") as arquivo:
                comandos = arquivo.read().split(";")
            for comando in comandos:
                if comando.strip():
                    cursor.execute(comando)
        connection.commit()
        print("Banco criado com sucesso.")
    finally:
        connection.close()


if __name__ == "__main__":
    install_packages()
    if "--recriar-banco" in sys.argv:
        setup_database()
    else:
        print("Dependências instaladas. O banco existente foi preservado.")
