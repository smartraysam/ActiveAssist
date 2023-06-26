import json
import subprocess
import tkinter as tk
import tkinter.messagebox as messagebox
import pystray
import win32gui
import win32con
from pystray import MenuItem as item, Menu
from PIL import Image

CONFIG_FILE = "C:\\ActiveAssist\\data\\config.json"
TRAY_ICON = "C:\\ActiveAssist\\assets\\tray_icon.png"

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        messagebox.showerror("Error", "Config file not found!")
        return None
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Invalid config file format!")
        return None

    return config

def save_config(config):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save config file: {e}")

def restart_service():
    try:
        subprocess.run(["python", "your_service_wrapper.py", "restart"], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to restart service: {e}")

def save_button_clicked():
    proxy_host = entry_proxy_host.get()
    proxy_port = entry_proxy_port.get()

    config = load_config()
    if config is None:
        return

    config["proxyHost"] = proxy_host
    config["proxyPort"] = proxy_port

    save_config(config)
    restart_service()

    # root.iconify()
    root.withdraw()

def tray_icon_clicked(icon, item):
    if item == "maximize":
        root.deiconify()
        icon.stop()
    elif item == "exit":
        icon.stop()
        root.destroy()

# Load config
config = load_config()
if config is None:
    exit()

# Create GUI
root = tk.Tk()
root.title("Proxy Configuration")
root.geometry("300x150")
root.protocol("WM_DELETE_WINDOW", lambda: tray_icon_clicked(icon, "exit"))

# Create input fields
label_proxy_host = tk.Label(root, text="Proxy Host:")
label_proxy_host.pack()
entry_proxy_host = tk.Entry(root)
entry_proxy_host.insert(tk.END, config["proxyHost"])
entry_proxy_host.pack()

label_proxy_port = tk.Label(root, text="Proxy Port:")
label_proxy_port.pack()
entry_proxy_port = tk.Entry(root)
entry_proxy_port.insert(tk.END, config["proxyPort"])
entry_proxy_port.pack()

# Create save button
save_button = tk.Button(root, text="Save", command=save_button_clicked)
save_button.pack()

# Create system tray icon
def menu_exit_clicked(icon, item):
    icon.stop()
    root.destroy()

menu = (item('Maximize', lambda: tray_icon_clicked(icon, "maximize")),
        item('Exit', lambda: tray_icon_clicked(icon, "exit")))

image = Image.open(TRAY_ICON)
image = image.resize((30, 30))
icon = pystray.Icon("name", image, "Title", menu)
icon.run()

# Start the main event loop
root.mainloop()