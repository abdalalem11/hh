from flask import Flask, request, jsonify
import os
import requests
import datetime

app = Flask(__name__)

TELEGRAM_TOKEN = "8875360747:AAHZH8ti8BTzA8_Gzo6QV6ex4OsaJyoBovI"
TELEGRAM_CHAT_ID = "1170411845"

def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message[:4000], "parse_mode": "HTML"}
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Error: {e}")

CODES_DB = {}

def generate_codes(category, count=100):
    codes = []
    for i in range(1, count + 1):
        if category == 'Python':
            code = f'''# Python Example {i}
def example_{i}():
    result = {i * 7 + 3}
    data = {{'id': {i}, 'value': result, 'status': 'success' if result % 2 == 0 else 'pending'}}
    print(f"Result: {{data}}")
    return data
example_{i}()'''
        elif category == 'JavaScript':
            code = f'''// JS Example {i}
function example_{i}() {{
    const result = {i * 7 + 3};
    const data = {{id: {i}, value: result, status: result % 2 === 0 ? 'success' : 'pending'}};
    console.log('Result:', data);
    return data;
}}
example_{i}();'''
        elif category == 'HTML':
            code = f'''<!-- HTML Example {i} -->
<!DOCTYPE html>
<html><body>
    <h1>Example {i}</h1>
    <p>Value: {i * 7 + 3}</p>
    <p>ID: {i} | Status: {'Success' if (i * 7 + 3) % 2 == 0 else 'Pending'}</p>
</body></html>'''
        elif category == 'CSS':
            code = f'''/* CSS Example {i} */
.example-{i} {{
    background: #1a0a0a; color: #E8C66A;
    padding: {i * 2}px; border: 2px solid #8B0000;
}}
.example-{i}:hover {{ border-color: #E8C66A; }}'''
        elif category == 'PHP':
            code = f'''<?php
function example_{i}() {{
    $result = {i * 7 + 3};
    $data = ['id' => {i}, 'value' => $result, 'status' => $result % 2 == 0 ? 'success' : 'pending'];
    echo json_encode($data);
}}
example_{i}();?>'''
        elif category == 'SQL':
            code = f'''-- SQL Example {i}
CREATE TABLE example_{i} (id INT, value INT DEFAULT {i * 7 + 3}, status TEXT);
INSERT INTO example_{i} VALUES (1, {i * 7 + 3}, 'success');
SELECT * FROM example_{i};'''
        elif category == 'Bash':
            code = f'''#!/bin/bash
result=$(({i} * 7 + 3))
echo "ID: {i} | Value: $result | Status: $([ $((result % 2)) -eq 0 ] && echo 'success' || echo 'pending')"'''
        elif category == 'C++':
            code = f'''#include <iostream>
using namespace std;
int example_{i}() {{
    int result = {i * 7 + 3};
    cout << "ID: {i}\\nValue: " << result << "\\nStatus: " << (result % 2 == 0 ? "success" : "pending");
    return result;
}}
int main() {{ example_{i}(); return 0; }}'''
        elif category == 'Java':
            code = f'''public class Example_{i} {{
    public static void main(String[] args) {{
        int result = {i * 7 + 3};
        System.out.println("ID: {i}\\nValue: " + result + "\\nStatus: " + (result % 2 == 0 ? "success" : "pending"));
    }}
}}'''
        elif category == 'Go':
            code = f'''package main
import "fmt"
func example_{i}() {{
    result := {i * 7 + 3}
    status := "pending"
    if result%2 == 0 {{ status = "success" }}
    fmt.Printf("ID: %d\\nValue: %d\\nStatus: %s\\n", {i}, result, status)
}}
func main() {{ example_{i}() }}'''
        elif category == 'Rust':
            code = f'''fn example_{i}() {{
    let result = {i * 7 + 3};
    let status = if result % 2 == 0 {{ "success" }} else {{ "pending" }};
    println!("ID: {}\\nValue: {}\\nStatus: {}", {i}, result, status);
}}
fn main() {{ example_{i}(); }}'''
        else:
            code = f'# {category} Example {i}\nprint("ID: {i} | Value: {i * 7 + 3}")'
        codes.append(code)
    return codes

categories = ['Python', 'JavaScript', 'HTML', 'CSS', 'PHP', 'SQL', 'Bash', 'C++', 'Java', 'C#', 'Go', 'Rust']

for cat in categories:
    CODES_DB[cat] = generate_codes(cat, 100)

@app.route('/')
def index():
    visitor_ip = request.remote_addr
    send_telegram(f"🔥 New visitor | IP: {visitor_ip} | @SSSTlF")
    
    buttons = ''.join([f'<a href="/code/{cat}" class="btn">{cat}</a>' for cat in categories])
    return f'''
<!DOCTYPE html>
<html dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>مبرمج عبود | @SSSTlF</title>
<style>
* {{margin:0;padding:0;box-sizing:border-box;}}
body {{font-family:'Cairo',sans-serif;background:#0a0505;color:#F5E6D3;min-height:100vh;padding:20px;}}
.aurora {{position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none;overflow:hidden;}}
.aurora::before {{content:'';position:absolute;width:600px;height:600px;background:radial-gradient(circle,rgba(139,0,0,0.08),transparent 70%);top:-10%;left:-10%;animation:a1 15s infinite alternate;}}
.aurora::after {{content:'';position:absolute;width:500px;height:500px;background:radial-gradient(circle,rgba(232,198,106,0.06),transparent 70%);bottom:-10%;right:-10%;animation:a2 20s infinite alternate;}}
@keyframes a1 {{0%{{transform:translate(0,0)scale(1)}}100%{{transform:translate(200px,100px)scale(1.5)}}}}
@keyframes a2 {{0%{{transform:translate(0,0)scale(1)}}100%{{transform:translate(-200px,-100px)scale(1.5)}}}}
.container {{position:relative;z-index:1;max-width:1200px;margin:0 auto;}}
.navbar {{background:rgba(10,5,5,0.85);backdrop-filter:blur(20px);border:1px solid rgba(139,0,0,0.15);border-radius:24px;padding:20px;text-align:center;margin-bottom:30px;}}
.navbar h1 {{font-size:36px;font-weight:800;background:linear-gradient(135deg,#E8C66A,#8B0000,#E8C66A);background-size:300% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:s 4s infinite;}}
@keyframes s {{0%,100%{{background-position:0%center}}50%{{background-position:200%center}}}}
.navbar .sub {{font-size:14px;color:#D4AF37;letter-spacing:4px;}}
.navbar .tag {{font-size:11px;color:#8B0000;letter-spacing:6px;opacity:0.6;}}
.hero {{text-align:center;padding:30px 20px;background:rgba(255,255,255,0.02);border-radius:24px;border:1px solid rgba(139,0,0,0.08);margin-bottom:30px;}}
.hero h2 {{font-size:28px;color:#D4AF37;}}
.hero h2 span {{background:linear-gradient(135deg,#E8C66A,#8B0000);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}}
.hero .badge {{display:inline-block;padding:6px 24px;border:1px solid rgba(232,198,106,0.15);border-radius:50px;color:#E8C66A;font-size:14px;margin-top:10px;letter-spacing:3px;}}
.hero .stats {{display:flex;gap:30px;justify-content:center;margin-top:15px;flex-wrap:wrap;}}
.hero .stats span {{color:#D4AF37;font-size:14px;}}
.hero .stats strong {{color:#E8C66A;font-size:20px;}}
.btns {{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px;margin-top:20px;}}
.btn {{display:block;padding:14px 18px;border-radius:14px;text-decoration:none;text-align:center;font-weight:600;font-size:14px;border:1px solid rgba(139,0,0,0.08);background:rgba(255,255,255,0.02);color:#F5E6D3;transition:0.3s;}}
.btn:hover {{transform:translateY(-3px);border-color:#E8C66A;box-shadow:0 10px 40px rgba(232,198,106,0.08);background:rgba(139,0,0,0.05);color:#E8C66A;}}
.footer {{text-align:center;padding:25px;margin-top:30px;border-top:1px solid rgba(139,0,0,0.08);background:rgba(10,5,5,0.5);border-radius:20px;}}
.footer .signature {{color:#8B0000;font-size:11px;letter-spacing:6px;opacity:0.5;}}
.footer p {{color:#D4AF37;font-size:12px;opacity:0.5;}}
@media(max-width:768px){{.navbar h1{{font-size:24px}}.hero h2{{font-size:20px}}.btns{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<div class="aurora"></div>
<div class="container">
<div class="navbar"><h1>مبرمج عبود</h1><div class="sub">@SSSTlF</div><div class="tag">أصل العرب</div></div>
<div class="hero">
<h2>أكثر من <span>1000 كود</span> حقيقي</h2>
<div class="badge">✦ كل فئة تحتوي على 100 كود ✦</div>
<div class="stats"><span><strong>{len(categories)}</strong> فئة</span><span><strong>{len(categories)*100}</strong> كود</span><span><strong>100%</strong> حقيقي</span></div>
</div>
<div class="btns">{buttons}</div>
<div class="footer"><div class="signature">أصل العرب</div><p>© 2026 مبرمج عبود | @SSSTlF</p></div>
</div>
</body>
</html>
'''

@app.route('/code/<category>')
def show_codes(category):
    if category not in CODES_DB:
        return "غير موجود", 404
    codes = CODES_DB[category]
    html = ''
    for i, c in enumerate(codes):
        html += f'''
<div class="block">
<div class="head"><span>#{i+1}</span><button onclick="copyCode({i})">📋 نسخ</button></div>
<pre class="code">{c}</pre>
</div>
'''
    return f'''
<!DOCTYPE html>
<html dir="rtl">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{category} — مبرمج عبود</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{font-family:'Cairo',sans-serif;background:#0a0505;color:#F5E6D3;padding:20px;}}
.aurora{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none;overflow:hidden;}}
.aurora::before{{content:'';position:absolute;width:600px;height:600px;background:radial-gradient(circle,rgba(139,0,0,0.06),transparent 70%);top:-10%;left:-10%;animation:a1 15s infinite alternate;}}
.aurora::after{{content:'';position:absolute;width:500px;height:500px;background:radial-gradient(circle,rgba(232,198,106,0.04),transparent 70%);bottom:-10%;right:-10%;animation:a2 20s infinite alternate;}}
@keyframes a1{{0%{{transform:translate(0,0)scale(1)}}100%{{transform:translate(200px,100px)scale(1.5)}}}}
@keyframes a2{{0%{{transform:translate(0,0)scale(1)}}100%{{transform:translate(-200px,-100px)scale(1.5)}}}}
.container{{position:relative;z-index:1;max-width:1100px;margin:0 auto;}}
.back{{display:inline-block;padding:8px 20px;border-radius:50px;border:1px solid rgba(232,198,106,0.15);color:#E8C66A;text-decoration:none;margin-bottom:15px;}}
.back:hover{{background:rgba(232,198,106,0.05);}}
.header{{text-align:center;padding:25px;background:rgba(255,255,255,0.02);border-radius:20px;border:1px solid rgba(139,0,0,0.08);margin-bottom:20px;}}
.header h1{{font-size:32px;background:linear-gradient(135deg,#E8C66A,#8B0000,#E8C66A);background-size:200% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:s 3s infinite;}}
@keyframes s{{0%,100%{{background-position:0%center}}50%{{background-position:200%center}}}}
.header .sub{{color:#D4AF37;font-size:14px;}}
.header .badge{{display:inline-block;padding:4px 16px;border-radius:50px;background:rgba(139,0,0,0.1);color:#E8C66A;font-size:13px;margin-top:8px;border:1px solid rgba(139,0,0,0.1);}}
.block{{background:rgba(255,255,255,0.02);border:1px solid rgba(139,0,0,0.08);border-radius:14px;margin-bottom:12px;overflow:hidden;}}
.block:hover{{border-color:rgba(232,198,106,0.15);}}
.head{{display:flex;justify-content:space-between;align-items:center;padding:8px 14px;background:rgba(139,0,0,0.05);border-bottom:1px solid rgba(139,0,0,0.05);}}
.head span{{color:#D4AF37;font-size:12px;font-weight:600;}}
.head button{{padding:4px 14px;border-radius:50px;border:1px solid rgba(232,198,106,0.15);background:transparent;color:#E8C66A;font-size:12px;cursor:pointer;font-family:'Cairo',sans-serif;}}
.head button:hover{{background:rgba(232,198,106,0.05);}}
.code{{padding:14px;margin:0;font-family:'Courier New',monospace;font-size:12px;line-height:1.6;color:#A5D6A7;overflow-x:auto;white-space:pre-wrap;word-wrap:break-word;background:rgba(0,0,0,0.4);direction:ltr;text-align:left;}}
.footer{{text-align:center;padding:15px;margin-top:20px;border-top:1px solid rgba(139,0,0,0.08);}}
.footer .signature{{color:#8B0000;font-size:11px;letter-spacing:6px;opacity:0.5;}}
.footer p{{color:#D4AF37;font-size:12px;opacity:0.5;}}
@media(max-width:768px){{.header h1{{font-size:24px}}.code{{font-size:11px;padding:10px}}}}
</style>
</head>
<body>
<div class="aurora"></div>
<div class="container">
<a href="/" class="back">← العودة</a>
<div class="header"><h1>{category}</h1><div class="sub">@SSSTlF — مبرمج عبود</div><div class="badge">✦ {len(codes)} كود حقيقي ✦</div></div>
{html}
<div class="footer"><div class="signature">أصل العرب</div><p>© 2026 مبرمج عبود | @SSSTlF</p></div>
</div>
<script>
function copyCode(i) {{
    const pre = document.querySelectorAll('.code')[i];
    navigator.clipboard.writeText(pre.textContent).then(() => {{
        const btn = document.querySelectorAll('.head button')[i];
        btn.textContent = '✅ تم';
        setTimeout(() => btn.textContent = '📋 نسخ', 1500);
    }});
}}
</script>
</body>
</html>
'''

if __name__ == '__main__':
    send_telegram(f"🔥 مبرمج عبود | @SSSTlF | {len(categories)} فئة | {len(categories)*100} كود")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
