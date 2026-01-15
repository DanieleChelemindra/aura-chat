import socket
import threading
import datetime
from logger import log_txt

HOST = '127.0.0.1'
PORT = 5001
LOG_FILE = "server_log.txt"

def handle_client(conn, addr):
    log_txt(LOG_FILE, f"CLIENT CONNESSO {addr}")
    conn.sendall(f"Ciao {addr[0]}, connessione stabilita!\n".encode())

    while True:
        data = conn.recv(1024).decode().strip()
        if not data:
            break

        log_txt(LOG_FILE, f"RICEVUTO da {addr[0]}: {data}")
        print(f"[{addr[0]}] -> {data}")

        if data.upper() == "TIME":
            risposta = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elif data.upper() == "NAME":
            risposta = socket.gethostname()
        elif data.upper() == "EXIT":
            risposta = "connessione chiusa"
            conn.sendall(risposta.encode())
            log_txt(LOG_FILE, f"INVIATO: {risposta}")
            break
        else:
            risposta = f"{addr[0]}, messaggio ricevuto"

        conn.sendall((risposta + "\n").encode())
        log_txt(LOG_FILE, f"INVIATO: {risposta}")

    conn.close()
    log_txt(LOG_FILE, f"CLIENT DISCONNESSO {addr}")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[SERVER IN ASCOLTO] su {HOST}:{PORT}")
    log_txt(LOG_FILE, "SERVER AVVIATO")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        log_txt(LOG_FILE, f"CONNESSIONI ATTIVI: {threading.active_count() - 1}")

if __name__ == "__main__":
    main()
