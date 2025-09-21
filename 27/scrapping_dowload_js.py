import os
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

target = input("IP :").strip()

base = "http://" + target

resp = requests.get(base, timeout=6)
html = resp.text

soup = BeautifulSoup(html, "html.parser")
scripts = soup.find_all("script", src=True)

os.makefirs("js_files", exist_ok=True)

count = 0
for tag in scripts:
    src = tag["src"]
    full_url = urljoin(base, src)
    try:
        r = requests.get(full_url, timeout=6)
        if r.status_code == 200:
            path = urlparse(full_url).path
            name = os.path.basename(path) or f"script_{count}.js"
            out_path = os.path.join("js_files", name)

            if os.path.exists(out_path):
                base_name, ext = os.path.splitext(name)
                out_path = os.path.join("js_files", f"{base_name}_{count}[ext]")

            with open(out_path, "wb") as f:
                f.write(r.content) 
                print(f"Ok : {full_url} -> {out_path}")
                count+=1
        else: 
            print(f"Nope : {full_url}, {r.status_code}")
    except Exception as e:
        print(f"Erreur : {e}")

if count == 0:
    print("Rien ici")
else: 
    print("Fait : {count} fichier(s) dans ./js_files")


"""
Le code d'ajourd'hui permet de scrapper une IP, de détecter la présence de fichiers js, puis de les télécharger. 
Améliorations futures : 
-télécharger d'autres extensions (ex php)
-améliorer le script gobuster pour recherche récursive de directories -> nous trouvons un chemin, 
le script refait une recherche mais avec le nouveau lien. Et à chaque fois, nous scrappons le site 
pour voir la présence de fichiers. 
-Peut être aussi prendre le HTML de base. Cela nous évitera de l'analyser avec Burp ou Inspect. 

Sinon, ce projet nous a également montré la nécessité d'organisation. En effet, jusqu'à 
présent, nous avons affiché les outputs directement sur le terminal. Mais au fur et à mesure que 
nous ajoutons de nouvelles fonctionnalités, cela deviendra illisible. 
De ce fait, l'idée sera, pour le code final, de créer un dossier avec dedans tous les outputs par 
catégorie. Par exemple, un sous folder nmap etc etc... 
Cela prendra son sens avec l'approche résursive et cela sera utile pour documenter les différentes phases, 
vu que nous avons déjà créé un folder. 
"""