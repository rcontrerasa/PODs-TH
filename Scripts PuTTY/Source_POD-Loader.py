import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys
import shutil

def get_profiles():
    profiles = {}
    base_dirs = ["ASA", "CCNA", "CCNP"]
    
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS  # Si está empaquetado como .exe
    else:
        base_path = os.getcwd()  # Si está corriendo desde el script

    for category in base_dirs:
        category_path = os.path.join(base_path, category)
        profiles[category] = []

        if os.path.exists(category_path):
            for file in os.listdir(category_path):
                if file.endswith(".reg"):
                    profile_name = file.replace(".reg", "")
                    # Cambiar el nombre mostrado, por ejemplo, CCNP-POD1 a POD-1
                    display_name = profile_name.split('-')[-1]
                    profiles[category].append((profile_name, f"{display_name}"))
    return profiles

def find_putty():
    possible_paths = [
        "C:\\Program Files\\PuTTY\\putty.exe",
        "C:\\Program Files (x86)\\PuTTY\\putty.exe",
        os.path.join(os.environ.get("ProgramFiles", ""), "PuTTY", "putty.exe"),
        os.path.join(os.environ.get("ProgramFiles(x86)", ""), "PuTTY", "putty.exe")
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def show_pods(category):
    global selected_category, selected_profile_var, profile_vars
    selected_category = category
    selected_profile_var = None
    profile_vars = {}
    main_frame.pack_forget()
    pod_frame.pack()
    
    # Mostrar la categoría grande centrada y luego el texto de selección de POD
    category_label.config(text=category, font=("Arial", 24, "bold"))
    pod_label.config(text="Selecciona un POD:", font=("Arial", 16, "bold"))
    
    for widget in pod_check_frame.winfo_children():
        widget.destroy()
    
    for profile, display_name in profiles.get(category, []):
        btn = tk.Button(pod_check_frame, text=display_name, font=("Arial", 12, "bold"), width=20, height=2, command=lambda p=profile: add_single_profile(p))
        btn.pack(pady=5)
    
    manual_btn = tk.Button(pod_check_frame, text="Multiple", font=("Arial", 10, "bold"), width=15, height=1, command=show_manual_selection)
    manual_btn.pack(pady=5)

def show_manual_selection():
    pod_frame.pack_forget()
    manual_frame.pack()
    manual_label.config(text=f"Selecciona múltiples PODs de {selected_category}")
    
    for widget in manual_check_frame.winfo_children():
        widget.destroy()
    
    for profile, _ in profiles.get(selected_category, []):
        var = tk.BooleanVar()
        tk.Checkbutton(manual_check_frame, text=profile, variable=var).pack(anchor='w')
        profile_vars[profile] = var

def go_back():
    pod_frame.pack_forget()
    main_frame.pack()

def go_back_manual():
    manual_frame.pack_forget()
    pod_frame.pack()

def add_single_profile(profile):
    # Obtener la ruta del archivo .reg
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.getcwd()
    
    reg_file_path = os.path.join(base_path, selected_category, f"{profile}.reg")
    
    # Comprobar si el archivo reg existe
    if os.path.exists(reg_file_path):
        # Copiar el archivo reg temporalmente para usarlo
        temp_reg_file = os.path.join(base_path, "temp.reg")
        shutil.copy(reg_file_path, temp_reg_file)
        subprocess.run(["reg", "import", temp_reg_file], shell=True)
        os.remove(temp_reg_file)  # Eliminar el archivo temporal después de la importación

        # Preguntar si se desea abrir el perfil
        if messagebox.askyesno("Abrir en PuTTY", "¿Deseas abrir el perfil ahora?"):
            open_profile(profile)
        messagebox.showinfo("Éxito", f"El perfil {profile} ha sido añadido con éxito.")
    else:
        messagebox.showerror("Error", f"El perfil {profile} no se encuentra.")

def add_multiple_profiles():
    selected_profiles = [profile for profile, var in profile_vars.items() if var.get()]
    if not selected_profiles:
        messagebox.showwarning("Selección Vacía", "No has seleccionado ningún perfil para añadir.")
        return
    
    for profile in selected_profiles:
        # Obtener la ruta del archivo .reg
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.getcwd()

        reg_file_path = os.path.join(base_path, selected_category, f"{profile}.reg")
        
        if os.path.exists(reg_file_path):
            # Copiar el archivo reg temporalmente para usarlo
            temp_reg_file = os.path.join(base_path, "temp.reg")
            shutil.copy(reg_file_path, temp_reg_file)
            subprocess.run(["reg", "import", temp_reg_file], shell=True)
            os.remove(temp_reg_file)  # Eliminar el archivo temporal después de la importación

    messagebox.showinfo("Éxito", f"Se han añadido {len(selected_profiles)} perfiles con éxito.")

def open_profile(profile):
    # Obtener la ruta del archivo .bat
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.getcwd()

    bat_file_path = os.path.join(base_path, selected_category, f"Open_{profile}.bat")

    if os.path.exists(bat_file_path):
        subprocess.Popen([bat_file_path], shell=True)
    else:
        messagebox.showerror("Error", f"El archivo BAT para {profile} no se encuentra.")

# Función para obtener el archivo .ico en el entorno correcto (fuera o dentro del .exe)
def get_icon_path():
    if getattr(sys, 'frozen', False):  # Si estamos ejecutando un .exe
        # Si es un .exe, el icono estará en el directorio temporal del ejecutable
        return os.path.join(sys._MEIPASS, 'putty.ico')
    else:
        # Si no es un .exe, el icono estará en el directorio de trabajo
        return 'putty.ico'

# Crear ventana principal
root = tk.Tk()
root.title("POD-Loader")
root.geometry("500x550")

# Establecer el icono de la ventana
icon_path = get_icon_path()
root.iconbitmap(icon_path)  # Usamos la ruta obtenida por la función

profiles = get_profiles()
selected_category = None
profile_vars = {}

# Pantalla de selección de categoría
main_frame = tk.Frame(root)
main_frame.pack()
# Título grande y centrado
title_label = tk.Label(main_frame, text="Selecciona un perfil", font=("Arial", 20, "bold"))
title_label.pack(pady=20)

# Crear botones para CCNA, CCNP, ASA
button_frame = tk.Frame(main_frame)
button_frame.pack()

ccna_button = tk.Button(button_frame, text="CCNA", font=("Arial", 14, "bold"), width=10, height=2, command=lambda: show_pods("CCNA"))
ccnp_button = tk.Button(button_frame, text="CCNP", font=("Arial", 14, "bold"), width=10, height=2, command=lambda: show_pods("CCNP"))
asa_button = tk.Button(main_frame, text="ASA", font=("Arial", 14, "bold"), width=10, height=2, command=lambda: show_pods("ASA"))

ccna_button.grid(row=0, column=0, padx=10, pady=10)
ccnp_button.grid(row=0, column=1, padx=10, pady=10)
asa_button.pack(pady=10)

# Pantalla de selección de PODs
pod_frame = tk.Frame(root)
category_label = tk.Label(pod_frame, text="", font=("Arial", 24, "bold"))
category_label.pack()
pod_label = tk.Label(pod_frame, text="", font=("Arial", 16, "bold"))
pod_label.pack()
pod_check_frame = tk.Frame(pod_frame)
pod_check_frame.pack()

tk.Button(pod_frame, text="Volver", font=("Arial", 10), command=go_back).pack(pady=5)

# Pantalla de selección manual
manual_frame = tk.Frame(root)
manual_label = tk.Label(manual_frame, text="", font=("Arial", 12, "bold"))
manual_label.pack()
manual_check_frame = tk.Frame(manual_frame)
manual_check_frame.pack()

tk.Button(manual_frame, text="Añadir al Registro", font=("Arial", 10), command=add_multiple_profiles).pack(pady=5)
tk.Button(manual_frame, text="Volver", font=("Arial", 10), command=go_back_manual).pack(pady=5)

root.mainloop()
