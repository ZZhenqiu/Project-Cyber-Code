import requests

url = "http://testphp.vulnweb.com"

wordlist = [
    "admin",
    "images",
    "uploads", 
    "login",
    "css",
    "includes"
]

print (f" Scan {url}... ")

for word in wordlist:
    test_url = url.rstrip("/") + "/" + word
    try:
        response = requests.get(test_url, timeout=5)
        if response.status_code == 200:
            print(f"[200] Found : {test_url}")
        elif response.status_code == 403:
            print(f"[403] : {test_url}")
    except requests.RequestException as e:
        print(f"[!] Error with {test_url}: {e}")


"""
Pour Gobuster, le fonctionnement est plutôt compréhensible. Il s'agit d'envoyer une requête HTTP (GET)
à chacune des urls créés par la wordlist et il faudra regarder la réponse HTTP. 
Et sur Python, la librairie requests permet de faire ces requêtes HTTP. 

Mais maintenant, je suis face à un problème : l'utilisation de librairie permet de simplifier énormément les choses
(une ligne suffit), mais rend la chose beaucoup plus abstraite. Nous pourrions penser à faire cela en C aussi. 
Cela pourrait être une idée interessante pour le futur : refaire tous les programmes, cette fois-ci en C. 
Tips utile : j'avais des problèmes d'installation avec VsCode. Même en faisant pip/pip3 install, je rencontrais le message ModuleNotFoundError: No module named "". 
J'ai trouvé une solution qui marche : python3 -m pip install "". Cela permet de forcer l'installer sur le Python utilisé par VsCode et ça marche pour moi. 
"""