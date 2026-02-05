import socket
import threading
import json
import os

PORTA_TCP = 60000
UTENTI_FILE = "clients.json"

client_connessi = {}

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def carica_client():
    if os.path.exists(UTENTI_FILE):
        with open(UTENTI_FILE, "r") as f:
            return json.load(f)
    return {}

def salva_client(data):
    with open(UTENTI_FILE, "w") as f:
        json.dump(data, f, indent=2)

def gestisci_client(conn, addr, db):
    try:
        data = conn.recv(1024)
        payload = json.loads(data.decode())

        if payload["type"] == "REGISTER":
            nome = payload["name"]
            client_connessi[conn] = nome
            db[addr[0]] = nome
            salva_client(db)
            print(f"{nome} connesso")

        while True:
            msg = conn.recv(1024)
            if not msg:
                break

            testo = msg.decode()
            mittente = client_connessi.get(conn, "Sconosciuto")

            for c in list(client_connessi):
                if c != conn:
                    c.sendall(f"{mittente}: {testo}".encode())
    finally:
        client_connessi.pop(conn, None)
        conn.close()

def tcp_server():
    db = carica_client()
    ip = get_local_ip()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", PORTA_TCP))
    server.listen()

    print(f"SERVER ATTIVO SU {ip}:{PORTA_TCP}")

    while True:
        conn, addr = server.accept()
        threading.Thread(
            target=gestisci_client,
            args=(conn, addr, db),
            daemon=True
        ).start()

if __name__ == "__main__":
    tcp_server()
