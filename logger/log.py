import datetime
import os

def LogActivities(log, log_path="C:\\ActiveAssist\\Logger"):
    today = datetime.datetime.now().strftime("%d%m%y")
    log_filename = f"monitor_{today}.log"
    log_file_path = os.path.join(log_path, log_filename)
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {log}\n"
    
    with open(log_file_path, "a") as file:
        file.write(log_entry)
