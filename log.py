import datetime

def logactivities(log, log_file="monitor.log"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {log}\n"
    
    with open(log_file, "a") as file:
        file.write(log_entry)
