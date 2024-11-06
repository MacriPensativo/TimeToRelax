import tkinter as tk
from tkinter import colorchooser
import json
import time
import threading
import keyboard
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
from screeninfo import get_monitors

# Configuración inicial
config = {
    "color": "red",
    "opacity": 0.3,
    "deactivation_key": "space",
    "appear_time": 10,
    "monitor": "both"
}
paused = False  # Controla el estado de pausa

# Cargar configuración desde un archivo
def load_config():
    global config
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        save_config(config)

# Guardar configuración en un archivo
def save_config(new_config):
    with open("config.json", "w") as f:
        json.dump(new_config, f)

# Interfaz de configuración
def open_settings():
    settings_window = tk.Toplevel()
    settings_window.title("Configuración de TimeToRelax")
    
    # Color de fondo
    tk.Label(settings_window, text="Color del pantallazo:").pack()
    color_btn = tk.Button(settings_window, text="Elegir color", command=lambda: choose_color(settings_window))
    color_btn.pack()

    # Opacidad
    tk.Label(settings_window, text="Opacidad del pantallazo (0.1 - 1.0):").pack()
    opacity_entry = tk.Entry(settings_window)
    opacity_entry.insert(0, str(config["opacity"]))
    opacity_entry.pack()

    # Tecla de desactivación
    tk.Label(settings_window, text="Tecla para desactivar:").pack()
    key_entry = tk.Entry(settings_window)
    key_entry.insert(0, config["deactivation_key"])
    key_entry.pack()

    # Tiempo de aparición
    tk.Label(settings_window, text="Tiempo para que aparezca (segundos):").pack()
    time_entry = tk.Entry(settings_window)
    time_entry.insert(0, str(config["appear_time"]))
    time_entry.pack()

    # Selección de monitor
    tk.Label(settings_window, text="Monitor para mostrar el pantallazo:").pack()
    monitor_var = tk.StringVar(settings_window)
    monitor_var.set(config["monitor"])
    tk.OptionMenu(settings_window, monitor_var, "both", "primary", "secondary").pack()

    # Botón de guardar configuración
    save_btn = tk.Button(settings_window, text="Guardar", command=lambda: save_settings(opacity_entry, key_entry, time_entry, monitor_var, settings_window))
    save_btn.pack()

def choose_color(settings_window):
    color_code = colorchooser.askcolor(title="Elige el color de fondo")[1]
    if color_code:
        config["color"] = color_code

def save_settings(opacity_entry, key_entry, time_entry, monitor_var, settings_window):
    try:
        config["opacity"] = float(opacity_entry.get())
        config["deactivation_key"] = key_entry.get()
        config["appear_time"] = int(time_entry.get())
        config["monitor"] = monitor_var.get()
        save_config(config)
        settings_window.destroy()
    except ValueError:
        print("Error en la configuración. Verifica los valores.")

# Pantallazo de descanso
def show_overlay():
    monitors = get_monitors()
    
    def create_window_for_monitor(monitor):
        window = tk.Toplevel()
        window.geometry(f"{monitor.width}x{monitor.height}+{monitor.x}+{monitor.y}")
        window.attributes('-topmost', True)
        window.attributes('-alpha', config["opacity"])
        window.configure(background=config["color"])
        
        message = tk.Label(window, text="TIME TO HAVE A BREAK!!", font=("Arial", 48, "bold"), fg="white", bg=config["color"])
        message.place(relx=0.5, rely=0.5, anchor="center")
        
        return window

    windows = []
    if config["monitor"] == "both":
        for monitor in monitors:
            windows.append(create_window_for_monitor(monitor))
    elif config["monitor"] == "primary" and monitors:
        windows.append(create_window_for_monitor(monitors[0]))
    elif config["monitor"] == "secondary" and len(monitors) > 1:
        windows.append(create_window_for_monitor(monitors[1]))

    is_visible = True
    def toggle_visibility():
        nonlocal is_visible
        is_visible = not is_visible
        for window in windows:
            if is_visible:
                window.deiconify()
            else:
                window.withdraw()
        if windows:
            windows[0].after(500, toggle_visibility)

    def deactivate():
        start = None
        while True:
            if keyboard.is_pressed(config["deactivation_key"]):
                if start is None:
                    start = time.time()
                elif time.time() - start >= 3:
                    for window in windows:
                        window.destroy()
                    return
            else:
                start = None
            time.sleep(0.1)

    toggle_visibility()
    threading.Thread(target=deactivate, daemon=True).start()
    windows[0].mainloop()

# Temporizador para activar el pantallazo
def start_timer():
    if not paused:  # Verifica el estado de pausa
        root.after(config["appear_time"] * 1000, show_overlay)

# Pausar/Reanudar temporizador
def toggle_pause():
    global paused
    paused = not paused
    if paused:
        print("Temporizador pausado.")
    else:
        print("Temporizador reanudado.")
        start_timer()  # Reinicia el temporizador al reanudar

def on_exit(icon, item):
    icon.stop()

def setup_tray_icon():
    image = Image.new("RGB", (64, 64), (255, 0, 0))
    d = ImageDraw.Draw(image)
    d.rectangle([0, 0, 64, 64], fill=(255, 0, 0))

    icon = Icon("TimeToRelax", image, menu=Menu(
        MenuItem("Configuración", lambda icon, item: open_settings()),
        MenuItem("Pausar/Reanudar", lambda icon, item: toggle_pause()),
        MenuItem("Salir", on_exit)
    ))
    icon.run_detached()

if __name__ == "__main__":
    load_config()
    
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal de Tkinter
    open_settings()  # Abre el menú de configuración
    
    # Inicia el temporizador para el pantallazo de descanso
    setup_tray_icon()  # Configura el icono de la bandeja del sistema
    start_timer()  # Inicia el temporizador
    root.mainloop()
