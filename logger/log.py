import datetime
import os

def LogActivities(log, log_path="C:\\ActiveAssist\\logger\\monitor.log"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {log}\n"    
    with open(log_path, "a") as file:
        file.write(log_entry)
