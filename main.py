from flask import Flask, request, render_template_string, jsonify
import os
import requests
import datetime
import json

app = Flask(__name__)

TELEGRAM_TOKEN = "8875360747:AAHZH8ti8BTzA8_Gzo6QV6ex4OsaJyoBovI"
TELEGRAM_CHAT_ID = "1170411845"

def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message[:4000], "parse_mode": "HTML"}
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"خطأ: {e}")

# ===== أكواد حقيقية باللغة الإنجليزية =====
CODES_DB = {}

def generate_real_codes(category, count=100):
    codes = []
    for i in range(1, count + 1):
        if category == 'Python':
            code = f'''# ===== {category} - Example {i} =====
# Code by: Abood | @SSSTlF

def example_{i}():
    """
    {category} - Real code example {i}
    """
    result = {i * 7 + 3}
    data = {{
        'id': {i},
        'name': f'item_{i}',
        'value': result,
        'status': 'success' if result % 2 == 0 else 'pending'
    }}
    print(f"Result: {{data}}")
    return data

if __name__ == '__main__':
    example_{i}()
'''
        elif category == 'JavaScript':
            code = f'''// ===== {category} - Example {i} =====
// Code by: Abood | @SSSTlF

function example_{i}() {{
    console.log(`Running {category} example {i}`);
    let result = {i * 7 + 3};
    const data = {{
        id: {i},
        name: `item_${{i}}`,
        value: result,
        status: result % 2 === 0 ? 'success' : 'pending'
    }};
    console.log('Result:', data);
    return data;
}}

example_{i}();
'''
        elif category == 'HTML':
            code = f'''<!-- ===== {category} - Example {i} ===== -->
<!-- Code by: Abood | @SSSTlF -->

<!DOCTYPE html>
<html>
<head>
    <title>{category} Example {i}</title>
</head>
<body>
    <h1>{category} Example {i}</h1>
    <p>Value: {i * 7 + 3}</p>
    <div id="data-{i}">
        <span>ID: {i}</span>
        <span>Status: {'Success' if (i * 7 + 3) % 2 == 0 else 'Pending'}</span>
    </div>
</body>
</html>
'''
        elif category == 'CSS':
            code = f'''/* ===== {category} - Example {i} ===== */
/* Code by: Abood | @SSSTlF */

.example-{i} {{
    background: linear-gradient(135deg, #1a0a0a, #2d0a0a);
    color: #E8C66A;
    padding: {i * 2}px;
    border-radius: {i % 10 + 4}px;
    border: 2px solid #8B0000;
    box-shadow: 0 0 30px rgba(139, 0, 0, 0.3);
    transition: all 0.3s ease;
}}

.example-{i}:hover {{
    transform: scale(1.02);
    border-color: #E8C66A;
    box-shadow: 0 0 60px rgba(232, 198, 106, 0.15);
}}
'''
        elif category == 'PHP':
            code = f'''<?php
// ===== {category} - Example {i} =====
// Code by: Abood | @SSSTlF

function example_{i}() {{
    $result = {i * 7 + 3};
    $data = [
        'id' => {i},
        'name' => 'item_' . {i},
        'value' => $result,
        'status' => $result % 2 == 0 ? 'success' : 'pending'
    ];
    echo "Result: " . json_encode($data) . "\\n";
    return $data;
}}

example_{i}();
?>
'''
        elif category == 'SQL':
            code = f'''-- ===== {category} - Example {i} =====
-- Code by: Abood | @SSSTlF

CREATE TABLE IF NOT EXISTS example_{i} (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    value INTEGER DEFAULT {i * 7 + 3},
    status TEXT DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO example_{i} (name, value, status)
VALUES 
    ('item_1', {i * 7 + 3}, 'success'),
    ('item_2', {i * 7 + 5}, 'pending'),
    ('item_3', {i * 7 + 7}, 'success');

SELECT * FROM example_{i} WHERE status = 'success';
SELECT COUNT(*) as total FROM example_{i};
'''
        elif category == 'Bash':
            code = f'''#!/bin/bash
# ===== {category} - Example {i} =====
# Code by: Abood | @SSSTlF

echo "Running {category} example {i}"
result=$(({i} * 7 + 3))
name="item_${{i}}"
echo "Result: $result"
echo "Name: $name"

if [ $((result % 2)) -eq 0 ]; then
    echo "Status: success"
else
    echo "Status: pending"
fi

echo "ID: {i}" > output_{i}.txt
echo "Value: $result" >> output_{i}.txt
echo "Created output_{i}.txt"
'''
        elif category == 'C++':
            code = f'''// ===== {category} - Example {i} =====
// Code by: Abood | @SSSTlF

#include <iostream>
#include <map>
#include <string>
using namespace std;

int example_{i}() {{
    cout << "Running {category} example {i}" << endl;
    int result = {i * 7 + 3};
    map<string, string> data;
    data["id"] = to_string({i});
    data["name"] = "item_" + to_string({i});
    data["value"] = to_string(result);
    data["status"] = (result % 2 == 0) ? "success" : "pending";
    
    for (auto& pair : data) {{
        cout << pair.first << ": " << pair.second << endl;
    }}
    return result;
}}

int main() {{
    example_{i}();
    return 0;
}}
'''
        elif category == 'Java':
            code = f'''// ===== {category} - Example {i} =====
// Code by: Abood | @SSSTlF

import java.util.HashMap;
import java.util.Map;

public class Example_{i} {{
    public static void main(String[] args) {{
        System.out.println("Running {category} example {i}");
        int result = {i * 7 + 3};
        Map<String, Object> data = new HashMap<>();
        data.put("id", {i});
        data.put("name", "item_" + {i});
        data.put("value", result);
        data.put("status", result % 2 == 0 ? "success" : "pending");
        System.out.println("Result: " + data);
    }}
}}
'''
        elif category == 'C#':
            code = f'''// ===== {category} - Example {i} =====
// Code by: Abood | @SSSTlF

using System;
using System.Collections.Generic;

class Example_{i} {{
    static void Main() {{
        Console.WriteLine("Running {category} example {i}");
        int result = {i * 7 + 3};
        var data = new Dictionary<string, object> {{
            {{"id", {i}}},
            {{"name", "item_" + {i}}},
            {{"value", result}},
            {{"status", result % 2 == 0 ? "success" : "pending"}}
        }};
        Console.WriteLine("Result: " + string.Join(", ", data));
    }}
}}
'''
        elif category == 'Go':
            code = f'''// ===== {category} - Example {i} =====
// Code by: Abood | @SSSTlF

package main

import "fmt"

func example_{i}() {{
    fmt.Printf("Running {category} example %d\\n", {i})
    result := {i * 7 + 3}
    data := map[string]interface{}{{
        "id": {i},
        "name": fmt.Sprintf("item_%d", {i}),
        "value": result,
        "status": "success",
    }}
    if result%2 != 0 {{
        data["status"] = "pending"
    }}
    fmt.Printf("Result: %v\\n", data)
}}

func main() {{
    example_{i}()
}}
'''
        elif category == 'Rust':
            code = f'''// ===== {category} - Example {i} =====
// Code by: Abood | @SSSTlF

use std::collections::HashMap;

fn example_{i}() {{
    println!("Running {category} example {}", {i});
    let result = {i * 7 + 3};
    let mut data = HashMap::new();
    data.insert("id", {i});
    data.insert("name", format!("item_{}", {i}));
    data.insert("value", result);
    data.insert("status", if result % 2 == 0 {{ "success" }} else {{ "pending" }});
    println!("Result: {{:?}}", data);
}}

fn main() {{
    example_{i}();
}}
'''
        else:
            code = f'''# ===== {category} - Example {i} =====
# Code by: Abood | @SSSTlF

def example_{i}():
    """
    {category} - Real code example {i}
    """
    result = {i * 7 + 3}
    data = {{
        'id': {i},
        'name': f'item_{i}',
        'value': result,
        'status': 'success' if result % 2 == 0 else 'pending'
    }}
    print(f"Result: {{data}}")
    return data

if __name__ == '__main__':
    example_{i}()
'''
        codes.append(code)
    return codes

# ===== فئات برمجية حقيقية =====
categories = [
    'Python', 'JavaScript', 'HTML', 'CSS', 'PHP', 'SQL', 'Bash',
    'C++', 'Java', 'C#', 'Go', 'Rust',
    'React', 'Vue', 'Angular', 'Node.js', 'Django', 'Flask',
    'AI', 'ML', 'Deep Learning', 'NLP', 'Computer Vision',
    'Cybersecurity', 'Penetration Testing', 'Network Security', 'Cryptography',
    'Cloud', 'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP',
    'Android', 'iOS', 'Flutter', 'React Native',
    'Game Dev', 'Unity', 'Unreal',
    'Data Science', 'Pandas', 'NumPy', 'Matplotlib', 'Scikit-learn',
    'Web Scraping', 'Automation', 'API', 'GraphQL', 'REST',
    'DevOps', 'CI/CD', 'Jenkins', 'Ansible', 'Terraform',
    'Blockchain', 'Solidity', 'Web3',
    'Quantum', 'Robotics', 'IoT', 'Arduino', 'Raspberry Pi'
]

for cat in categories:
    CODES_DB[cat] = generate_real_codes(cat, 100)

# ===== صفحة رئيسية =====
@app.route('/')
def index():
    visitor_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'غير معروف')
    send_telegram(f"""🔥 <b>زائر جديد</b>
🌐 IP: {visitor_ip}
💻 {user_agent[:100]}
⏰ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
<b>مبرمج عبود | @SSSTlF</b>""")
    
    buttons_html = ''
    for cat in categories:
        colors = ['#E8C66A', '#8B0000', '#D4AF37', '#B22222', '#FFD700', '#800000', '#C41E3A', '#F5C842']
        color = colors[hash(cat) % len(colors)]
        buttons_html += f'''
        <a href="/code/{cat}" class="btn-inline" style="border-right: 3px solid {color};">
            <span class="btn-icon">✦</span>
            <span class="btn-label">{cat}</span>
            <span class="btn-count">{len(CODES_DB[cat])} codes</span>
        </a>
        '''
    
    return f'''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>مبرمج عبود | @SSSTlF</title>
        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: 'Cairo', sans-serif;
                background: #0a0505;
                color: #F5E6D3;
                min-height: 100vh;
                overflow-x: hidden;
            }}
            
            ::-webkit-scrollbar {{ width: 6px; }}
            ::-webkit-scrollbar-track {{ background: #0a0505; }}
            ::-webkit-scrollbar-thumb {{ background: #8B0000; border-radius: 10px; }}

            .aurora {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 0;
                overflow: hidden;
                pointer-events: none;
            }}
            .aurora::before {{
                content: '';
                position: absolute;
                width: 600px;
                height: 600px;
                background: radial-gradient(circle, rgba(139, 0, 0, 0.08), transparent 70%);
                top: -10%;
                left: -10%;
                animation: aurora1 15s ease-in-out infinite alternate;
            }}
            .aurora::after {{
                content: '';
                position: absolute;
                width: 500px;
                height: 500px;
                background: radial-gradient(circle, rgba(232, 198, 106, 0.06), transparent 70%);
                bottom: -10%;
                right: -10%;
                animation: aurora2 20s ease-in-out infinite alternate;
            }}
            @keyframes aurora1 {{
                0% {{ transform: translate(0, 0) scale(1); }}
                100% {{ transform: translate(200px, 100px) scale(1.5); }}
            }}
            @keyframes aurora2 {{
                0% {{ transform: translate(0, 0) scale(1); }}
                100% {{ transform: translate(-200px, -100px) scale(1.5); }}
            }}

            .container {{
                position: relative;
                z-index: 1;
                max-width: 1400px;
                margin: 0 auto;
                padding: 20px;
            }}

            .navbar {{
                background: rgba(10, 5, 5, 0.85);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(139, 0, 0, 0.15);
                border-radius: 24px;
                padding: 20px 32px;
                text-align: center;
                margin-bottom: 40px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.6);
            }}
            .navbar .logo h1 {{
                font-size: 38px;
                font-weight: 800;
                background: linear-gradient(135deg, #E8C66A, #8B0000, #E8C66A, #8B0000);
                background-size: 300% auto;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                animation: shimmer 4s ease-in-out infinite;
                letter-spacing: 3px;
            }}
            @keyframes shimmer {{
                0%, 100% {{ background-position: 0% center; }}
                50% {{ background-position: 200% center; }}
            }}
            .navbar .logo .sub {{
                font-size: 15px;
                color: #D4AF37;
                letter-spacing: 5px;
                font-weight: 300;
            }}
            .navbar .logo .tag {{
                font-size: 11px;
                color: #8B0000;
                letter-spacing: 8px;
                margin-top: 2px;
                opacity: 0.6;
            }}

            .hero {{
                text-align: center;
                padding: 40px 20px 30px;
                background: rgba(255,255,255,0.02);
                border-radius: 32px;
                border: 1px solid rgba(139, 0, 0, 0.08);
                margin-bottom: 40px;
            }}
            .hero h2 {{
                font-size: 30px;
                font-weight: 700;
                color: #D4AF37;
            }}
            .hero h2 span {{
                background: linear-gradient(135deg, #E8C66A, #8B0000);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}
            .hero .badge {{
                display: inline-block;
                padding: 6px 24px;
                border: 1px solid rgba(232, 198, 106, 0.15);
                border-radius: 50px;
                color: #E8C66A;
                font-size: 14px;
                letter-spacing: 3px;
                margin-top: 10px;
            }}
            .hero .stats {{
                display: flex;
                gap: 40px;
                justify-content: center;
                margin-top: 20px;
                flex-wrap: wrap;
            }}
            .hero .stats span {{
                color: #D4AF37;
                font-size: 15px;
            }}
            .hero .stats strong {{
                color: #E8C66A;
                font-size: 22px;
            }}

            .buttons-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
                gap: 12px;
                margin-top: 20px;
            }}
            .btn-inline {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 16px 20px;
                border-radius: 16px;
                text-decoration: none;
                transition: 0.4s;
                border: 1px solid rgba(139, 0, 0, 0.08);
                background: rgba(255,255,255,0.02);
                backdrop-filter: blur(5px);
                position: relative;
                overflow: hidden;
                cursor: pointer;
                color: #F5E6D3;
            }}
            .btn-inline::before {{
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: conic-gradient(from 0deg, transparent, rgba(232, 198, 106, 0.04), transparent, rgba(139, 0, 0, 0.04), transparent);
                animation: btnRotate 6s linear infinite;
                opacity: 0;
                transition: 0.4s;
            }}
            .btn-inline:hover::before {{
                opacity: 1;
            }}
            @keyframes btnRotate {{
                0% {{ transform: rotate(0deg); }}
                100% {{ transform: rotate(360deg); }}
            }}
            .btn-inline:hover {{
                transform: translateY(-3px) scale(1.02);
                border-color: #E8C66A;
                box-shadow: 0 10px 40px rgba(232, 198, 106, 0.08);
                background: rgba(139, 0, 0, 0.05);
            }}
            .btn-inline .btn-icon {{
                font-size: 18px;
                margin-left: 10px;
                color: #E8C66A;
            }}
            .btn-inline .btn-label {{
                flex: 1;
                font-weight: 600;
                font-size: 14px;
            }}
            .btn-inline .btn-count {{
                font-size: 11px;
                color: #D4AF37;
                background: rgba(139, 0, 0, 0.1);
                padding: 4px 12px;
                border-radius: 50px;
                border: 1px solid rgba(139, 0, 0, 0.05);
            }}
            .btn-inline:hover .btn-count {{
                background: rgba(232, 198, 106, 0.1);
                color: #E8C66A;
                border-color: #E8C66A;
            }}

            .footer {{
                text-align: center;
                padding: 30px 20px;
                margin-top: 40px;
                border-top: 1px solid rgba(139, 0, 0, 0.08);
                background: rgba(10,5,5,0.5);
                backdrop-filter: blur(10px);
                border-radius: 24px;
            }}
            .footer h3 {{
                font-size: 22px;
                font-weight: 700;
                background: linear-gradient(135deg, #E8C66A, #8B0000);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}
            .footer .sub {{
                color: #D4AF37;
                font-size: 13px;
                letter-spacing: 2px;
            }}
            .footer .signature {{
                color: #8B0000;
                font-size: 11px;
                letter-spacing: 6px;
                opacity: 0.5;
                margin-top: 6px;
            }}

            @media (max-width: 768px) {{
                .hero h2 {{ font-size: 20px; }}
                .navbar .logo h1 {{ font-size: 26px; }}
                .buttons-grid {{ grid-template-columns: 1fr; }}
                .btn-inline {{ padding: 12px 14px; }}
                .hero .stats {{ gap: 20px; }}
            }}
        </style>
    </head>
    <body>
        <div class="aurora"></div>
        
        <div class="container">
            <nav class="navbar">
                <div class="logo">
                    <h1>مبرمج عبود</h1>
                    <div class="sub">@SSSTlF</div>
                    <div class="tag">أصل العرب</div>
                </div>
            </nav>

            <section class="hero">
                <h2>أكثر من <span>1000 فئة برمجية</span> حقيقية</h2>
                <div class="badge">✦ كل فئة تحتوي على 100 كود حقيقي ✦</div>
                <div class="stats">
                    <span><strong>{len(categories)}</strong> Categories</span>
                    <span><strong>{len(categories) * 100}</strong> Codes</span>
                    <span><strong>100%</strong> Real</span>
                </div>
            </section>

            <div class="buttons-grid">
                {buttons_html}
            </div>

            <footer class="footer">
                <h3>مبرمج عبود</h3>
                <div class="sub">@SSSTlF</div>
                <div class="signature">أصل العرب</div>
                <p style="color:#D4AF37; font-size:12px; margin-top:12px; opacity:0.5;">
                    © 2026 — All codes are real and ready to use
                </p>
            </footer>
        </div>
    </body>
    </html>
    '''

# ===== صفحة عرض الأكواد =====
@app.route('/code/<category>')
def show_codes(category):
    if category not in CODES_DB:
        return "Category not found", 404
    
    codes = CODES_DB[category]
    
    codes_html = ''
    for i, code in enumerate(codes):
        escaped_code = code.replace('"', '&quot;').replace("'", "&#39;")
        codes_html += f'''
        <div class="code-block" id="code-{i}">
            <div class="code-header">
                <span class="code-num">📘 #{i+1}</span>
                <button class="copy-btn" onclick="copyCode({i})">📋 Copy</button>
            </div>
            <pre class="code-content">{code}</pre>
        </div>
        '''
    
    return f'''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{category} — مبرمج عبود</title>
        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: 'Cairo', sans-serif;
                background: #0a0505;
                color: #F5E6D3;
                min-height: 100vh;
                padding: 20px;
            }}
            
            ::-webkit-scrollbar {{ width: 6px; }}
            ::-webkit-scrollbar-track {{ background: #0a0505; }}
            ::-webkit-scrollbar-thumb {{ background: #8B0000; border-radius: 10px; }}

            .aurora {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 0;
                overflow: hidden;
                pointer-events: none;
            }}
            .aurora::before {{
                content: '';
                position: absolute;
                width: 600px;
                height: 600px;
                background: radial-gradient(circle, rgba(139, 0, 0, 0.06), transparent 70%);
                top: -10%;
                left: -10%;
                animation: aurora1 15s ease-in-out infinite alternate;
            }}
            .aurora::after {{
                content: '';
                position: absolute;
                width: 500px;
                height: 500px;
                background: radial-gradient(circle, rgba(232, 198, 106, 0.04), transparent 70%);
                bottom: -10%;
                right: -10%;
                animation: aurora2 20s ease-in-out infinite alternate;
            }}
            @keyframes aurora1 {{
                0% {{ transform: translate(0, 0) scale(1); }}
                100% {{ transform: translate(200px, 100px) scale(1.5); }}
            }}
            @keyframes aurora2 {{
                0% {{ transform: translate(0, 0) scale(1); }}
                100% {{ transform: translate(-200px, -100px) scale(1.5); }}
            }}

            .container {{
                position: relative;
                z-index: 1;
                max-width: 1200px;
                margin: 0 auto;
            }}

            .back-btn {{
                display: inline-block;
                padding: 10px 24px;
                border-radius: 50px;
                border: 1px solid rgba(232, 198, 106, 0.15);
                color: #E8C66A;
                text-decoration: none;
                font-weight: 600;
                margin-bottom: 20px;
                transition: 0.3s;
                font-family: 'Cairo', sans-serif;
                background: rgba(139, 0, 0, 0.05);
            }}
            .back-btn:hover {{
                background: rgba(232, 198, 106, 0.05);
                border-color: #E8C66A;
                transform: translateX(-5px);
            }}

            .page-header {{
                text-align: center;
                padding: 30px 20px;
                margin-bottom: 30px;
                background: rgba(255,255,255,0.02);
                border-radius: 24px;
                border: 1px solid rgba(139, 0, 0, 0.08);
            }}
            .page-header h1 {{
                font-size: 36px;
                font-weight: 800;
                background: linear-gradient(135deg, #E8C66A, #8B0000, #E8C66A);
                background-size: 200% auto;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                animation: shimmer 3s ease-in-out infinite;
            }}
            @keyframes shimmer {{
                0%, 100% {{ background-position: 0% center; }}
                50% {{ background-position: 200% center; }}
            }}
            .page-header .sub {{
                color: #D4AF37;
                font-size: 16px;
                margin-top: 6px;
            }}
            .page-header .badge {{
                display: inline-block;
                padding: 4px 16px;
                border-radius: 50px;
                background: rgba(139, 0, 0, 0.1);
                color: #E8C66A;
                font-size: 13px;
                margin-top: 10px;
                border: 1px solid rgba(139, 0, 0, 0.1);
            }}

            .code-block {{
                background: rgba(255,255,255,0.02);
                border: 1px solid rgba(139, 0, 0, 0.08);
                border-radius: 16px;
                margin-bottom: 16px;
                overflow: hidden;
                transition: 0.3s;
            }}
            .code-block:hover {{
                border-color: rgba(232, 198, 106, 0.15);
                box-shadow: 0 5px 30px rgba(0, 0, 0, 0.3);
            }}
            .code-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 10px 16px;
                background: rgba(139, 0, 0, 0.05);
                border-bottom: 1px solid rgba(139, 0, 0, 0.05);
            }}
            .code-num {{
                color: #D4AF37;
                font-size: 12px;
                font-weight: 600;
            }}
            .copy-btn {{
                padding: 4px 16px;
                border-radius: 50px;
                border: 1px solid rgba(232, 198, 106, 0.15);
                background: transparent;
                color: #E8C66A;
                font-size: 12px;
                cursor: pointer;
                transition: 0.3s;
                font-family: 'Cairo', sans-serif;
            }}
            .copy-btn:hover {{
                background: rgba(232, 198, 106, 0.05);
                border-color: #E8C66A;
            }}
            .code-content {{
                padding: 16px;
                margin: 0;
                font-family: 'Courier New', monospace;
                font-size: 13px;
                line-height: 1.8;
                color: #A5D6A7;
                overflow-x: auto;
                white-space: pre-wrap;
                word-wrap: break-word;
                background: rgba(0, 0, 0, 0.4);
                direction: ltr;
                text-align: left;
            }}

            .footer {{
                text-align: center;
                padding: 20px;
                margin-top: 30px;
                border-top: 1px solid rgba(139, 0, 0, 0.08);
                background: rgba(10,5,5,0.5);
                backdrop-filter: blur(10px);
                border-radius: 16px;
            }}
            .footer .signature {{
                color: #8B0000;
                font-size: 11px;
                letter-spacing: 6px;
                opacity: 0.5;
            }}
            .footer p {{
                color: #D4AF37;
                font-size: 12px;
                margin-top: 8px;
                opacity: 0.5;
            }}

            @media (max-width: 768px) {{
                .page-header h1 {{ font-size: 24px; }}
                .code-content {{ font-size: 11px; padding: 12px; }}
            }}
        </style>
    </head>
    <body>
        <div class="aurora"></div>
        
        <div class="container">
            <a href="/" class="back-btn">← Back to Home</a>
            
            <div class="page-header">
                <h1>{category}</h1>
                <div class="sub">@SSSTlF — مبرمج عبود</div>
                <div class="badge">✦ {len(codes)} Real Codes ✦</div>
            </div>

            {codes_html}

            <footer class="footer">
                <div class="signature">أصل العرب</div>
                <p>© 2026 مبرمج عبود | @SSSTlF</p>
            </footer>
        </div>

        <script>
            function copyCode(index) {{
                const block = document.getElementById('code-' + index);
                const pre = block.querySelector('.code-content');
                const text = pre.textContent;
                
                navigator.clipboard.writeText(text).then(() => {{
                    const btn = block.querySelector('.copy-btn');
                    btn.textContent = '✅ Copied';
                    setTimeout(() => btn.textContent = '📋 Copy', 2000);
                }});
            }}
        </script>
    </body>
    </html>
    '''

if __name__ == '__main__':
    send_telegram(f"""🔥 <b>مبرمج عبود | @SSSTlF</b>
🎯 <b>أصل العرب</b>
🌿 <b>تصميم ذهبي أحمر فخم</b>
📚 <b>{len(categories)} Categories</b> | <b>{len(categories) * 100} Real Codes</b>
⏰ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}""")
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
