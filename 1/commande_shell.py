import subprocess

commande = subprocess.run(["dir"], capture_output=True, text=True)
print("Donc : ")
print(commande.stdout)


"""""
Cet exercice n’aide pas vraiment au niveau de l’apprentissage de Python (il n’y a pas grand chose, d’autant plus que la plus value du programme est discutable). 
Toutefois, il m’aura permis de creuser un peu plus sur le fonctionnement des commandes shell. 
En effet, Python n’a pas la capacité d’exécuter des commandes systèmes directement. Il doit de ce fait passer par une API qui appelle les fonctions du système d’explotiation. C’est pour cette raison que nous devons utiliser la librairie subprocess, ou os.system. 
Ce blocage m’a permis de chercher un minimum le fonctionnement d’une commande simple comme “ls”. 
Selon ce que j’ai compris, lorsque nous mettons comme input “ls” sur un Linux, notre shell cherche l’exécutable correspondant : “/bin/ls” grâce à la variable $PATH.
Par la suite, le shell crée un nouveau processus en appelant le syscall fork() puis execve(“/bin/ls”, [“ls”], env). 
Enfin, “ls” s’exécute. Concrètement, c’est un binaire utilisé compilé en C qui : 
-ouvre le répertoire courant avec opendir() avec un syscall openat(). 
-lit les entrées de répertoire avec un syscall ) getdents64()
-écrit le résultat à l’écran avec un syscall write()
-une fois cela fait, il appelle exit avec un syscall exit_group(). 

Comment voir ça ? Avec la commande suivante : 
strace ls


Aborder ces points m’aura aidé à mieux appréhender certains points comme le rôle du $PATH, qui a d’ailleurs une utilité pour l’escalade de privilège, mais aussi de revoir des concepts étudiés en cours à Telecom Paris comme fork() et execve(). 
Si la théorie est utile, la pratique permet (pour mon cas) une meilleure compréhension. Ici, fork() est un syscall qui vise à dupliquer le processus courant, donc le shell. Pourquoi ? Car si le shell exécute “ls” dans son propre processus, il ne pourra plus continuer après. C’est la raison du fork, qui créera un processus enfant/une copie du shell qui va exécuter le ls tandis que le processus parent reste en attente. 
“execve()” est un syscall qui remplace le code rourant/le shell enfant par un autre programme, ici /bin/ls. Nous y renvoyons l’argument [“ls”], et la variable d’environnement. 
Enfin, rappelons que le processus parent/le shell original utilise waitpid() pour attendre que le processsus enfant ait fini. Ainsi, quand ls se termine avec le syscall exit_group(), le shell reprend la main. 

Note : en lisant des exemples de PATH, par exemple /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin , je me suis demandé, “mais si le PATH est dans /bin/ls, pourquoi avoir tous ces autres chemins et pas simplement /bin ? 

Il semblerait que la réponse soit historique et organisationnelle. En effet, chaque répertoire du $PATH a un rôle précis : 
/bin contient les programmes essentiels au démarrage et à l’utilisation minimale du système (ls, cp, cat, echo…)
/usr/bin contient la majorité des programmes utilisateurs standars (python3, gcc, vim)
/usr/sbin contient les utilitaires d’aministration (sshd, apache2, nginx)
/usr/local/bin contient les programmes installés manuellement par l’administrateur. 

Donc, pourquoi tous ces dossiers dans $PATH ? 
Premièrement, pour des raisons de compatbilité historique. Avant, /bin et /usr/bin était parfois sur des partitions séparées. 
Ensuite, cela permet une séparation claire : /bin concerne le minimum vital, /usr/bin pour les applications standars et /usr/local/bin les programmes personnels. 

Cela veut aussi dire que si nous limitons le path à /bin et non à /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin, notre système serait très limité (nous ne pourrions plus faire grand chose). 

Deuxième note : 
J’ai essayé de faire la même chose avec Windows (et “dir”), mais cela ne marchait pas. La raison était la suivante : “dir”, contraitement à “ls”, n’est pas un exécutable mais un builtin du programme “cmd.exe”. Donc, mettre uniquement “dir” reviendrait à chercher dir.exe dans C:\Windows\System32, qui n’existe pas. Il faut donc faire : subprocess.run(["cmd", "/c", "dir"]). Avec /c pour dire à cmd quelle commande exécuter"""