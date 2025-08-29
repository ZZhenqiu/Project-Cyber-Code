import subprocess
import requests
import time

whitelist = {
    "/usr/bin/passwd",
    "/usr/bin/sudo",
    "/usr/bin/chsh",
    "/usr/bin/chfn",
    "/usr/bin/newgrp",
    "/usr/bin/gpasswd",
    "/bin/su"
}

print("[*] Début ")
start = time.time() 

cmd = ["find", "/", "-perm", "-u=s", "-type", "f"]
result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
suid_bins= result.stdout.splitlines()

elapsed = time.time() - start

candidates = [binpath for binpath in suid_bins if binpath not in whitelist]

if not candidates:
    print("[!] Aucun binaire intéressant trouvé hors whitelist.")
    exit(0)

print(f"[*] {len(candidates)} binaires hors whitelist détectés.\n")

for idx, binpath in enumerate(candidates, 1):
    url=f"https://gtfobins.github.io/gtfobins/{name}/"

    try:
        resp=requests.get(url, timeout=5)
        if resp.status_code==200 and "SUID" in resp.text:
            status="Trouvé"
        else:
            status = "Pas trouvé"
    
    except requests.RequestException:
        "Erreur"
    
    print(status + f" -> {url}")


"""
L'idée cette fois-ci est la suivante : 
En phase de privilege escalation, la partie reconnaissance est primordiale. En tant que débutant, le mieux est d'effectuer cette reconnaissance manuellement
puis, si rien n'est trouvé, de passer sur des outils automatisés comme Linpeas. 
Deux grands classiques de l'énumération manuelle est sudo -l et le SUID. 

Pour SUID, nous voulons créer un script qui exécute la commande shell (nous allons nous servir de ce que nous avons effectué Jour 1) et qui analyse
l'output : 
-En analysant les résultats, il va les comparer avec une recherche Internet pour voir si le programme est répertorié dans GTFOBINS. Si oui -> afficher.
-Nous créerons un tableau rassemblant tous les programmes pour qui le bit SUID est normal. Si trouve -> ne pas afficher
-Enfin, tous les programmes non répertoriés / inconnus seront affichés avec un message "inconnu" et il faudra effectuer une recherche internet. 

Il est aussi possible (et même plus optimal) de créer une liste pour les programmes répertoriés dans GTFOBINS, cela éviterait de faire une recherche 
pour chaque programme. Nous pouvons même imaginer un dictionnaire avec le programme et la commande donnée par le site. 
C'est l'approche qui sera adoptée pour la version "améliorée". La version simple nous permettra surtout de travailler le scaping avec Python. 


Update : ok, en faisant cela, je me suis heurté à deux problèmes : 
-le premier est la cohérence des noms. Dans ce CTF, le programme qui a le bit SUID est "python 2.7". Or, la seule recherche qui marche dans gtfobins 
est "python". Mettre le 2.7 donnera une absence de réponse, et donc un faux négatif. Nous pouvons corriger cela facilement en enlever les extensions. 
-le deuxième problème, beaucoup plus important, est le fait que les machines victimes n'ont pas accès à internet. En effet, sur la machine attaquante
(donc la virtual box normale), le code marche sans problème, mais ce que nous voulons, c'est le faire fonctionner sur la machine victime. 
La solution serait donc d'avoir une solution en local (comment faire ?) ou bien, de créer une liste avec tous les noms de binaire de la page 
https://gtfobins.github.io/#+suid 
Comme ça, nous pourrons faire quelque chose. 
La correction serait donc la suivante : 
1) plutôt que de scraper le site, nous allons chercher une correspondance entre l'output de find / -perm -u=s -type f 2>/dev/null et la liste que 
créerons manuellement. 
2) Si correspondance il y a, mettre "Trouvé", avec le script à utiliser (faire un dictionnaire pour ça ?). Ensuite, il faudra chercher manuellement
sur internet si un exploit est possible (car gtfobins n'est pas exhaustif).
3) formatter correctement l'output de la recherche SUID pour avoir "python" et non "python 2.7"

Nous ferons ça demain. 
"""