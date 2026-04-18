import requests
import threading
import random
import time

# Cấu hình mục tiêu
BASE_URL = "http://localhost:8080"
# Lưu ý: Thay đổi PHPSESSID cho khớp với session hiện tại của bạn nếu DVWA yêu cầu đăng nhập hợp lệ
COOKIES = {'PHPSESSID': '278ab58002dbd5f0e20387685d3f6a8e', 'security': 'low'}

# Các đường dẫn bình thường trên một trang web để làm nhiễu log (không mang tính tấn công)
NORMAL_ENDPOINTS = [
    "/",
    "/index.php",
    "/about.php",
    "/instructions.php",
    "/dvwa/css/main.css",
    "/dvwa/images/logo.png",
    "/favicon.ico",
    "/setup.php"
]

# Giả mạo đa dạng người dùng để log phong phú
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0"
]

def send_normal_request():
    """Gửi một GET request bình thường đóng giả người dùng đang lướt web"""
    path = random.choice(NORMAL_ENDPOINTS)
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    
    try:
        # Request tải trang bình thường
        requests.get(BASE_URL + path, headers=headers, cookies=COOKIES, timeout=3)
        print(f"[*] Normal Request -> {path}")
    except requests.exceptions.RequestException:
        pass # Bỏ qua lỗi Timeout

def worker(num_requests):
    """Worker cho mỗi luồng"""
    for _ in range(num_requests):
        send_normal_request()
        # Delay ngẫu nhiên từ 0.05 đến 0.2s để giả lập tốc độ lướt web của người dùng
        time.sleep(random.uniform(0.05, 0.2)) 

def start_traffic_generation(threads_count=5, requests_per_thread=100):
    total = threads_count * requests_per_thread
    print(f"🚀 Bắt đầu tạo Traffic bình thường: Tổng {total} requests tới DVWA...")
    start_time = time.time()
    
    thread_list = []
    
    for _ in range(threads_count):
        t = threading.Thread(target=worker, args=(requests_per_thread,))
        t.start()
        thread_list.append(t)
        
    for t in thread_list:
        t.join()
        
    duration = round(time.time() - start_time, 2)
    print(f"✅ Hoàn thành giả lập {total} log người dùng bình thường trong {duration} giây!")
    print("👉 Hãy kiểm tra Splunk, bạn sẽ thấy hệ thống ghi nhận rất nhiều request tải css, trang chủ, ảnh... hợp lệ chứ Alert sẽ KHÔNG bị trigger.")

if __name__ == "__main__":
    # Cấu hình: 5 luồng x 100 requests = 500 dòng log hoàn toàn bình thường được đổ vào Splunk
    start_traffic_generation(threads_count=5, requests_per_thread=100)
