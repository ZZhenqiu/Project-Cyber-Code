import socket

target = "10.10.185.161"
ports = range(1,101)
timeout = 1.0

for port in ports: 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    result = s.connect_ex((target, port))

    if result == 0: 
        print (f"Port {port:2d} : OPEN")
        banner = s.recv(1024)
        if banner:
            print("   Banner : ", banner.decode(errors="replace").strip())
        else: 
            print("   Banner : nope.")
    else:
        print(f"Port {port:2d} : CLOSED / FILTERED")

    s.close()


"""
Ce code a été utilisé pour le CTF "The server from hell". 
Il fallait à un moment donné énumérer toutes les bannières des 100 premiers ports. 
Voici une partie de l'output : 

Port 19 : OPEN
   Banner :  550 12345 0ff70008fc77f7000000f80008f8000007f0000000000000888ff00
Port 20 : OPEN
   Banner :  550 12345 0ff0008f00008ffc787f70000000000008f000000087fff8088cf00
Port 21 : OPEN
   Banner :  550 12345 0f7000f800770008777 go to port 12345 80008f7f700880cf00
Port 22 : OPEN
   Banner :  550 12345 0f8008c008fff8000000000000780000007f800087708000800ff00
Port 23 : OPEN
   Banner :  550 12345 0f8008707ff07ff8000008088ff800000000f7000000f800808ff00


Nous pouvons donc constater que le port 22 a donné un indice pour la suite du CTF.
Concernant le code en lui-même, nous avons repris le code nmap du premier jour, que 
en y ajoutant la recherche de banner. 
banner = s.recv(1024) -> car recv lit les octets depuis la socket TCP. Et 1024 est la taille 
maximale lue en ocetst pour cet appel. 
Nous pourrions également effectuer une boucle while pour en capturer plus, dans le cas où une 
bannière serait plus grande (?). 

banner.decode(errors="replace").strip() -> (errors="replace") est là si des octets ne 
forment pas un encodage UTF-8 valide. Cela empêche l'arret du programme et mets juste un simbole à 
la place. errors=ignore marche aussi. 

Et .strip() permet de supprimer les espaces (\r et\n). 
Enfin, {port:2d} -> le 2d est une manière pour ajouter du padding. Pour 2 espaces, cela n'est pas 
utile mais c'était une occasion d'utiliser une autre méthode. Padding à gauche d'ailleurs. 

"""