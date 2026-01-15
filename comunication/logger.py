from datetime import datetime

def log_txt(filename, messaggio):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {messaggio}\n")
