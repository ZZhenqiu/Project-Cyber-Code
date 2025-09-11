import requests 

url = "https://www.python.org/static/community_logos/python-logo.png"
r = requests.get(url, allow_redirects=True)

filename = url.split("/")[-1]

if r.status_code == 200:
    with open(filename, 'wb') as f:
        f.write(r.content)
    print("[+] OK")
else: 
    print("[!] Erreur : ", r.status_code)  


"""
Méthode simple pour télécharger un fichier, à la manière d'un wget. 
Rien de bien complexe, mais cela sera utile, combiné avec le code de commande shell
du premier jour pour automatiser la plupart des tâches. 
Donc à utiliser plus tard. 

Cependant, nous pouvons relever deux choses intéressantes. Premièrement, nous nous 
référons au Room "Python for Pentesters" de TryHackMe. Il y a un code de File Downloader
qui est le suivant : 

import requests
url = 'https://assets.tryhackme.com/img/THMlogo.png'
r = requests.get(url, allow_redirects=True)
open('THMlogo.png', 'wb').write(r.content)


Ce que nous pouvons noter de différent ici, c'est l'utilisation de "open" au lieu de 
"with open". La différence est qu'avec "open", il faut penser à fermer manuellement le 
fichier avec f.close(), car s'il reste ouvert en mémoire, cela peut provoquer certaines erreurs
comme des fuites de ressources. L'avantage de with open, c'est que Python gère automatiquement la
fermeture. 

Deuxièmement, cette ligne est intéressante filename = url.split("/")[-1], car le [-1] permet
de récupérer la dernière partie de l'url, donc le nom de l'image. 
La méthode .split découpe l'url en morceaux, séparés par "/" (donc "https", www.python.org, "static" etc etc)
Et, en Python, les indices négatifs comment à la fin de la liste, donc [-1] sélectionne le dernier élément.  

Le reste est principalement des ajouts esthétiques. 

Note à moi même : le slicing marche de la manière suivante mot_de_test[start:stop:step]. Step étant la manière, 
par exemple mot[::2] va prendre une lettre sur deux et mot[::-1] va inverser le mot. 

"""