import socket



PORTA_DISCOVERY = 50000
MESSAGGIO_RICHIESTA = "CERCASI_AURASERVER"
MESSAGGIO_RISPOSTA = "AURASERVER"

def get_local_ip():
    """ottiene l'IP locale del auraserver"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    #   creazione socket UDP(socket.AF_INET = IPv4, socket.SOCK_DGRAM = UDP)
    try:
        s.connect(("8.8.8.8", 80))# connessione a un server esterno per ottenere l'IP locale dell interfaccia di rete
        ip = s.getsockname()[0] # restituisce una tupla (IP, porta)
    finally:
        s.close()
    return ip

def avvia_server():
    ip_server = get_local_ip()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # consente il riutilizzo dell'indirizzo (safe su tutti gli OS anche windows💩)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(("0.0.0.0", PORTA_DISCOVERY))

    print(f"AuraServer avviato su {ip_server}:{PORTA_DISCOVERY}")
    print("In ascolto per richieste di discovery...")

    while True:
        try:
            data, addr = sock.recvfrom(1024)
            messaggio = data.decode().strip()

            if messaggio == MESSAGGIO_RICHIESTA:
                risposta = f"{MESSAGGIO_RISPOSTA}: {ip_server}"
                sock.sendto(risposta.encode(), addr)
                print(f"Risposto a {addr[0]}")

        except Exception as e:
            # il server resta sempre attivo anche in caso di errore
            print("Errore:", e)

if __name__ == "__main__":
    avvia_server()