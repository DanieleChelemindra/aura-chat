import socket
import struct
import threading
import json
import os

PORTA_DISCOVERY = 50000
PORTA_TCP = 60000
MULTICAST_GROUP = "239.255.0.1"

MESSAGGIO_RICHIESTA = "PAIRING_REQUEST"

UTENTI_FILE = "clients.json"

client_connessi = {}   # conn -> nome
client_sockets = []


def get_local_ip():
    """ottiene l'IP locale del auraserver"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # creazione socket UDP(socket.AF_INET = IPv4, socket.SOCK_DGRAM = UDP)
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


def udp_discovery():
    ip_server = get_local_ip()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) 
    # creazione socket UDP(socket.AF_INET = IPv4, socket.SOCK_DGRAM = si usano datagrammi, socket.IPPROTO_UDP = prot. UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # permette di riutilizzare la porta senza aspettare che il SO la liberi (chatgtp)
    sock.bind(("", PORTA_DISCOVERY))
    # bind ascolto su tutte le interfacce di rete alla porta PORTA_DISCOVERY

    mreq = struct.pack("4sl", socket.inet_aton(MULTICAST_GROUP), socket.INADDR_ANY)
    # struttura per iscriversi al gruppo multicast (4s = 4 byte stringa, l = long intero)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    # ricezione messaggi multicast

    print("AURAServer UDP discovery attivo")

    while True:
        data, addr = sock.recvfrom(1024)
        
        messaggio = data.decode().strip()

        if messaggio == MESSAGGIO_RICHIESTA:
            risposta = json.dumps({
                "type": "PAIRING_RESPONSE",
                "server_ip": ip_server,
                "tcp_port": PORTA_TCP
            })
            sock.sendto(risposta.encode(), addr)


def gestisci_client(conn, addr, db):
    try:
        data = conn.recv(1024)
        payload = json.loads(data.decode())

        if payload["type"] == "REGISTER":
            nome = payload["name"]
            client_connessi[conn] = nome
            db[addr[0]] = nome
            salva_client(db)

            print(f"Client registrato: {nome} ({addr[0]})")

        while True:
            msg = conn.recv(1024)
            if not msg:
                break

            testo = msg.decode()
            mittente = client_connessi.get(conn, "Sconosciuto")

            for c in client_connessi:
                if c != conn:
                    c.sendall(f"{mittente}: {testo}".encode())

    finally:
        client_connessi.pop(conn, None)
        conn.close()


def tcp_server():
    db = carica_client()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", PORTA_TCP))
    server.listen()

    print("Server TCP chat attivo")

    while True:
        conn, addr = server.accept()
        threading.Thread(
            target=gestisci_client,
            args=(conn, addr, db),
            daemon=True
        ).start()


if __name__ == "__main__":
    threading.Thread(target=udp_discovery, daemon=True).start()
    tcp_server()