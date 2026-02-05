import socket
import json
import threading

SERVER_IP = input("inserisci IP server")
PORTA_TCP = 60000

def ricevi(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            print(data.decode())
        except:
            break

def connetti():
    nome = input("Inserisci il tuo nome: ")

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.connect((SERVER_IP, PORTA_TCP))

    tcp.sendall(json.dumps({
        "type": "REGISTER",
        "name": nome
    }).encode())

    threading.Thread(target=ricevi, args=(tcp,), daemon=True).start()

    while True:
        msg = input()
        tcp.sendall(msg.encode())

if __name__ == "__main__":
    connetti()
