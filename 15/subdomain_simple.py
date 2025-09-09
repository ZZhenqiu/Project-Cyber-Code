import requests
import sys

list = open("subdomain.txt").read() 
subdomains = list.splitlines() 

for sub in subdomains: 
    sub_domains = f"http://{sub}.{sys.argv[1]}"

    try:
        response = requests.get(sub_domains) 
        
        if response.status.code == 200:
            print(f"[+] Trouvé : {sub}")
    except requests.ConnectionError:
        pass

"""
Penser à regarder pourquoi utiliser des outils différents pour énumération de dir et subdomains. 
En effet, souvent nous utilisons gobuster pour le premier et wfuzz ou ffuf pour le second. Alors qu'au final, la logique semble être la même, il y a
seulement le terme à FUZZ que nous devons mettre au dessus. 
Donc voir différence entre les deux. 
"""

