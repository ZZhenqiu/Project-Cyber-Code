import keyboard
import time

events = keyboard.record(until='enter')

word = ""
words = [] 

for w in events: 
    if w.event_type == "down":
        if len(w.name) == 1:
            word += w.name
        elif w.name == "space":
            if word:
                words.append(word)
                word=""
        elif w.name == "enter":
            if word: 
                words.append(word)
            break


with open("23/test.txt", "a", encoding="utf-8") as f: 
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(w.time))
        f.write(f"[{t}] {' '.join(words)}\n")

print("Fait") 

"""
Un problème présent dans le code d'hier, c'est qu'il enregistrait 
lettre par lettre, ce qui donnait des choses qui devenaient assez rapidement
illisibles. Par exemple : 
b
o
n
j
o
u
r

Ou quelque chose comme cela. Pour modifier cela, nous ajoutons une 
logique qui considère que chaque touche espace pressée correspond à
la fin d'un mot. 
Nous avons également ajouté la création d'un output dans un fichier 
test.txt. 
"""