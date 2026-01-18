import socket
import struct

PORTA_DISCOVERY = 50000
MULTICAST_GROUP = "239.255.0.1"

MESSAGGIO_RICHIESTA = "CERCASI_AURASERVER"
MESSAGGIO_RISPOSTA = "AURASERVER"

def get_local_ip():
    """ottiene l'IP locale del auraserver"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    # creazione socket UDP(socket.AF_INET = IPv4, socket.SOCK_DGRAM = UDP)
    try:
        s.connect(("8.8.8.8", 80))  # connessione a un server esterno per ottenere l'IP locale dell'interfaccia di rete
        ip = s.getsockname()[0]  # restituisce una tupla (IP, porta)
    finally:
        s.close()
    return ip

def avvia_server():
    ip_server = get_local_ip()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # bind su tutte le interfacce
    sock.bind(("", PORTA_DISCOVERY))

    # iscrizione al gruppo multicast
    mreq = struct.pack("4sl", socket.inet_aton(MULTICAST_GROUP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print(f"AuraServer attivo su {ip_server}:{PORTA_DISCOVERY}")
    print("In ascolto multicast...")

    while True:
        try:
            # riceve richieste
            data, addr = sock.recvfrom(1024)
            messaggio = data.decode(errors="ignore").strip()
            print(f"Ricevuto '{messaggio}' da {addr}")

            if messaggio == MESSAGGIO_RICHIESTA:
                risposta = f"{MESSAGGIO_RISPOSTA}: {ip_server}"
                sock.sendto(risposta.encode(), addr)
                print(f"Risposto a {addr[0]}")

        except Exception as e:
            # log degli errori senza fermare il server
            print("Errore:", e)

if __name__ == "__main__":
    avvia_server()