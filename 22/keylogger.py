import keyboard

keys = keyboard.record(until = 'ENTER')
keyboard.play(keys)

"""
Bon, nous avons repris le code fourni dans le Room Python for cybersecurity de 
TryHackMe. 
Comme vous le voyez, le code en lui même n'a que peu d'intérêt. 
Le but sera d'étudier la librairie pour améliorer le code. 

Il faudra à minima pouvoir stocker l'output dans un fichier et non juste dans le terminal. 
Une meilleure option serait d'envoyer l'output dans un serveur type C2 (à voir comment faire).
Penser aussi à la partie obstruction, et la partie delivery. 
"""