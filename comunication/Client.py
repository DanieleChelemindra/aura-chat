import socket
from logger import log_txt

SERVER = '127.0.0.1'
PORT = 5001
LOG_FILE = "client_log.txt"

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    log_txt(LOG_FILE, f"CONNESSO a {SERVER}:{PORT}")

    welcome = client.recv(1024).decode().strip()
    print(welcome)
    log_txt(LOG_FILE, f"RICEVUTO: {welcome}")

    while True:
        msg = input("Scrivi un messaggio (TIME, NAME, EXIT o altro): ")
        client.sendall(msg.encode())
        log_txt(LOG_FILE, f"INVIATO: {msg}")

        risposta = client.recv(1024).decode().strip()
        print("Server:", risposta)
        log_txt(LOG_FILE, f"RICEVUTO: {risposta}")

        if msg.upper() == "EXIT":
            break

    client.close()
    log_txt(LOG_FILE, "DISCONNESSO")

if __name__ == "__main__":
    main()
