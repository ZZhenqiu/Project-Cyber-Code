import socket

target = "scanme.nmap.org"

ports = [22, 80, 443, 8080]

print(f"Bref, scan de {target} sur les ports {ports}\n")

for port in ports:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((target, port))

    if result == 0:
        print(f"Port {port} : OPEN")
    
    else: 
        print(f"Port {port} : Closed / filtered")
    sock.close