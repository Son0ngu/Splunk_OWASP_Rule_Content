import requests, time, random
TARGET = 'http://localhost:8080/'
COOKIES = {'PHPSESSID': '278ab58002dbd5f0e20387685d3f6a8e', 'security': 'low'}
PAYLOADS = [
    # --- Common Environment & Configs ---
    '.env', '.env.backup', '.env.dev', '.env.local', '.env.prod',
    'config.php.bak', 'config.php.old', 'config.inc', 'wp-config.php.bak',
    'settings.py', 'settings.json', 'appsettings.json', 'parameters.yml',
    
    # --- Database Backups & Dumps ---
    'backup.sql', 'db_backup.sql', 'dump.sql', 'database.sqlite', 'database.sqlite3',
    'database.db', 'db.sqlite', 'backup.tar.gz', 'backup.zip',
    
    # --- SSH / Version Control / Git Exposure ---
    'id_rsa', 'id_rsa.pub', 'known_hosts', 'authorized_keys', '.ssh/id_rsa',
    '.git/config', '.git/HEAD', '.git/logs/HEAD', '.svn/entries', '.hg/entries',
    
    # --- Cloud, Infrastructure & Java/Spring Contexts ---
    '.aws/credentials', '.aws/config', 'aws_access_keys.csv', 
    'docker-compose.yml', 'Dockerfile', 'web.config', 'Web.config',
    '/WEB-INF/classes/applicationContext.xml', '/WEB-INF/web.xml', '/WEB-INF/spring-mvc.xml',
    'sftp-config.json', 'ftp.txt', '.bash_history', '.mysql_history'
]
print('--- A02: Cryptographic Failures / Sensitive Data Exposure ---')
for p in PAYLOADS:
    res = requests.get(TARGET + p, cookies=COOKIES)
    print(f'[*] Checked file: {p} -> Status: {res.status_code}')
    time.sleep(random.uniform(0.5, 1.5))
