import requests
from urllib.parse import quote

BASE = "http://10.10.120.218:1337/"
WORDLIST = "common.txt"
TIMEOUT = 3.0

sess = requests.Session()
sess.headers.update({"User-Agent": "fuzzer/1.0"})

with open(WORDLIST, "r", errors="ignore") as f:
    for line in f:
        w = line.strip()
        if not w:
            continue
        for path in (w, "hmr_" + w):
            safe = quote(path)
            target = BASE + safe
            try:
                r = sess.get(target, timeout=TIMEOUT, allow_redirects=True)
            
            except requests.RequestException:
                continue

            if r.status_code == 404:
                continue

            print(f"{r.status_code} {r.url}")




"""
Ce scrip a aidé pour le CTF "Hammer" de TryHackMe. 
Nous avons trouvé l'information suivante en commentaire HTML : 
"Dev Note: Directory naming convention must be hmr_DIRECTORY_NAME". 

De ce fait, un gobuster classique ne suffisait pas, il fallait effectuer une recherche
de directory avec hmr_[directory]. En bref, un fuzzing. 
Nous en avons profité pour modifier notre code gobuster initial, en y intégrant notamment
une wordlist (common.txt) et en utilisant quote() pour échapper les espaces et cractères 
spéciaux (sans cela, j'ai eu un message d'erreur). Par exemple, un espace devient %20. 

Ce qui change ici : 
sess = requests.Session() : permet de réutiliser une connexion plutot que d'ouvrir une nouvelle
connexion TCP à chaque fois. 

sess.headers.update({"User-Agent": "fuzzer/1.0"}) : nous mettons un User Agent car parfois, 
certains serveurs bloquent ou renvoient des pages différentes selon le User Agent. 


La prochaine fois, nous ajouterons du argparse pour plus de modularité dans le code. Ici, nous
voulons simplement que le scrip fonctionne correctement. 
Cela veut aussi dire que cette partie sera modifiée. 
for path in (w, "hmr_" + w):

"""