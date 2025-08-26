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



"""Ok, maintenant, pourquoi tout ça ? Car le fonctionnement de nmap repose sur des TCP connect scans. C’est ce que nous voulons reproduire avec Python. Nous utilisons donc ici socket + connect pour l’ouverture d’une connexion TCP. 

Cette ligne : sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

Est interprétée de la sorte : socket.socket() permet de créer un nouveau socket. 
Les deux arguments sont AF_INET pour désigner la famille d’adresse (IPV4) et SOCK_STREAM (TCP).

Ce qui veut dire qu’ici, notre scanner ne fonctionne pas avec IPV6, UDP etc etc… 
Ah, et pourquoi un socket ? 

Car un scan de ports repose sur la communication réseau. En informatique, il y a forcément un endroit où il faut recevoir et envoyer des paquets. 
En Python, pour coder un scanner, il faut passer par les sockets, car c’est l’unique interface standardisée (à ma connaissance) que le système d’epxloitation fournit pour parler au réseau (au niveau user). 

Pour développer un peu, un système d’exploitation doit offrir aux programmes utilisateurs (Python, C) une API (app programming interface) pour accéder aux ressources matérielles, ex : disque, mémoire, carte réseau…
Pour le disque, nous avons les API fichiers (open, read, write)
Pour le réseau, nous avons les API sockets (socket, bind, connect, send, recv). 
API processus : fork, exec… 

Car le programme ne peut pas parler directement au matériel, donc le système d’exploitation fournit des API standardisées pour tout le monde. 
Ces API sont exposées par le noyau sous dorme d’appels systèmes. 

Historiquement, cette API vient de BSD Unix en 1993. Depuis, tous les OS modernes l’ont adoptée. 

Maintenant, quelle que soit la langue, les sockets sont le passage obligé car le noyau gère la pile TCP/IP et expose une seule interface, le socket. 

C’est une mesure de sécurité car si chaque programme pouvait directement parler au matériel -> conflits d’accès, pas de sécurité etc etc. 
Le noyau est la couche logicielle centrale qui contrele l’accès au matériel, arbitre les ressources etc etc. 

Enfin, comme nous demandons une action au noyau, il faut soit etre en mode privilégie, soit faire un appel système. Comme nous sommes sur Python (haut niveau), il se passe la chose suivante : 

Nous passons par l’API socket de Python. Ce dernier va appeler la libc en interne, qui effectuera le Syscall, et enfin, le noyau suivra les instructions (initialiser la pile TCP/IP). 
Par conséquent, la fonction socket() est un wrapper autour du syscall sys_socket. 

"""