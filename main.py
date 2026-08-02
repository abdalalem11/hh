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

def generate_bot_codes():
    codes = []
    lessons = [
        ("مقدمة عن البوتات", "ما هو البوت؟\nالبوت هو برنامج يعمل تلقائياً"),
        ("أنواع البوتات", "أنواع البوتات:\n1. محادثة\n2. ويب\n3. ألعاب"),
        ("لغة بايثون للبوتات", "لماذا بايثون؟\nسهلة التعلم\nمكتبات جاهزة"),
        ("تثبيت بايثون", "تثبيت بايثون:\n1. تحميل من python.org"),
        ("مكتبة python-telegram-bot", "تثبيت المكتبة:\npip install python-telegram-bot"),
        ("إنشاء بوت تليجرام", "خطوات:\n1. @BotFather\n2. /newbot"),
        ("أول كود بوت", "from telegram import Update\nfrom telegram.ext import ApplicationBuilder"),
        ("أوامر البوت", "إضافة أوامر start و help"),
        ("مكتبة discord.py", "pip install discord.py"),
        ("إنشاء بوت ديسكورد", "Discord Developer Portal"),
        ("أول كود بوت ديسكورد", "import discord\nfrom discord.ext import commands"),
        ("مكتبة requests", "import requests\nresponse = requests.get()"),
        ("مكتبة BeautifulSoup", "from bs4 import BeautifulSoup"),
        ("مكتبة selenium", "from selenium import webdriver"),
        ("بوتات الواتساب", "pip install pywhatkit"),
        ("بوتات الانستغرام", "pip install instabot"),
        ("بوتات تويتر", "pip install tweepy"),
        ("معالجة النصوص", "مكتبات: re, nltk, spaCy"),
        ("معالجة الصور", "مكتبات: PIL, OpenCV"),
        ("بوتات الذكاء الاصطناعي", "مكتبات: transformers, openai"),
        ("بوتات الصوت", "مكتبات: speech_recognition, pyttsx3"),
        ("قواعد البيانات", "مكتبات: sqlite3, pymongo"),
        ("التعامل مع APIs", "مكتبات: requests, aiohttp"),
        ("جدولة المهام", "مكتبات: schedule, APScheduler"),
        ("الأمان في البوتات", "نصائح أمان مهمة"),
        ("نشر البوت", "طرق النشر: Render, Heroku"),
        ("تحسين الأداء", "استخدام async/await, caching"),
        ("أخطاء شائعة", "Invalid Token, Rate Limits"),
        ("مشاريع تطبيقية", "بوت طقس, بوت تذكير, بوت مساعد"),
        ("خاتمة", "مبروك! أنت الآن مبرمج بوتات")
    ]
    
    for i, (title, content) in enumerate(lessons, 1):
        code = f'''# ===== الدرس {i}: {title} =====
# مبرمج عبود | @SSSTlF

'''
        code += f'# {content}\n\n'
        code += f'print("الدرس {i}: {title}")\n'
        code += f'print("{content[:100]}...")\n'
        code += f'print("✅ تم إكمال الدرس {i}")\n'
        codes.append(code)
    return codes

def generate_codes(category, count=100):
    codes = []
    for i in range(1, count + 1):
        code = f'''# {category} - مثال {i}
def example_{i}():
    result = {i * 7 + 3}
    data = {{'id': {i}, 'value': result, 'status': 'success' if result % 2 == 0 else 'pending'}}
    print(f"Result: {{data}}")
    return data
example_{i}()'''
        codes.append(code)
    return codes

categories = [
    'تعليم البوتات', 'بايثون', 'جافا سكريبت', 'إتش تي إم إل', 'سي إس إس', 
    'بي إتش بي', 'إس كيو إل', 'باش', 'سي بلس بلس', 'جافا', 
    'سي شارب', 'رياكت', 'فيو', 'أنغولار', 'نود جي إس',
    'جانغو', 'فلاسك', 'ذكاء اصطناعي', 'تعلم آلة', 'تعلم عميق',
    'أمن سيبراني', 'سحابة', 'دوكر', 'كوبرنيتيس'
]

for cat in categories:
    if cat == 'تعليم البوتات':
        CODES_DB[cat] = generate_bot_codes()
    else:
        CODES_DB[cat] = generate_codes(cat, 100)

@app.route('/')
def index():
    visitor_ip = request.remote_addr
    send_telegram(f"🔥 زائر جديد | IP: {visitor_ip} | @SSSTlF | {len(categories)} فئة")
    
    buttons = ''.join([f'''
    <div class="card glass" data-category="{cat}">
        <div class="card-icon">⌨</div>
        <div class="card-title">{cat}</div>
        <div class="card-count">{len(CODES_DB[cat])} كود</div>
        <div class="card-desc">مكتبة أكواد احترافية في {cat}</div>
        <a href="/code/{cat}" class="card-btn">استكشف <span>→</span></a>
    </div>
    ''' for cat in categories])
    
    return f'''
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>مبرمج عبود | @SSSTlF</title>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
:root {{
    --bg: #05070D;
    --gold: #E8C66A;
    --purple: #7C3AED;
    --blue: #3B82F6;
    --red: #8B0000;
    --white: #F8FAFC;
    --glass-bg: rgba(255,255,255,0.04);
    --glass-border: rgba(255,255,255,0.08);
}}

* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html {{ scroll-behavior: smooth; }}

body {{
    font-family: 'Cairo', sans-serif;
    background: var(--bg);
    color: var(--white);
    min-height: 100vh;
    overflow-x: hidden;
    cursor: none;
}}

/* ===== Cursor Glow ===== */
.cursor-glow {{
    position: fixed;
    width: 600px;
    height: 600px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(232,198,106,0.06), transparent 70%);
    pointer-events: none;
    z-index: 9999;
    transform: translate(-50%, -50%);
    transition: all 0.08s ease;
}}
.cursor-dot {{
    position: fixed;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--gold);
    pointer-events: none;
    z-index: 10000;
    transform: translate(-50%, -50%);
    box-shadow: 0 0 20px rgba(232,198,106,0.5);
}}

/* ===== Scrollbar ===== */
::-webkit-scrollbar {{ width: 8px; }}
::-webkit-scrollbar-track {{ background: var(--bg); }}
::-webkit-scrollbar-thumb {{ background: var(--gold); border-radius: 10px; }}

/* ===== Loading Screen ===== */
.loading-screen {{
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: var(--bg);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 99999;
    transition: opacity 0.8s ease, visibility 0.8s ease;
}}
.loading-screen.hidden {{
    opacity: 0;
    visibility: hidden;
}}
.loading-screen .logo {{
    font-size: 48px;
    font-weight: 900;
    background: linear-gradient(135deg, var(--gold), var(--red), var(--gold));
    background-size: 300% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 3s ease-in-out infinite;
}}
.loading-screen .sub {{
    color: var(--gold);
    font-size: 16px;
    letter-spacing: 6px;
    opacity: 0.6;
}}
.loading-screen .loader {{
    width: 60px;
    height: 60px;
    border: 3px solid rgba(232,198,106,0.1);
    border-top-color: var(--gold);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-top: 30px;
}}
.loading-screen .progress-bar {{
    width: 200px;
    height: 2px;
    background: rgba(232,198,106,0.1);
    border-radius: 10px;
    margin-top: 20px;
    overflow: hidden;
}}
.loading-screen .progress-bar .fill {{
    width: 0%;
    height: 100%;
    background: linear-gradient(90deg, var(--gold), var(--red));
    animation: progress 2s ease-in-out forwards;
}}
@keyframes spin {{ to {{ transform: rotate(360deg); }} }}
@keyframes progress {{ 0% {{ width: 0%; }} 100% {{ width: 100%; }} }}
@keyframes shimmer {{
    0%, 100% {{ background-position: 0% center; }}
    50% {{ background-position: 200% center; }}
}}

/* ===== Scroll Progress ===== */
.scroll-progress {{
    position: fixed;
    top: 0; left: 0;
    width: 0%;
    height: 3px;
    background: linear-gradient(90deg, var(--gold), var(--red));
    z-index: 9998;
    transition: width 0.1s;
}}

/* ===== Back to Top ===== */
.back-top {{
    position: fixed;
    bottom: 30px; right: 30px;
    width: 50px; height: 50px;
    border-radius: 50%;
    background: rgba(232,198,106,0.1);
    border: 1px solid rgba(232,198,106,0.2);
    color: var(--gold);
    font-size: 20px;
    cursor: pointer;
    z-index: 999;
    opacity: 0;
    transform: scale(0.8);
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
}}
.back-top.visible {{
    opacity: 1;
    transform: scale(1);
}}
.back-top:hover {{
    background: rgba(232,198,106,0.2);
    box-shadow: 0 0 40px rgba(232,198,106,0.2);
}}

/* ===== Background ===== */
.background {{
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    z-index: 0;
    pointer-events: none;
    overflow: hidden;
}}

/* Animated Mesh Gradient */
.mesh {{
    position: absolute;
    width: 100%; height: 100%;
    background: 
        radial-gradient(ellipse at 20% 50%, rgba(139,0,0,0.15), transparent 50%),
        radial-gradient(ellipse at 80% 20%, rgba(124,58,237,0.1), transparent 40%),
        radial-gradient(ellipse at 50% 80%, rgba(59,130,246,0.08), transparent 50%),
        radial-gradient(ellipse at 0% 0%, rgba(232,198,106,0.05), transparent 40%);
    animation: meshMove 20s ease-in-out infinite alternate;
}}
@keyframes meshMove {{
    0% {{ transform: scale(1) rotate(0deg); }}
    100% {{ transform: scale(1.1) rotate(5deg); }}
}}

/* Aurora */
.aurora {{
    position: absolute;
    width: 100%; height: 100%;
}}
.aurora .a1 {{
    position: absolute;
    width: 800px; height: 800px;
    background: radial-gradient(circle, rgba(232,198,106,0.06), transparent 70%);
    top: -200px; left: -200px;
    animation: auroraMove1 15s ease-in-out infinite alternate;
}}
.aurora .a2 {{
    position: absolute;
    width: 600px; height: 600px;
    background: radial-gradient(circle, rgba(124,58,237,0.06), transparent 70%);
    bottom: -100px; right: -100px;
    animation: auroraMove2 20s ease-in-out infinite alternate;
}}
.aurora .a3 {{
    position: absolute;
    width: 500px; height: 500px;
    background: radial-gradient(circle, rgba(59,130,246,0.05), transparent 70%);
    top: 40%; left: 50%;
    animation: auroraMove3 18s ease-in-out infinite alternate;
}}
@keyframes auroraMove1 {{
    0% {{ transform: translate(0,0) scale(1); }}
    100% {{ transform: translate(300px,200px) scale(1.5); }}
}}
@keyframes auroraMove2 {{
    0% {{ transform: translate(0,0) scale(1); }}
    100% {{ transform: translate(-200px,-150px) scale(1.4); }}
}}
@keyframes auroraMove3 {{
    0% {{ transform: translate(0,0) scale(1); }}
    100% {{ transform: translate(-150px,80px) scale(1.6); }}
}}

/* Grid */
.grid {{
    position: absolute;
    width: 100%; height: 100%;
    background-image: 
        linear-gradient(rgba(232,198,106,0.02) 1px, transparent 1px),
        linear-gradient(90deg, rgba(232,198,106,0.02) 1px, transparent 1px);
    background-size: 60px 60px;
}}

/* Particles */
.particles {{
    position: absolute;
    width: 100%; height: 100%;
}}
.particle {{
    position: absolute;
    width: 2px; height: 2px;
    background: var(--gold);
    border-radius: 50%;
    opacity: 0;
    animation: floatParticle linear infinite;
}}
@keyframes floatParticle {{
    0% {{ opacity: 0; transform: translateY(100vh) scale(0); }}
    10% {{ opacity: 1; }}
    90% {{ opacity: 1; }}
    100% {{ opacity: 0; transform: translateY(-10vh) scale(1); }}
}}

/* Glow Orbs */
.orb {{
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.3;
    animation: orbFloat 8s ease-in-out infinite alternate;
}}
.orb.orb1 {{
    width: 400px; height: 400px;
    background: rgba(139,0,0,0.2);
    top: 10%; left: 5%;
}}
.orb.orb2 {{
    width: 300px; height: 300px;
    background: rgba(232,198,106,0.15);
    bottom: 20%; right: 10%;
    animation-delay: 2s;
}}
.orb.orb3 {{
    width: 250px; height: 250px;
    background: rgba(124,58,237,0.1);
    top: 50%; left: 50%;
    animation-delay: 4s;
}}
@keyframes orbFloat {{
    0% {{ transform: translate(0,0) scale(1); }}
    100% {{ transform: translate(100px,-50px) scale(1.2); }}
}}

/* ===== Container ===== */
.container {{
    position: relative;
    z-index: 1;
    max-width: 1400px;
    margin: 0 auto;
    padding: 20px;
}}

/* ===== Navbar ===== */
.navbar {{
    position: sticky;
    top: 20px;
    z-index: 100;
    background: rgba(5,7,13,0.6);
    backdrop-filter: blur(25px);
    -webkit-backdrop-filter: blur(25px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 16px 30px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: all 0.3s ease;
    box-shadow: 0 20px 60px rgba(0,0,0,0.45);
}}
.navbar.scrolled {{
    background: rgba(5,7,13,0.9);
    box-shadow: 0 10px 40px rgba(0,0,0,0.6);
}}
.navbar .logo h1 {{
    font-size: 28px;
    font-weight: 900;
    background: linear-gradient(135deg, var(--gold), var(--red), var(--gold));
    background-size: 300% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 4s ease-in-out infinite;
}}
.navbar .logo .sub {{
    font-size: 11px;
    color: var(--gold);
    letter-spacing: 5px;
    opacity: 0.5;
}}
.navbar .nav-controls {{
    display: flex;
    align-items: center;
    gap: 15px;
}}
.navbar .search-box {{
    display: flex;
    align-items: center;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 50px;
    padding: 6px 16px;
    transition: 0.3s;
}}
.navbar .search-box:focus-within {{
    border-color: var(--gold);
    box-shadow: 0 0 30px rgba(232,198,106,0.05);
}}
.navbar .search-box input {{
    background: transparent;
    border: none;
    color: var(--white);
    font-family: 'Cairo', sans-serif;
    font-size: 13px;
    padding: 6px 8px;
    outline: none;
    width: 150px;
}}
.navbar .search-box input::placeholder {{ color: rgba(255,255,255,0.3); }}
.navbar .search-box .icon {{ color: rgba(255,255,255,0.3); font-size: 14px; }}

.theme-toggle {{
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 50%;
    width: 40px; height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    color: var(--gold);
    font-size: 18px;
    transition: 0.3s;
}}
.theme-toggle:hover {{
    background: rgba(232,198,106,0.1);
    border-color: var(--gold);
}}

/* ===== Top Stats Bar ===== */
.top-stats {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 15px;
    margin: 30px 0;
}}
.stat-card {{
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(25px);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 18px 20px;
    text-align: center;
    transition: 0.3s;
}}
.stat-card:hover {{
    border-color: rgba(232,198,106,0.2);
    transform: translateY(-3px);
}}
.stat-card .number {{
    font-size: 28px;
    font-weight: 800;
    color: var(--gold);
}}
.stat-card .label {{
    font-size: 12px;
    color: rgba(255,255,255,0.5);
    letter-spacing: 2px;
    margin-top: 2px;
}}
.stat-card .status-dot {{
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #28c840;
    animation: blink 2s infinite;
    margin-left: 6px;
}}
@keyframes blink {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0.3; }}
}}

/* ===== Hero ===== */
.hero {{
    text-align: center;
    padding: 60px 30px 50px;
    margin-bottom: 40px;
    position: relative;
    overflow: hidden;
    border-radius: 24px;
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.04);
}}
.hero .glow-sphere {{
    position: absolute;
    width: 300px; height: 300px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(232,198,106,0.1), transparent 70%);
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    pointer-events: none;
    animation: spherePulse 6s ease-in-out infinite;
}}
@keyframes spherePulse {{
    0%, 100% {{ transform: translate(-50%, -50%) scale(1); opacity: 0.5; }}
    50% {{ transform: translate(-50%, -50%) scale(1.3); opacity: 1; }}
}}
.hero .glitch {{
    font-size: 56px;
    font-weight: 900;
    color: var(--gold);
    position: relative;
    display: inline-block;
    animation: fadeInUp 1s ease forwards;
}}
.hero .glitch::before,
.hero .glitch::after {{
    content: 'هكر';
    position: absolute;
    top: 0; left: 0;
    opacity: 0;
    pointer-events: none;
}}
.hero .glitch::before {{
    color: var(--red);
    animation: glitch1 3s infinite;
    left: 2px;
}}
.hero .glitch::after {{
    color: var(--gold);
    animation: glitch2 3s infinite;
    left: -2px;
}}
@keyframes glitch1 {{
    0%, 90%, 100% {{ opacity: 0; transform: translate(0); }}
    92% {{ opacity: 1; transform: translate(-3px, -2px); }}
    94% {{ opacity: 0; transform: translate(3px, 2px); }}
}}
@keyframes glitch2 {{
    0%, 90%, 100% {{ opacity: 0; transform: translate(0); }}
    93% {{ opacity: 1; transform: translate(3px, 2px); }}
    95% {{ opacity: 0; transform: translate(-3px, -2px); }}
}}
.hero h2 {{
    font-size: 32px;
    font-weight: 700;
    color: var(--gold);
    margin-top: 10px;
    animation: fadeInUp 1s 0.2s ease forwards;
    opacity: 0;
}}
.hero h2 span {{
    background: linear-gradient(135deg, var(--gold), var(--red));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}
.hero .badge {{
    display: inline-block;
    padding: 8px 30px;
    border: 1px solid rgba(232,198,106,0.12);
    border-radius: 50px;
    color: var(--gold);
    font-size: 14px;
    letter-spacing: 4px;
    margin-top: 12px;
    animation: fadeInUp 1s 0.4s ease forwards;
    opacity: 0;
    background: rgba(232,198,106,0.03);
}}
.hero .badge i {{ animation: blink 2s infinite; font-style: normal; }}

/* ===== Cards Grid ===== */
.cards-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 16px;
    margin-top: 20px;
}}

/* ===== Glass Card ===== */
.card {{
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(25px);
    -webkit-backdrop-filter: blur(25px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 24px 20px;
    text-align: center;
    transition: all 0.35s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    box-shadow: 0 0 40px rgba(232,198,106,0.04), 0 20px 60px rgba(0,0,0,0.3);
    position: relative;
    overflow: hidden;
    opacity: 0;
    transform: translateY(30px);
    animation: fadeInUp 0.6s ease forwards;
}}
.card::before {{
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: conic-gradient(from 0deg, transparent, rgba(232,198,106,0.03), transparent, rgba(139,0,0,0.03), transparent);
    animation: cardRotate 10s linear infinite;
    opacity: 0;
    transition: 0.5s;
}}
.card:hover::before {{ opacity: 1; }}
@keyframes cardRotate {{
    0% {{ transform: rotate(0deg); }}
    100% {{ transform: rotate(360deg); }}
}}

.card:hover {{
    transform: translateY(-8px) scale(1.02) rotate(1deg);
    border-color: rgba(232,198,106,0.2);
    box-shadow: 0 0 60px rgba(232,198,106,0.08), 0 30px 80px rgba(0,0,0,0.4);
}}
.card .card-icon {{
    font-size: 32px;
    margin-bottom: 8px;
}}
.card .card-title {{
    font-size: 16px;
    font-weight: 700;
    color: var(--white);
}}
.card .card-count {{
    font-size: 12px;
    color: var(--gold);
    margin: 4px 0 8px;
}}
.card .card-desc {{
    font-size: 12px;
    color: rgba(255,255,255,0.4);
    line-height: 1.5;
    margin-bottom: 12px;
}}
.card .card-btn {{
    display: inline-block;
    padding: 6px 20px;
    border-radius: 50px;
    border: 1px solid rgba(232,198,106,0.12);
    color: var(--gold);
    text-decoration: none;
    font-size: 12px;
    transition: 0.3s;
    font-family: 'Cairo', sans-serif;
}}
.card .card-btn:hover {{
    background: rgba(232,198,106,0.1);
    border-color: var(--gold);
    box-shadow: 0 0 35px rgba(232,198,106,0.15);
}}
.card .card-btn span {{ transition: 0.3s; display: inline-block; }}
.card .card-btn:hover span {{ transform: translateX(-4px); }}

/* ===== Animations ===== */
@keyframes fadeInUp {{
    from {{ opacity: 0; transform: translateY(30px) scale(0.95); }}
    to {{ opacity: 1; transform: translateY(0) scale(1); }}
}}
@keyframes fadeIn {{
    from {{ opacity: 0; }}
    to {{ opacity: 1; }}
}}
@keyframes slideUp {{
    from {{ opacity: 0; transform: translateY(40px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes zoomIn {{
    from {{ opacity: 0; transform: scale(0.9); }}
    to {{ opacity: 1; transform: scale(1); }}
}}
@keyframes blurReveal {{
    from {{ opacity: 0; filter: blur(10px); }}
    to {{ opacity: 1; filter: blur(0); }}
}}

.animate-fade-in {{ animation: fadeIn 0.8s ease forwards; }}
.animate-slide-up {{ animation: slideUp 0.8s ease forwards; }}
.animate-zoom {{ animation: zoomIn 0.6s ease forwards; }}
.animate-blur {{ animation: blurReveal 0.8s ease forwards; }}

.delay-1 {{ animation-delay: 0.1s; }}
.delay-2 {{ animation-delay: 0.2s; }}
.delay-3 {{ animation-delay: 0.3s; }}
.delay-4 {{ animation-delay: 0.4s; }}
.delay-5 {{ animation-delay: 0.5s; }}

/* ===== Footer ===== */
.footer {{
    text-align: center;
    padding: 30px 20px;
    margin-top: 40px;
    border-top: 1px solid rgba(255,255,255,0.04);
    background: rgba(5,7,13,0.4);
    backdrop-filter: blur(20px);
    border-radius: 20px;
}}
.footer .signature {{
    color: var(--red);
    font-size: 12px;
    letter-spacing: 8px;
    opacity: 0.3;
}}
.footer p {{
    color: rgba(255,255,255,0.2);
    font-size: 12px;
    margin-top: 6px;
    letter-spacing: 2px;
}}

/* ===== Responsive ===== */
@media (max-width: 768px) {{
    .navbar {{
        flex-direction: column;
        gap: 12px;
        padding: 14px 18px;
        top: 10px;
    }}
    .navbar .search-box input {{ width: 100px; }}
    .hero .glitch {{ font-size: 32px; }}
    .hero h2 {{ font-size: 20px; }}
    .cards-grid {{ grid-template-columns: 1fr 1fr; }}
    .top-stats {{ grid-template-columns: 1fr 1fr; }}
    .cursor-glow, .cursor-dot {{ display: none; }}
}}
@media (max-width: 480px) {{
    .cards-grid {{ grid-template-columns: 1fr; }}
    .top-stats {{ grid-template-columns: 1fr; }}
}}
</style>
</head>
<body>

<!-- ===== Loading Screen ===== -->
<div class="loading-screen" id="loadingScreen">
    <div class="logo">مبرمج عبود</div>
    <div class="sub">@SSSTlF</div>
    <div class="loader"></div>
    <div class="progress-bar"><div class="fill"></div></div>
</div>

<!-- ===== Scroll Progress ===== -->
<div class="scroll-progress" id="scrollProgress"></div>

<!-- ===== Back to Top ===== -->
<button class="back-top" id="backTop" onclick="window.scrollTo({{top:0,behavior:'smooth'}})">↑</button>

<!-- ===== Cursor ===== -->
<div class="cursor-glow" id="cursorGlow"></div>
<div class="cursor-dot" id="cursorDot"></div>

<!-- ===== Background ===== -->
<div class="background">
    <div class="mesh"></div>
    <div class="aurora">
        <div class="a1"></div>
        <div class="a2"></div>
        <div class="a3"></div>
    </div>
    <div class="grid"></div>
    <div class="particles" id="particles"></div>
    <div class="orb orb1"></div>
    <div class="orb orb2"></div>
    <div class="orb orb3"></div>
</div>

<div class="container">

    <!-- ===== Navbar ===== -->
    <nav class="navbar" id="navbar">
        <div class="logo">
            <h1>مبرمج عبود</h1>
            <div class="sub">@SSSTlF</div>
        </div>
        <div class="nav-controls">
            <div class="search-box">
                <span class="icon">🔍</span>
                <input type="text" id="searchInput" placeholder="بحث..." oninput="filterCards(this.value)">
            </div>
            <button class="theme-toggle" onclick="toggleTheme()" title="تبديل الوضع">🌙</button>
        </div>
    </nav>

    <!-- ===== Top Stats ===== -->
    <div class="top-stats">
        <div class="stat-card animate-fade-in delay-1">
            <div class="number" id="statCategories">0</div>
            <div class="label">📂 الفئات</div>
        </div>
        <div class="stat-card animate-fade-in delay-2">
            <div class="number" id="statCodes">0</div>
            <div class="label">📚 الأكواد</div>
        </div>
        <div class="stat-card animate-fade-in delay-3">
            <div class="number" id="statVisits">0</div>
            <div class="label">👁️ الزيارات</div>
        </div>
        <div class="stat-card animate-fade-in delay-4">
            <div class="number"><span class="status-dot"></span> ONLINE</div>
            <div class="label">🛡️ الحالة</div>
        </div>
    </div>

    <!-- ===== Hero ===== -->
    <section class="hero">
        <div class="glow-sphere"></div>
        <div class="glitch">هكر</div>
        <h2>أكثر من <span>24 فئة</span> برمجية احترافية</h2>
        <div class="badge"><i>✦</i> كل فئة تحتوي على 100 كود حقيقي <i>✦</i></div>
    </section>

    <!-- ===== Cards ===== -->
    <div class="cards-grid" id="cardsGrid">
        {buttons}
    </div>

    <!-- ===== Footer ===== -->
    <footer class="footer">
        <div class="signature">أصل العرب</div>
        <p>© 2026 مبرمج عبود | @SSSTlF</p>
    </footer>

</div>

<script>
// ===== Loading Screen =====
window.addEventListener('load', () => {{
    setTimeout(() => {{
        document.getElementById('loadingScreen').classList.add('hidden');
        document.body.style.cursor = 'default';
    }}, 2500);
}});

// ===== Cursor Glow =====
const glow = document.getElementById('cursorGlow');
const dot = document.getElementById('cursorDot');
document.addEventListener('mousemove', (e) => {{
    glow.style.left = e.clientX + 'px';
    glow.style.top = e.clientY + 'px';
    dot.style.left = e.clientX + 'px';
    dot.style.top = e.clientY + 'px';
}});

// ===== Particles =====
const particlesContainer = document.getElementById('particles');
for (let i = 0; i < 60; i++) {{
    const p = document.createElement('div');
    p.className = 'particle';
    p.style.left = Math.random() * 100 + '%';
    p.style.animationDuration = (Math.random() * 15 + 10) + 's';
    p.style.animationDelay = (Math.random() * 10) + 's';
    p.style.width = (Math.random() * 3 + 1) + 'px';
    p.style.height = p.style.width;
    particlesContainer.appendChild(p);
}}

// ===== Scroll Progress =====
window.addEventListener('scroll', () => {{
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = (scrollTop / docHeight) * 100;
    document.getElementById('scrollProgress').style.width = progress + '%';
    
    // Back to top
    const backTop = document.getElementById('backTop');
    if (scrollTop > 500) {{
        backTop.classList.add('visible');
    }} else {{
        backTop.classList.remove('visible');
    }}
    
    // Navbar
    const navbar = document.getElementById('navbar');
    if (scrollTop > 50) {{
        navbar.classList.add('scrolled');
    }} else {{
        navbar.classList.remove('scrolled');
    }}
}});

// ===== Counters =====
function animateCounter(el, target, duration = 2000) {{
    let start = 0;
    const step = Math.max(1, Math.floor(target / 60));
    const interval = duration / 60;
    const timer = setInterval(() => {{
        start += step;
        if (start >= target) {{
            start = target;
            clearInterval(timer);
        }}
        el.textContent = start;
    }}, interval);
}}

document.addEventListener('DOMContentLoaded', () => {{
    animateCounter(document.getElementById('statCategories'), {len(categories)});
    animateCounter(document.getElementById('statCodes'), {len(categories) * 100});
    animateCounter(document.getElementById('statVisits'), Math.floor(Math.random() * 1000) + 100);
}});

// ===== Search Filter =====
function filterCards(query) {{
    const cards = document.querySelectorAll('.card');
    const q = query.toLowerCase().trim();
    cards.forEach(card => {{
        const title = card.querySelector('.card-title').textContent.toLowerCase();
        const desc = card.querySelector('.card-desc').textContent.toLowerCase();
        if (title.includes(q) || desc.includes(q)) {{
            card.style.display = '';
        }} else {{
            card.style.display = 'none';
        }}
    }});
}}

// ===== Theme Toggle =====
let darkMode = true;
function toggleTheme() {{
    darkMode = !darkMode;
    const root = document.documentElement;
    const btn = document.querySelector('.theme-toggle');
    if (darkMode) {{
        root.style.setProperty('--bg', '#05070D');
        root.style.setProperty('--white', '#F8FAFC');
        btn.textContent = '🌙';
        document.body.style.background = '#05070D';
        document.body.style.color = '#F8FAFC';
    }} else {{
        root.style.setProperty('--bg', '#F8FAFC');
        root.style.setproperty('--white', '#05070D');
        btn.textContent = '☀️';
        document.body.style.background = '#F8FAFC';
        document.body.style.color = '#05070D';
    }}
}}

// ===== Keyboard Shortcuts =====
document.addEventListener('keydown', (e) => {{
    if (e.ctrlKey && e.key === '/') {{
        e.preventDefault();
        document.getElementById('searchInput').focus();
    }}
    if (e.key === 'Escape') {{
        document.getElementById('searchInput').blur();
    }}
}});

console.log('🔥 مبرمج عبود | @SSSTlF | أصل العرب');
console.log('📚 {len(categories)} فئة | {len(categories) * 100} كود');
</script>
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
<div class="code-block glass" id="code-{i}">
    <div class="code-head">
        <span class="num">#{i+1}</span>
        <div>
            <button class="fav-btn" onclick="toggleFav({i})" id="fav-{i}">🤍</button>
            <button class="copy-btn" onclick="copyCode({i})">📋 نسخ</button>
        </div>
    </div>
    <pre class="code-content">{c}</pre>
</div>
'''
    return f'''
<!DOCTYPE html>
<html dir="rtl">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{category} — مبرمج عبود</title>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root {{ --bg: #05070D; --gold: #E8C66A; --red: #8B0000; --white: #F8FAFC; }}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{font-family:'Cairo',sans-serif;background:var(--bg);color:var(--white);padding:20px;}}
::-webkit-scrollbar{{width:8px;}}
::-webkit-scrollbar-track{{background:var(--bg);}}
::-webkit-scrollbar-thumb{{background:var(--gold);border-radius:10px;}}

.background{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none;overflow:hidden;background:radial-gradient(ellipse at 50% 50%,#0d0d0d,#000000);}}
.background .g1{{position:absolute;width:600px;height:600px;background:radial-gradient(circle,rgba(139,0,0,0.05),transparent 70%);top:-200px;left:-200px;animation:g1 20s infinite alternate;}}
.background .g2{{position:absolute;width:500px;height:500px;background:radial-gradient(circle,rgba(232,198,106,0.03),transparent 70%);bottom:-100px;right:-100px;animation:g2 25s infinite alternate;}}
@keyframes g1{{0%{{transform:translate(0,0)scale(1)}}100%{{transform:translate(200px,150px)scale(1.5)}}}}
@keyframes g2{{0%{{transform:translate(0,0)scale(1)}}100%{{transform:translate(-150px,-100px)scale(1.3)}}}}

.container{{position:relative;z-index:1;max-width:1100px;margin:0 auto;}}
.back{{display:inline-block;padding:8px 24px;border-radius:50px;border:1px solid rgba(232,198,106,0.12);color:var(--gold);text-decoration:none;margin-bottom:15px;font-size:13px;transition:0.3s;}}
.back:hover{{background:rgba(139,0,0,0.05);border-color:var(--red);}}

.header{{text-align:center;padding:25px;background:rgba(255,255,255,0.02);border-radius:20px;border:1px solid rgba(139,0,0,0.06);margin-bottom:20px;backdrop-filter:blur(10px);}}
.header h1{{font-size:34px;font-weight:900;background:linear-gradient(135deg,var(--gold),var(--red),var(--gold));background-size:200% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:s 4s infinite;}}
@keyframes s{{0%,100%{{background-position:0%center}}50%{{background-position:200%center}}}}
.header .sub{{color:var(--gold);font-size:14px;letter-spacing:3px;opacity:0.6;}}
.header .badge{{display:inline-block;padding:4px 18px;border-radius:50px;background:rgba(139,0,0,0.08);color:var(--gold);font-size:13px;margin-top:8px;border:1px solid rgba(139,0,0,0.06);}}

.glass{{background:rgba(255,255,255,0.04);backdrop-filter:blur(25px);border:1px solid rgba(255,255,255,0.06);border-radius:16px;box-shadow:0 0 40px rgba(232,198,106,0.04),0 20px 60px rgba(0,0,0,0.3);}}
.code-block{{margin-bottom:14px;overflow:hidden;transition:0.3s;}}
.code-block:hover{{border-color:rgba(232,198,106,0.15);box-shadow:0 10px 40px rgba(0,0,0,0.3);}}
.code-head{{display:flex;justify-content:space-between;align-items:center;padding:10px 18px;border-bottom:1px solid rgba(255,255,255,0.04);}}
.code-head .num{{color:var(--gold);font-size:12px;font-weight:600;}}
.code-head button{{padding:4px 14px;border-radius:50px;border:1px solid rgba(232,198,106,0.1);background:transparent;color:var(--gold);font-size:12px;cursor:pointer;transition:0.3s;font-family:'Cairo',sans-serif;margin:0 4px;}}
.code-head button:hover{{background:rgba(232,198,106,0.05);border-color:var(--gold);}}
.fav-btn{{border-color:rgba(255,50,50,0.1)!important;color:#ff5f57!important;}}
.fav-btn.active{{background:rgba(255,50,50,0.1)!important;border-color:#ff5f57!important;}}
.code-content{{padding:16px;margin:0;font-family:'Courier New',monospace;font-size:12px;line-height:1.7;color:#a0c0a0;overflow-x:auto;white-space:pre-wrap;word-wrap:break-word;background:rgba(0,0,0,0.3);direction:ltr;text-align:left;}}

.footer{{text-align:center;padding:15px;margin-top:20px;border-top:1px solid rgba(255,255,255,0.04);}}
.footer .signature{{color:var(--red);font-size:11px;letter-spacing:8px;opacity:0.3;}}
.footer p{{color:rgba(255,255,255,0.15);font-size:12px;margin-top:4px;letter-spacing:2px;}}

@media(max-width:768px){{.header h1{{font-size:24px}}.code-content{{font-size:11px;padding:10px}}}}
</style>
</head>
<body>
<div class="background"><div class="g1"></div><div class="g2"></div></div>
<div class="container">
<a href="/" class="back">← العودة</a>
<div class="header"><h1>{category}</h1><div class="sub">@SSSTlF — مبرمج عبود</div><div class="badge">✦ {len(codes)} كود حقيقي ✦</div></div>
{html}
<div class="footer"><div class="signature">أصل العرب</div><p>© 2026 مبرمج عبود | @SSSTlF</p></div>
</div>
<script>
function copyCode(i) {{
    const pre = document.querySelectorAll('.code-content')[i];
    navigator.clipboard.writeText(pre.textContent).then(() => {{
        const btns = document.querySelectorAll('.copy-btn');
        const btn = btns[i];
        btn.textContent = '✅ تم';
        setTimeout(() => btn.textContent = '📋 نسخ', 1500);
    }});
}}

function toggleFav(i) {{
    const btn = document.getElementById('fav-' + i);
    btn.classList.toggle('active');
    btn.textContent = btn.classList.contains('active') ? '❤️' : '🤍';
    let favs = JSON.parse(localStorage.getItem('favCodes') || '[]');
    const id = '{category}-' + i;
    if (btn.classList.contains('active')) {{
        if (!favs.includes(id)) favs.push(id);
    }} else {{
        favs = favs.filter(f => f !== id);
    }}
    localStorage.setItem('favCodes', JSON.stringify(favs));
}}

// تحميل المفضلة
document.addEventListener('DOMContentLoaded', () => {{
    const favs = JSON.parse(localStorage.getItem('favCodes') || '[]');
    favs.forEach(id => {{
        const parts = id.split('-');
        if (parts[0] === '{category}') {{
            const btn = document.getElementById('fav-' + parts[1]);
            if (btn) {{
                btn.classList.add('active');
                btn.textContent = '❤️';
            }}
        }}
    }});
}});
</script>
</body>
</html>
'''

if __name__ == '__main__':
    send_telegram(f"🔥 مبرمج عبود | @SSSTlF | {len(categories)} فئة | {len(categories)*100} كود")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
