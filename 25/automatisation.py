import sys
import subprocess
import webbrowser

IP = sys.argv[1] if len(sys.argv) > 1 else input("IP : ")

subprocess.Popen(["nmap","-p-", "-A", IP])

subprocess.Popen([
    "gobuster", "dir",
    "-w", "/usr/share/wordlists/dirb/common.txt",
    "-u", f"http://{IP}"
])

subprocess.Popen(["burp", "suite"])

webbrowser.open(IP)

print("Voilà. ")


"""
Bon, ce code là est principalement du QoL. Il sert à m'éviter de devoir faire les 
mêmes commandes à chaque début de CTF. 
Pratique car le process est toujours le même (sauf exception), à savoir nmap, gobuster,
burp suite et analyse manuelle du site. 

Nous rajouterons des choses (par exemple le crawl + récupération de fichiers grâce à dirb),
mais aussi, il faudra corriger un problème technique : utiliser ce code nous empêche d'écrire
sur le terminal actuel. Ce qui fait que nous devons en ouvrir un autre. 
Trouver la raison de ce problème. 

Ensuite, s'entraîner avec les librairies pour nmap/gobuster pour améliorer les fonctionalités 
et ensuite intégrer notre code au lieu d'utiliser les outils. 

"""