import socket
from network_utils import get_broadcast_ip

PORTA_DISCOVERY = 50000
MESSAGGIO = "CERCASI_AURASERVER"
TIMEOUT = 5

def scopri_server():
    broadcast_ip = get_broadcast_ip()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(("", PORTA_DISCOVERY))
    sock.settimeout(TIMEOUT)

    try:
        sock.sendto(MESSAGGIO.encode(), (broadcast_ip, PORTA_DISCOVERY))
        print(f"Broadcast inviato a {broadcast_ip}")

        data, addr = sock.recvfrom(1024)
        print("Risposta:", data.decode(), "da", addr)

    except socket.timeout:
        print("Nessun server trovato")

    finally:
        sock.close()

if __name__ == "__main__":
    scopri_server()