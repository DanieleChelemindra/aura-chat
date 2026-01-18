import socket



PORTA_DISCOVERY = 50000
MULTICAST_GROUP = "239.255.0.1"
MESSAGGIO = "CERCASI_AURASERVER"
TIMEOUT = 5

def scopri_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.settimeout(TIMEOUT)

    sock.sendto(MESSAGGIO.encode(), (MULTICAST_GROUP, PORTA_DISCOVERY))
    print("Richiesta multicast inviata...")

    try:
        data, addr = sock.recvfrom(1024)
        print("Server trovato:", data.decode(), "da", addr)
    except socket.timeout:
        print("Nessun server trovato")

    sock.close()

if __name__ == "__main__":
    scopri_server()