import json
import tkinter as tk
import tkinter.messagebox as messagebox

CONFIG_FILE = "C:\\ActiveAssist\\settings\\settings.json"

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


def save_button_clicked():
    proxy_host = entry_proxy_host.get()
    proxy_port = entry_proxy_port.get()
    license_key = entry_license_key.get()
    scan_rate = scan_rate.get()

    config = load_config()
    if config is None:
        return

    config["proxyHost"] = proxy_host
    config["proxyPort"] = proxy_port
    config["licenseKey"] = license_key
    config["scanRate"] = scan_rate

    save_config(config)
    status_label.config(text="Configuration saved successfully")
    messagebox.showinfo("succes", "Configuration saved successfully")

# Load config
config = load_config()
if config is None:
    exit()

# Create GUI
root = tk.Tk()
root.title("Proxy Configuration")
root.geometry("400x400")
root.resizable(False, False)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the x and y position to center the window
x = int((screen_width - 400) / 2)
y = int((screen_height - 400) / 2)

# Set the window position
root.geometry(f"400x400+{x}+{y}")
root.deiconify()
# Create input fields
label_proxy_host = tk.Label(root, text="Proxy Host:")
label_proxy_host.pack()
entry_proxy_host = tk.Entry(root, width=30)
entry_proxy_host.insert(tk.END, config["proxyHost"])
entry_proxy_host.pack()

label_proxy_port = tk.Label(root, text="Proxy Port:")
label_proxy_port.pack()
entry_proxy_port = tk.Entry(root, width=30)
entry_proxy_port.insert(tk.END, config["proxyPort"])
entry_proxy_port.pack()

label_scan_rate = tk.Label(root, text="Scan Rate (sec):")
label_scan_rate.pack()
entry_scan_rate = tk.Entry(root, width=30)
entry_scan_rate.insert(tk.END, config["scanRate"])
entry_scan_rate.pack()

label_license_key = tk.Label(root, text="License Key:")
label_license_key.pack()
entry_license_key = tk.Entry(root, width=30)
entry_license_key.insert(tk.END, config["licenseKey"])
entry_license_key.pack(pady=10)

# Create save button
save_button = tk.Button(
    root, text="Save", command=save_button_clicked, width=30)
save_button.pack(pady=10)

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()
