import socket

PORTA_DISCOVERY = 50000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", PORTA_DISCOVERY))

print("Server in ascolto...")

while True:
    data, addr = sock.recvfrom(1024)
    print(f"Ricevuto da {addr}: {data}")