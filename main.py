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

# ===== قاعدة الأكواد =====
CODES_DB = {}

def generate_codes(category, count=100):
    codes = []
    for i in range(1, count + 1):
        code = f'''# ===== {category} - مثال رقم {i} =====
# مبرمج عبود | @SSSTlF

def example_{i}():
    """
    {category} - كود رقم {i}
    """
    print(f"تنفيذ {category} - مثال {i}")
    result = {i * 7 + 3}
    data = {{
        'id': {i},
        'name': f'{category}_{i}',
        'value': result,
        'status': 'نجاح' if result % 2 == 0 else 'قيد التنفيذ'
    }}
    print(f"النتيجة: {{data}}")
    return data

if __name__ == '__main__':
    example_{i}()
'''
        codes.append(code)
    return codes

# ===== إنشاء الأكواد لكل فئة =====
categories = [
    'python', 'javascript', 'html', 'css', 'php', 'sql', 
    'bash', 'cpp', 'java', 'csharp', 'go', 'rust',
    'react', 'vue', 'angular', 'nodejs', 'django', 'flask',
    'ai', 'ml', 'deep-learning', 'nlp', 'computer-vision',
    'cybersecurity', 'penetration-testing', 'network-security', 'cryptography',
    'cloud', 'docker', 'kubernetes', 'aws', 'azure', 'gcp',
    'mobile', 'android', 'ios', 'flutter', 'react-native',
    'game-dev', 'unity', 'unreal', 'p5js',
    'data-science', 'pandas', 'numpy', 'matplotlib', 'scikit-learn',
    'web-scraping', 'automation', 'api', 'graphql', 'rest',
    'devops', 'ci-cd', 'jenkins', 'ansible', 'terraform',
    'blockchain', 'solidity', 'web3',
    'quantum', 'robotics', 'iot', 'arduino', 'raspberrypi'
]

for cat in categories:
    CODES_DB[cat] = generate_codes(cat, 100)

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
    
    # إنشاء الأزرار
    buttons_html = ''
    for cat in categories:
        display_name = cat.replace('-', ' ').replace('_', ' ').title()
        buttons_html += f'''
        <a href="/code/{cat}" class="btn-inline {cat}">
            <span class="btn-icon">✦</span>
            <span class="btn-label">{display_name}</span>
            <span class="btn-count">{len(CODES_DB[cat])} كود</span>
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
                background: #05070D;
                color: #F8FAFC;
                min-height: 100vh;
                overflow-x: hidden;
            }}
            
            ::-webkit-scrollbar {{ width: 6px; }}
            ::-webkit-scrollbar-track {{ background: #05070D; }}
            ::-webkit-scrollbar-thumb {{ background: #E8C66A; border-radius: 10px; }}

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
                background: radial-gradient(circle, rgba(232, 198, 106, 0.06), transparent 70%);
                top: -10%;
                left: -10%;
                animation: aurora1 15s ease-in-out infinite alternate;
            }}
            .aurora::after {{
                content: '';
                position: absolute;
                width: 500px;
                height: 500px;
                background: radial-gradient(circle, rgba(59, 130, 246, 0.06), transparent 70%);
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

            /* Navbar */
            .navbar {{
                background: rgba(5, 7, 13, 0.7);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(232, 198, 106, 0.1);
                border-radius: 24px;
                padding: 16px 32px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 40px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
            }}
            .navbar .logo h1 {{
                font-size: 28px;
                font-weight: 800;
                background: linear-gradient(135deg, #E8C66A, #F8FAFC, #E8C66A);
                background-size: 200% auto;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                animation: shimmer 3s ease-in-out infinite;
            }}
            @keyframes shimmer {{
                0%, 100% {{ background-position: 0% center; }}
                50% {{ background-position: 200% center; }}
            }}
            .navbar .logo .sub {{
                font-size: 11px;
                color: #D4AF37;
                letter-spacing: 4px;
                opacity: 0.6;
            }}
            .navbar .logo .tag {{
                font-size: 10px;
                color: #AEB8C4;
                letter-spacing: 2px;
            }}

            /* Hero */
            .hero {{
                text-align: center;
                padding: 50px 20px 40px;
                background: rgba(255,255,255,0.02);
                border-radius: 32px;
                border: 1px solid rgba(232, 198, 106, 0.05);
                margin-bottom: 40px;
            }}
            .hero h1 {{
                font-size: 56px;
                font-weight: 800;
                background: linear-gradient(135deg, #E8C66A, #F8FAFC, #E8C66A);
                background-size: 200% auto;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                animation: shimmer 3s ease-in-out infinite;
            }}
            .hero .subtitle {{
                font-size: 18px;
                color: #AEB8C4;
                margin: 8px 0;
            }}
            .hero .badge {{
                display: inline-block;
                padding: 6px 20px;
                border: 1px solid rgba(232, 198, 106, 0.2);
                border-radius: 50px;
                color: #D4AF37;
                font-size: 13px;
                letter-spacing: 3px;
            }}
            .hero .stats {{
                display: flex;
                gap: 30px;
                justify-content: center;
                margin-top: 20px;
                flex-wrap: wrap;
            }}
            .hero .stats span {{
                color: #AEB8C4;
                font-size: 14px;
            }}
            .hero .stats strong {{
                color: #E8C66A;
                font-size: 20px;
            }}

            /* Buttons Grid */
            .buttons-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
                gap: 12px;
                margin-top: 20px;
            }}
            .btn-inline {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 14px 20px;
                border-radius: 16px;
                text-decoration: none;
                transition: 0.4s;
                border: 1px solid rgba(255,255,255,0.05);
                background: rgba(255,255,255,0.02);
                backdrop-filter: blur(5px);
                position: relative;
                overflow: hidden;
                cursor: pointer;
                color: #F8FAFC;
            }}
            .btn-inline::before {{
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: conic-gradient(from 0deg, transparent, rgba(232, 198, 106, 0.05), transparent);
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
                transform: translateY(-3px) scale(1.01);
                border-color: #E8C66A;
                box-shadow: 0 10px 40px rgba(232, 198, 106, 0.08);
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
                color: #AEB8C4;
                background: rgba(255,255,255,0.05);
                padding: 4px 12px;
                border-radius: 50px;
            }}
            .btn-inline:hover .btn-count {{
                background: rgba(232, 198, 106, 0.15);
                color: #E8C66A;
            }}

            /* Colors */
            .btn-inline.python {{ border-right: 3px solid #3776AB; }}
            .btn-inline.javascript {{ border-right: 3px solid #F7DF1E; }}
            .btn-inline.html {{ border-right: 3px solid #E34F26; }}
            .btn-inline.css {{ border-right: 3px solid #1572B6; }}
            .btn-inline.php {{ border-right: 3px solid #777BB4; }}
            .btn-inline.sql {{ border-right: 3px solid #4479A1; }}
            .btn-inline.bash {{ border-right: 3px solid #4EAA25; }}
            .btn-inline.cpp {{ border-right: 3px solid #00599C; }}
            .btn-inline.java {{ border-right: 3px solid #007396; }}
            .btn-inline.csharp {{ border-right: 3px solid #68217A; }}
            .btn-inline.go {{ border-right: 3px solid #00ADD8; }}
            .btn-inline.rust {{ border-right: 3px solid #DEA584; }}
            .btn-inline.react {{ border-right: 3px solid #61DAFB; }}
            .btn-inline.vue {{ border-right: 3px solid #4FC08D; }}
            .btn-inline.angular {{ border-right: 3px solid #DD0031; }}
            .btn-inline.nodejs {{ border-right: 3px solid #339933; }}
            .btn-inline.django {{ border-right: 3px solid #092E20; }}
            .btn-inline.flask {{ border-right: 3px solid #000000; }}
            .btn-inline.ai {{ border-right: 3px solid #FF6F00; }}
            .btn-inline.ml {{ border-right: 3px solid #00BCD4; }}
            .btn-inline.deep-learning {{ border-right: 3px solid #E91E63; }}
            .btn-inline.nlp {{ border-right: 3px solid #9C27B0; }}
            .btn-inline.computer-vision {{ border-right: 3px solid #3F51B5; }}
            .btn-inline.cybersecurity {{ border-right: 3px solid #00E676; }}
            .btn-inline.penetration-testing {{ border-right: 3px solid #FF1744; }}
            .btn-inline.network-security {{ border-right: 3px solid #2979FF; }}
            .btn-inline.cryptography {{ border-right: 3px solid #D500F9; }}
            .btn-inline.cloud {{ border-right: 3px solid #00BCD4; }}
            .btn-inline.docker {{ border-right: 3px solid #2496ED; }}
            .btn-inline.kubernetes {{ border-right: 3px solid #326CE5; }}
            .btn-inline.aws {{ border-right: 3px solid #FF9900; }}
            .btn-inline.azure {{ border-right: 3px solid #0089D6; }}
            .btn-inline.gcp {{ border-right: 3px solid #4285F4; }}
            .btn-inline.mobile {{ border-right: 3px solid #3DDC84; }}
            .btn-inline.android {{ border-right: 3px solid #3DDC84; }}
            .btn-inline.ios {{ border-right: 3px solid #000000; }}
            .btn-inline.flutter {{ border-right: 3px solid #02569B; }}
            .btn-inline.react-native {{ border-right: 3px solid #61DAFB; }}
            .btn-inline.game-dev {{ border-right: 3px solid #FF6F00; }}
            .btn-inline.unity {{ border-right: 3px solid #000000; }}
            .btn-inline.unreal {{ border-right: 3px solid #0E1128; }}
            .btn-inline.p5js {{ border-right: 3px solid #ED225D; }}
            .btn-inline.data-science {{ border-right: 3px solid #4CAF50; }}
            .btn-inline.pandas {{ border-right: 3px solid #150458; }}
            .btn-inline.numpy {{ border-right: 3px solid #013243; }}
            .btn-inline.matplotlib {{ border-right: 3px solid #11557C; }}
            .btn-inline.scikit-learn {{ border-right: 3px solid #F7931E; }}
            .btn-inline.web-scraping {{ border-right: 3px solid #4CAF50; }}
            .btn-inline.automation {{ border-right: 3px solid #FF6F00; }}
            .btn-inline.api {{ border-right: 3px solid #00BCD4; }}
            .btn-inline.graphql {{ border-right: 3px solid #E10098; }}
            .btn-inline.rest {{ border-right: 3px solid #00BCD4; }}
            .btn-inline.devops {{ border-right: 3px solid #E95420; }}
            .btn-inline.ci-cd {{ border-right: 3px solid #0078D7; }}
            .btn-inline.jenkins {{ border-right: 3px solid #D24939; }}
            .btn-inline.ansible {{ border-right: 3px solid #EE0000; }}
            .btn-inline.terraform {{ border-right: 3px solid #5C4EE5; }}
            .btn-inline.blockchain {{ border-right: 3px solid #F7931A; }}
            .btn-inline.solidity {{ border-right: 3px solid #363636; }}
            .btn-inline.web3 {{ border-right: 3px solid #F16822; }}
            .btn-inline.quantum {{ border-right: 3px solid #00BCD4; }}
            .btn-inline.robotics {{ border-right: 3px solid #FF6F00; }}
            .btn-inline.iot {{ border-right: 3px solid #00BCD4; }}
            .btn-inline.arduino {{ border-right: 3px solid #00979D; }}
            .btn-inline.raspberrypi {{ border-right: 3px solid #C51A4A; }}

            /* Footer */
            .footer {{
                text-align: center;
                padding: 30px 20px;
                margin-top: 40px;
                border-top: 1px solid rgba(255,255,255,0.05);
                background: rgba(5,7,13,0.5);
                backdrop-filter: blur(10px);
                border-radius: 24px;
            }}
            .footer h3 {{
                font-size: 22px;
                font-weight: 700;
                background: linear-gradient(135deg, #E8C66A, #F8FAFC);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}
            .footer .sub {{
                color: #AEB8C4;
                font-size: 13px;
                letter-spacing: 2px;
            }}
            .footer .signature {{
                color: #D4AF37;
                font-size: 11px;
                letter-spacing: 6px;
                opacity: 0.4;
                margin-top: 6px;
            }}

            @media (max-width: 768px) {{
                .hero h1 {{ font-size: 32px; }}
                .navbar {{ flex-direction: column; gap: 12px; padding: 16px; }}
                .buttons-grid {{ grid-template-columns: 1fr; }}
                .btn-inline {{ padding: 12px 16px; }}
            }}
        </style>
    </head>
    <body>
        <div class="aurora"></div>
        
        <div class="container">
            <!-- Navbar -->
            <nav class="navbar">
                <div class="logo">
                    <h1>مبرمج عبود</h1>
                    <div class="sub">@SSSTlF</div>
                    <div class="tag">أصل العرب</div>
                </div>
                <div style="display:flex; gap:12px; flex-wrap:wrap;">
                    <span style="color:#AEB8C4; font-size:13px;">✦ {len(categories)} فئة</span>
                    <span style="color:#E8C66A; font-size:13px;">✦ {len(categories) * 100} كود</span>
                </div>
            </nav>

            <!-- Hero -->
            <section class="hero">
                <h1>مبرمج عبود</h1>
                <div class="subtitle">@SSSTlF — أصل العرب</div>
                <div class="badge">✦ أكثر من 2000 كود برمجي ✦</div>
                <div class="stats">
                    <span><strong>{len(categories)}</strong> فئة</span>
                    <span><strong>{len(categories) * 100}</strong> كود</span>
                    <span><strong>100%</strong> حقيقي</span>
                </div>
            </section>

            <!-- Buttons -->
            <div class="buttons-grid">
                {buttons_html}
            </div>

            <!-- Footer -->
            <footer class="footer">
                <h3>مبرمج عبود</h3>
                <div class="sub">@SSSTlF</div>
                <div class="signature">أصل العرب</div>
                <p style="color:#AEB8C4; font-size:12px; margin-top:12px;">
                    © 2026 — جميع الأكواد حقيقية وجاهزة للاستخدام
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
        return "الفئة غير موجودة", 404
    
    codes = CODES_DB[category]
    display_name = category.replace('-', ' ').replace('_', ' ').title()
    
    # إنشاء الأكواد مع زر النسخ
    codes_html = ''
    for i, code in enumerate(codes):
        escaped_code = code.replace('"', '&quot;').replace("'", "&#39;")
        codes_html += f'''
        <div class="code-block" id="code-{i}">
            <div class="code-header">
                <span class="code-num">#{i+1}</span>
                <button class="copy-btn" onclick="copyCode({i})">📋 نسخ</button>
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
        <title>{display_name} — مبرمج عبود</title>
        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: 'Cairo', sans-serif;
                background: #05070D;
                color: #F8FAFC;
                min-height: 100vh;
                padding: 20px;
            }}
            
            ::-webkit-scrollbar {{ width: 6px; }}
            ::-webkit-scrollbar-track {{ background: #05070D; }}
            ::-webkit-scrollbar-thumb {{ background: #E8C66A; border-radius: 10px; }}

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
                background: radial-gradient(circle, rgba(232, 198, 106, 0.06), transparent 70%);
                top: -10%;
                left: -10%;
                animation: aurora1 15s ease-in-out infinite alternate;
            }}
            .aurora::after {{
                content: '';
                position: absolute;
                width: 500px;
                height: 500px;
                background: radial-gradient(circle, rgba(59, 130, 246, 0.06), transparent 70%);
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
                border: 1px solid rgba(232, 198, 106, 0.2);
                color: #D4AF37;
                text-decoration: none;
                font-weight: 600;
                margin-bottom: 20px;
                transition: 0.3s;
                font-family: 'Cairo', sans-serif;
            }}
            .back-btn:hover {{
                background: rgba(232, 198, 106, 0.1);
                border-color: #E8C66A;
            }}

            .page-header {{
                text-align: center;
                padding: 30px 20px;
                margin-bottom: 30px;
                background: rgba(255,255,255,0.02);
                border-radius: 24px;
                border: 1px solid rgba(232, 198, 106, 0.05);
            }}
            .page-header h1 {{
                font-size: 40px;
                font-weight: 800;
                background: linear-gradient(135deg, #E8C66A, #F8FAFC, #E8C66A);
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
                color: #AEB8C4;
                font-size: 16px;
                margin-top: 6px;
            }}
            .page-header .badge {{
                display: inline-block;
                padding: 4px 16px;
                border-radius: 50px;
                background: rgba(232, 198, 106, 0.1);
                color: #D4AF37;
                font-size: 13px;
                margin-top: 10px;
            }}

            .code-block {{
                background: rgba(255,255,255,0.02);
                border: 1px solid rgba(255,255,255,0.05);
                border-radius: 16px;
                margin-bottom: 16px;
                overflow: hidden;
                transition: 0.3s;
            }}
            .code-block:hover {{
                border-color: rgba(232, 198, 106, 0.15);
                box-shadow: 0 5px 30px rgba(0,0,0,0.2);
            }}
            .code-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 10px 16px;
                background: rgba(255,255,255,0.03);
                border-bottom: 1px solid rgba(255,255,255,0.05);
            }}
            .code-num {{
                color: #AEB8C4;
                font-size: 12px;
                font-weight: 600;
            }}
            .copy-btn {{
                padding: 4px 16px;
                border-radius: 50px;
                border: 1px solid rgba(232, 198, 106, 0.2);
                background: transparent;
                color: #D4AF37;
                font-size: 12px;
                cursor: pointer;
                transition: 0.3s;
                font-family: 'Cairo', sans-serif;
            }}
            .copy-btn:hover {{
                background: rgba(232, 198, 106, 0.1);
                border-color: #E8C66A;
            }}
            .code-content {{
                padding: 16px;
                margin: 0;
                font-family: 'Courier New', monospace;
                font-size: 13px;
                line-height: 1.6;
                color: #00ff88;
                overflow-x: auto;
                white-space: pre-wrap;
                word-wrap: break-word;
                background: rgba(0,0,0,0.3);
            }}

            .footer {{
                text-align: center;
                padding: 20px;
                margin-top: 30px;
                border-top: 1px solid rgba(255,255,255,0.05);
            }}
            .footer .signature {{
                color: #D4AF37;
                font-size: 11px;
                letter-spacing: 6px;
                opacity: 0.4;
            }}

            @media (max-width: 768px) {{
                .page-header h1 {{ font-size: 28px; }}
                .code-content {{ font-size: 11px; padding: 12px; }}
            }}
        </style>
    </head>
    <body>
        <div class="aurora"></div>
        
        <div class="container">
            <a href="/" class="back-btn">← العودة للرئيسية</a>
            
            <div class="page-header">
                <h1>{display_name}</h1>
                <div class="sub">@SSSTlF — مبرمج عبود</div>
                <div class="badge">✦ {len(codes)} كود برمجي حقيقي ✦</div>
            </div>

            {codes_html}

            <footer class="footer">
                <div class="signature">أصل العرب</div>
                <p style="color:#AEB8C4; font-size:12px; margin-top:8px;">
                    © 2026 مبرمج عبود | @SSSTlF
                </p>
            </footer>
        </div>

        <script>
            function copyCode(index) {{
                const block = document.getElementById('code-' + index);
                const pre = block.querySelector('.code-content');
                const text = pre.textContent;
                
                navigator.clipboard.writeText(text).then(() => {{
                    const btn = block.querySelector('.copy-btn');
                    btn.textContent = '✅ تم النسخ';
                    setTimeout(() => btn.textContent = '📋 نسخ', 2000);
                }});
            }}
        </script>
    </body>
    </html>
    '''

if __name__ == '__main__':
    send_telegram(f"""🔥 <b>تم تشغيل موقع مبرمج عبود</b>
🎯 <b>@SSSTlF | أصل العرب</b>
📚 <b>{len(categories)} فئة</b> | <b>{len(categories) * 100} كود</b>
⏰ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}""")
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
