from scapy.all import ARP, Ether, srp, conf

ip_range = "10.10.32.0/24" #à modifier bien sur 
interface = conf.iface   

packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_range)
ans, _ = srp(packet, timeout=2, iface=interface, inter=0.1, verbose=False)

print("IP".ljust(16), "MAC")
print("-" * 40)
for _, received in ans:
    print(received.psrc.ljust(16), received.hwsrc)


"""
Ok, partie intéressante, ce code permet de faire quelques rappels sur les réseaux. 
Premièrement, que fait ce script ? C'est un scan ARP sur un sous réseau donné (le notre en l'occurence). 
Il envoie une requête ARP broadcast pour chaque IP et récolte les réponses. Le but est d'obtenir une liste
des machines actives sur le LAN, avec les adresses IP et MAC. 
En bref, c'est un outil de cartographie du réseau local. Voici un exemple d'output sur notre VM TryHackMe :
IP             MAC 
------------------------------
10.10.32.63 02:7e:01:c1:03:ab 
10.10.32.89 02:2e:5c:5c:63:a5 
10.10.32.152 02:a5:ef:86:d4:c3 
10.10.32.165 02:e2:74:0d:70:2f 
10.10.32.182 02:b5:b9:40:0c:01 
10.10.32.231 02:5d:64:16:53:0d

Cela a une utilité aussi bien en red team (découverte de serveurs interessants comme AD, database etc etc, possible attaque 
ARP spoofing) mais aussi blue team (vérifier quelles machines sont connectées au réseau, détecter des appareils inconnus...) 
De plus, le scan ARP est pertinent car ce dernier est obligatoire dans un réseau Ethernet ou IPV4. Et contrairement au ping ICMP, 
qui peut être bloqué, les réponses ARP ne sont pas filtrées (ou en tout cas, pas facilement)

Maintenant, expliquons certaines lignes : 
Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_range). Ici le point important est le /. Pourquoi ? Car ARP est un protocole qui 
permet de trouver l'adresse MAC correspondant à une IP. Néanmoins, un paquet ARP doit ciruler sur le réseau physique (Ethernet par exemple). 
Par conséquent, il faut l'encapsuler dans une trame Ethernet, et c'est la signification de Ether() / ARP() -> une trame Ethernet contenenant
une requête ARP. Sans /, nous aurions simplement construit deux objets séparés. 

dst signifie l'adresse MAC de destination. Mettre ff:ff:ff:ff:ff:ff signifie l'adresse de broadcast, tout le monde sur le LAN reçoit la trame. 
pdst est l'IP ou la plage d'IP de requete. Par conséquent, Scapy génèrera une requête ARP pour chaque IP de cette plage. 

ans, _ = srp(packet, timeout=2, iface=interface, inter=0.1, verbose=False) -> srp veut dire send, receive, paquet (niveau 2). D'ailleurs, pour 
travailler sur la couche IP, nous utiliserons seulement sr. Cette partie permet donc d'envoyer nos paquets créés par la ligne précédente. Deux 
choses sont à noter, iface = interface, permet de forcer Scapy à utiliser le bon interface réseau, car sinon cela ne marche pas (à voir les 
différences sur une machine Windows), et inter=0.1 permet d'éviter d'envoyer 254 paquets d'un coup. 
Enfin, il y a "ans, _" car la fonction srp retourne deux listes, ans : les requêtes qui otn eu une réponse, et unans : les requetes n'ayant pas 
eu de réponse. _ est une convention Python pour dire d'ignorer cela. 

Nous l'utilisons une deuxième fois ici : for _, received in ans:
    print(received.psrc.ljust(16), received.hwsrc)
L'idée est que ans renvoit un couple de résultats : la requete envoyée, et la réponse reçue. Comme la requete envoyée ne nous intéresse pas, nous 
mettons "for _, received" pour ne récupérer que la seconde partie. Ensuite, psrc c'est protocol source address (l'IP qui a répondu), et hwsrc c'est
hardware source address, donc l'adresse MAC. 

Ah oui, et ljust(16) est juste du padding. Donc c'est l'équivalent de 16 espaces.

Note : from scapy.all import ARP, Ether, srp, conf. 
Pourquoi ? Car si nous mettons uniquement "import scapy", ça ne chargera que le module racine scapy. Ainsi, mettre ARP(...) renverra une erreur car 
ARP n'est pas défini. Une solution serait de mettre le chemin complet : 
import scapy.all
test = scapy.all.ARP(...), mais comme vous pouvez le constater, c'est plus lourd, surtout si notre code devient conséquent. 
Bref, une autre bonne pratique est d'importer seulement ce dont nous avons besoin. 
C'est d'ailleurs un principe similaire au "Need to Know" en cybersécurité. 

"""