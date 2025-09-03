import platform
import os

os_type = platform.system().lower()

print(f"Bref, le système : {os_type} ")

if "linux" in os_type:
    cmd = "ls"
elif "windows" in os_type:
    cmd = "dir"
else:
    cmd = "???"

print(f"Donc, voici la commande : {cmd}\n")
os.system(cmd)


"""
Ok, ce script est très simple voire simpliste. Mais il est utile car nous pourrons l'utiliser dans le futur pour automatiser en fonction de l'OS. 
Par exemple, la phase d'énumération manuelle en Linesc/Winesc est différente, donc utilité ici. 
Contre point : cela suppose que la machine cible ait les librairies platform et os, ce qui n'est pas certain. Nous avons eu un problème similaire
avec gtfobins et le fait que les machines cibles (sur THM) n'ont pas de connexion internet. 
à voir donc comment faire. 

Enfin, nous arrivons sur une période où TryHackMe organise un event. Plus tu termines de room, plus tu gagnes des tickets. Donc pour les jours suivants, 
je vais principalement me concentrer sur la résolution de CTFs. 
"""