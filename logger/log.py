import datetime
import os

def LogActivities(log, log_file="monitor.log"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {log}\n"
    log_directory = "logger"

    log_path = os.path.join(log_directory, log_file)
    
    with open(log_path, "a") as file:
        file.write(log_entry)
