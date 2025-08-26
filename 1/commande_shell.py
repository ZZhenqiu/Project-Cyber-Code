import subprocess

# Lancer "dir"
result_dir = subprocess.run(["cmd", "/c", "dir"], capture_output=True, text=True)
print("Résultat de dir :")
print(result_dir.stdout)

# Lancer "whoami"
result_whoami = subprocess.run(["whoami"], capture_output=True, text=True)
print("Résultat de whoami :")
print(result_whoami.stdout)
