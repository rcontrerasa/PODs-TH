import time
import os
import sys
import subprocess

# 🔹 Verificar si paramiko está instalado, si no, instalarlo automáticamente
try:
    import paramiko
except ImportError:
    print("[INFO] Paramiko no está instalado. Instalándolo ahora...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "paramiko"])
    import paramiko

# Datos de autenticación para los dispositivos
DEVICE_USER = "CCNA"
DEVICE_PASSWORD = input("Ingrese Contraseña Para CCNA: ")

# Ruta base de los archivos de configuración (el mismo directorio que el script)
CONFIGS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "configs")

# Diccionario de configuraciones por dispositivo
DEVICE_CONFIGS = {
    "ISP": "ISP.txt",
    "R1": "R1.txt",
    "R2": "R2.txt",
    "R3": "R3.txt",
    "DLS1": "DLS1.txt",
    "DLS2": "DLS2.txt",
    "ALS1": "ALS1.txt",
}

# Datos de los dispositivos (todos incluidos aquí)
DEVICES = [
    # POD-1
    {"device": "ISP-P1", "ip": "172.16.0.10"},
    {"device": "R1-P1", "ip": "172.16.0.11"},
    {"device": "R2-P1", "ip": "172.16.0.12"},
    {"device": "R3-P1", "ip": "172.16.0.13"},
    {"device": "DLS1-P1", "ip": "172.16.0.14"},
    {"device": "DLS2-P1", "ip": "172.16.0.15"},
    {"device": "ALS1-P1", "ip": "172.16.0.16"},
    # POD-2
    {"device": "ISP-P2", "ip": "172.16.0.20"},
    {"device": "R1-P2", "ip": "172.16.0.21"},
    {"device": "R2-P2", "ip": "172.16.0.22"},
    {"device": "R3-P2", "ip": "172.16.0.23"},
    {"device": "DLS1-P2", "ip": "172.16.0.24"},
    {"device": "DLS2-P2", "ip": "172.16.0.25"},
    {"device": "ALS1-P2", "ip": "172.16.0.26"},
    # POD-3
    {"device": "ISP-P3", "ip": "172.16.0.30"},
    {"device": "R1-P3", "ip": "172.16.0.31"},
    {"device": "R2-P3", "ip": "172.16.0.32"},
    {"device": "R3-P3", "ip": "172.16.0.33"},
    {"device": "DLS1-P3", "ip": "172.16.0.34"},
    {"device": "DLS2-P3", "ip": "172.16.0.35"},
    {"device": "ALS1-P3", "ip": "172.16.0.36"},
    # POD-4
    {"device": "ISP-P4", "ip": "172.16.0.40"},
    {"device": "R1-P4", "ip": "172.16.0.41"},
    {"device": "R2-P4", "ip": "172.16.0.42"},
    {"device": "R3-P4", "ip": "172.16.0.43"},
    {"device": "DLS1-P4", "ip": "172.16.0.44"},
    {"device": "DLS2-P4", "ip": "172.16.0.45"},
    {"device": "ALS1-P4", "ip": "172.16.0.46"},
    # POD-5
    {"device": "ISP-P5", "ip": "172.16.0.50"},
    {"device": "R1-P5", "ip": "172.16.0.51"},
    {"device": "R2-P5", "ip": "172.16.0.52"},
    {"device": "R3-P5", "ip": "172.16.0.53"},
    {"device": "DLS1-P5", "ip": "172.16.0.54"},
    {"device": "DLS2-P5", "ip": "172.16.0.55"},
    {"device": "ALS1-P5", "ip": "172.16.0.56"},
]

# Función para enviar comandos SSH
def send_ssh_commands(ip, username, password, commands):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"[INFO] Conectando a {ip}...")
        ssh_client.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)
        print(f"[INFO] Conexión establecida con {ip}.")
        
        # Abrir canal interactivo
        shell = ssh_client.invoke_shell()
        time.sleep(0.5)  # Aumentar el tiempo de espera inicial
        
        # Enviar tres "Enter" seguidos para asegurar la conexión correcta
        for _ in range(2):
            shell.send("\n")
            shell.send("\n")
            shell.send("\n")
            time.sleep(0.1)  # Espera de 2 segundos entre los pulsos de "Enter"
        
        # Leer la salida de la shell para asegurarse de que esté lista
        shell.recv(65535)
        
        # Enviar comandos
        for command in commands:
            print(f"[INFO] Enviando comando: {command.strip()}")
            shell.send(command + "\n")
            time.sleep(0.1)  # Aumentar el tiempo de espera después de enviar cada comando
            output = shell.recv(65535).decode()
            print(f"[DEBUG] Salida de {ip}:\n{output}")
        
        # Cerrar conexión
        shell.close()
    except Exception as e:
        print(f"[ERROR] No se pudo conectar a {ip}: {e}")
    finally:
        ssh_client.close()

# Función principal para configurar dispositivos
def main():
    if not os.path.exists(CONFIGS_PATH):
        print(f"[ERROR] La carpeta de configuraciones '{CONFIGS_PATH}' no existe.")
        sys.exit(1)
    for device_info in DEVICES:
        device = device_info["device"]
        ip = device_info["ip"]
        device_type = device.split("-")[0]
        config_file = DEVICE_CONFIGS.get(device_type)
        
        if not config_file:
            print(f"[ERROR] Configuración no encontrada para {device_type}")
            continue

        # Leer archivo de configuración
        config_path = os.path.join(CONFIGS_PATH, config_file)

        try:
            with open(config_path, "r") as file:
                commands = file.readlines()
            print(f"[INFO] Aplicando configuración a {device} ({ip})...")
            send_ssh_commands(ip, DEVICE_USER, DEVICE_PASSWORD, commands)
        except FileNotFoundError:
            print(f"[ERROR] Archivo de configuración no encontrado: {config_file}")
        except Exception as e:
            print(f"[ERROR] Error aplicando configuración a {device}: {e}")

if __name__ == "__main__":
    main()
    input("Fin del Proceso.")