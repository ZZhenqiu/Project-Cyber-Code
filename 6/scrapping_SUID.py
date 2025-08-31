import requests
from bs4 import BeautifulSoup

url = "https://gtfobins.github.io/#+suid"
print(f"[*] Récupération de {url}...")

resp = requests.get(url)
soup = BeautifulSoup(resp.text, "html.parser")

bins = [a.text.strip() for a in soup.select("a.bin-name")]

print(f"[+] {len(bins)} binaires SUID trouvés sur GTFOBins:\n")
for b in bins:
    print(b)

    """
    Pour l'installation, c'est pip3 install beautifulsoup4 requests
    """