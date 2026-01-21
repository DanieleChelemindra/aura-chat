import socket
import json
import threading

PORTA_DISCOVERY = 50000
MULTICAST_GROUP = "239.255.0.1"

def ricevi(sock):
    while True:
        try:
            data = sock.recv(1024)
            print(data.decode())
        except:
            break


def scopri_e_connetti():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.sendto(b"PAIRING_REQUEST", (MULTICAST_GROUP, PORTA_DISCOVERY))

    data, _ = sock.recvfrom(1024)
    risposta = json.loads(data.decode())

    server_ip = risposta["server_ip"]
    tcp_port = risposta["tcp_port"]

    nome = input("Inserisci il tuo nome: ")

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.connect((server_ip, tcp_port))

    tcp.sendall(json.dumps({
        "type": "REGISTER",
        "name": nome
    }).encode())

    threading.Thread(target=ricevi, args=(tcp,), daemon=True).start()

    while True:
        msg = input()
        tcp.sendall(msg.encode())


if __name__ == "__main__":
    scopri_e_connetti()