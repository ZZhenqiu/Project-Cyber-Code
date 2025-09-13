import hashlib

wordlist = str(input('wordlist : '))
hash = str(input('Hash : '))

with open(wordlist, 'r') as file: 
    for line in file.readlines():
        hash_ob = hashlib.md5(line.strip().encode()) 
        hashed_pass = hash_ob.hexdigest() 
        if hashed_pass == hash:
            print("Ok : " + line.strip())
            exit(0)


"""
Bref, un classique, on commence par du md5 car c'est le plus commun dans les CTFs. 
L'idée est la suivante : en raison du one wayness d'un hash, nous devons hasher 
nous-même des mdps (avec la wordlist) et ensuite regarder s'il y a une correspondance
entre les deux. 

Maintenant, plusieurs choses sont à améliorer : 
-la rapidité (question difficile pour Python)
-les autres protocoles (il y en a beaucoup, donc à voir comment implémenter cela)
-la reconnaissance d'un hash, car ici, nous partons du principe que le hash correspond à 
du md5
"""