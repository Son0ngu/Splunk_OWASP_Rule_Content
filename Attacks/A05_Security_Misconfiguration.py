import requests, time, random
TARGET = 'http://localhost:8080/'
COOKIES = {'PHPSESSID': '278ab58002dbd5f0e20387685d3f6a8e', 'security': 'low'}
PAYLOADS = [
    # --- Basic: Common Admin Panels & Info Disclosures ---
    'phpinfo.php', 'info.php', 'test.php', 'server-status', 'server-info',
    'admin/', 'administrator/', 'admin_login.php', 'login.php', 'dashboard/',
    
    # --- Medium: Frameworks, APIs, and Version Control Artifacts ---
    'actuator/health', 'actuator/env', 'actuator/heapdump', 
    'swagger-ui.html', 'api/docs', 'v2/api-docs',
    '.DS_Store', 'Thumbs.db', '.idea/workspace.xml', '__pycache__/',
    
    # --- Advanced: Application Diagnostics & Management Interfaces ---
    'trace.axd', 'elmah.axd', 'phpMyAdmin/', 'pma/', 
    'server-status?auto', 'jmx-console/', 'manager/html',
    'debug/default/view', 'wp-content/debug.log'
]
print('--- A05: Security Misconfiguration ---')
for p in PAYLOADS:
    res = requests.get(TARGET + p, cookies=COOKIES)
    print(f'[*] Scanned endpoint: {p} -> Status: {res.status_code}')
    time.sleep(random.uniform(0.5, 1.5))
