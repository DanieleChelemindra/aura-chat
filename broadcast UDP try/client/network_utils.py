import socket
import ipaddress

def get_local_ip():
    """Restituisce l'IP locale principale"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()

def get_broadcast_ip(netmask="255.255.255.0"):
    """
    Calcola l'IP di broadcast automaticamente.
    Netmask di default /24 (la più comune).
    """
    local_ip = get_local_ip()
    network = ipaddress.IPv4Network(f"{local_ip}/{netmask}", strict=False)
    return str(network.broadcast_address)