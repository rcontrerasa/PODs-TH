import time
import os
import sys
import subprocess
import ctypes

# Verificar si paramiko está instalado, si no, instalarlo automáticamente
try:
    import paramiko
except ImportError:
    print("[INFO] Paramiko no está instalado. Instalándolo ahora...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "paramiko"])
    import paramiko

def open_configs_folder():
    """Abre la carpeta 'configs' y espera la confirmación del usuario para continuar."""
    if os.path.exists(CONFIGS_PATH):
        print(f"[INFO] Abriendo la carpeta de configuraciones: {CONFIGS_PATH}")
        subprocess.Popen(f'explorer "{CONFIGS_PATH}"')  # Abre el explorador de archivos en la carpeta configs
        ctypes.windll.user32.MessageBoxW(0, "Verifique que los archivos de configuración están en la carpeta 'configs'.\nPresione Aceptar para continuar.", "Confirmación", 1)
    else:
        ctypes.windll.user32.MessageBoxW(0, f"La carpeta de configuraciones no existe en: {CONFIGS_PATH}", "Error", 0)
        sys.exit(1)

# Datos de autenticación para los dispositivos
DEVICE_USER = "CCNP"
DEVICE_PASSWORD = input("Ingrese Contraseña Para CCNP: ")

# Ruta base de los archivos de configuración
if getattr(sys, 'frozen', False):
    # Si el script es un ejecutable empaquetado con PyInstaller
    # Busca la carpeta 'configs' en el directorio donde está el ejecutable
    CONFIGS_PATH = os.path.join(sys._MEIPASS, "configs")
else:
    # Si estamos ejecutando el script desde el código fuente
    CONFIGS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "configs")

# Si no encuentra los archivos de configuración, buscar en el directorio de instalación del ejecutable
if not os.path.exists(CONFIGS_PATH):
    CONFIGS_PATH = os.path.join(os.path.dirname(sys.executable), "configs")

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

# Datos de los dispositivos (actualizados con las nuevas IPs)
DEVICES = [
    # POD-1
    {"device": "ISP-P1", "ip": "172.16.0.80"},
    {"device": "R1-P1", "ip": "172.16.0.81"},
    {"device": "R2-P1", "ip": "172.16.0.82"},
    {"device": "R3-P1", "ip": "172.16.0.83"},
    {"device": "DLS1-P1", "ip": "172.16.0.84"},
    {"device": "DLS2-P1", "ip": "172.16.0.85"},
    {"device": "ALS1-P1", "ip": "172.16.0.86"},
    # POD-2
    {"device": "ISP-P2", "ip": "172.16.0.90"},
    {"device": "R1-P2", "ip": "172.16.0.91"},
    {"device": "R2-P2", "ip": "172.16.0.92"},
    {"device": "R3-P2", "ip": "172.16.0.93"},
    {"device": "DLS1-P2", "ip": "172.16.0.94"},
    {"device": "DLS2-P2", "ip": "172.16.0.95"},
    {"device": "ALS1-P2", "ip": "172.16.0.96"},
    # POD-3
    {"device": "ISP-P3", "ip": "172.16.0.100"},
    {"device": "R1-P3", "ip": "172.16.0.101"},
    {"device": "R2-P3", "ip": "172.16.0.102"},
    {"device": "R3-P3", "ip": "172.16.0.103"},
    {"device": "DLS1-P3", "ip": "172.16.0.104"},
    {"device": "DLS2-P3", "ip": "172.16.0.105"},
    {"device": "ALS1-P3", "ip": "172.16.0.106"},
    # POD-4
    {"device": "ISP-P4", "ip": "172.16.0.110"},
    {"device": "R1-P4", "ip": "172.16.0.111"},
    {"device": "R2-P4", "ip": "172.16.0.112"},
    {"device": "R3-P4", "ip": "172.16.0.113"},
    {"device": "DLS1-P4", "ip": "172.16.0.114"},
    {"device": "DLS2-P4", "ip": "172.16.0.115"},
    {"device": "ALS1-P4", "ip": "172.16.0.116"},
    # POD-5
    {"device": "ISP-P5", "ip": "172.16.0.120"},
    {"device": "R1-P5", "ip": "172.16.0.121"},
    {"device": "R2-P5", "ip": "172.16.0.122"},
    {"device": "R3-P5", "ip": "172.16.0.123"},
    {"device": "DLS1-P5", "ip": "172.16.0.124"},
    {"device": "DLS2-P5", "ip": "172.16.0.125"},
    {"device": "ALS1-P5", "ip": "172.16.0.126"},
    # POD-6
    {"device": "ISP-P6", "ip": "172.16.0.140"},
    {"device": "R1-P6", "ip": "172.16.0.141"},
    {"device": "R2-P6", "ip": "172.16.0.142"},
    {"device": "R3-P6", "ip": "172.16.0.143"},
    {"device": "DLS1-P6", "ip": "172.16.0.144"},
    {"device": "DLS2-P6", "ip": "172.16.0.145"},
    {"device": "ALS1-P6", "ip": "172.16.0.146"},
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
    open_configs_folder()
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
