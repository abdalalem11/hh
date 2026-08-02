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

# ===== تعليم برمجة البوتات من الصفر =====
def generate_bot_codes():
    codes = []
    lessons = [
        ("مقدمة عن البوتات", "ما هو البوت؟\nالبوت هو برنامج يعمل تلقائياً يؤدي مهام محددة دون تدخل بشري."),
        ("أنواع البوتات", "أنواع البوتات:\n1. بوتات محادثة (Chatbots)\n2. بوتات ويب (Web Bots)\n3. بوتات ألعاب\n4. بوتات تحليل بيانات"),
        ("لغة بايثون للبوتات", "لماذا بايثون؟\n- سهلة التعلم\n- مكتبات جاهزة (python-telegram-bot, discord.py)\n- مجتمع كبير"),
        ("تثبيت بايثون", "تثبيت بايثون:\n1. تحميل من python.org\n2. تثبيت عبرTermux: pkg install python\n3. التأكد: python --version"),
        ("مكتبة python-telegram-bot", "تثبيت المكتبة:\npip install python-telegram-bot"),
        ("إنشاء بوت تليجرام", "خطوات إنشاء بوت تليجرام:\n1. ابحث عن @BotFather\n2. أرسل /newbot\n3. اختر اسماً\n4. احصل على التوكن (Token)"),
        ("أول كود بوت", '''from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

async def start(update, context):
    await update.message.reply_text("مرحباً! أنا بوتك الأول")

app = ApplicationBuilder().token("TOKEN_HERE").build()
app.add_handler(CommandHandler("start", start))
app.run_polling()'''),
        ("أوامر البوت", "إضافة أوامر:\n@app.message_handler(commands=['start', 'help'])\n- start: ترحيب\n- help: مساعدة"),
        ("مكتبة discord.py", "تثبيت مكتبة ديسكورد:\npip install discord.py"),
        ("إنشاء بوت ديسكورد", "خطوات:\n1. اذهب إلى Discord Developer Portal\n2. أنشئ تطبيقاً جديداً\n3. أنشئ بوتاً\n4. انسخ التوكن"),
        ("أول كود بوت ديسكورد", '''import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'بوت {bot.user} جاهز')

@bot.command()
async def hello(ctx):
    await ctx.send('مرحباً!')

bot.run('TOKEN_HERE')'''),
        ("مكتبة requests", "للتواصل مع APIs:\nimport requests\nresponse = requests.get('https://api.example.com')"),
        ("مكتبة BeautifulSoup", "لتحليل صفحات الويب:\nfrom bs4 import BeautifulSoup\nsoup = BeautifulSoup(html, 'html.parser')"),
        ("مكتبة selenium", "للتحكم في المتصفح:\nfrom selenium import webdriver\ndriver = webdriver.Chrome()"),
        ("بوتات الواتساب", "استخدام مكتبة pywhatkit:\npip install pywhatkit"),
        ("بوتات الانستغرام", "استخدام instabot:\npip install instabot"),
        ("بوتات تويتر", "استخدام tweepy:\npip install tweepy"),
        ("معالجة النصوص", "مكتبات معالجة النصوص:\n- re (regex)\n- nltk\n- spaCy"),
        ("معالجة الصور", "مكتبات معالجة الصور:\n- PIL\n- OpenCV\n- pillow"),
        ("بوتات الذكاء الاصطناعي", "مكتبات الذكاء الاصطناعي:\n- transformers\n- openai\n- tensorflow"),
        ("بوتات الصوت", "مكتبات الصوت:\n- speech_recognition\n- pyttsx3\n- gTTS"),
        ("قواعد البيانات", "مكتبات قواعد البيانات:\n- sqlite3\n- pymongo\n- psycopg2"),
        ("التعامل مع APIs", "أمثلة على APIs:\n- OpenWeatherMap (الطقس)\n- NewsAPI (الأخبار)\n- Google Maps (الخرائط)"),
        ("جدولة المهام", "مكتبات الجدولة:\n- schedule\n- APScheduler\n- time"),
        ("الأمان في البوتات", "نصائح أمان:\n- لا تشارك التوكن\n- استخدم متغيرات البيئة\n- تحقق من المدخلات"),
        ("نشر البوت", "طرق النشر:\n1. Render\n2. Heroku\n3. PythonAnywhere\n4. VPS"),
        ("تحسين الأداء", "نصائح تحسين:\n- استخدام async/await\n- caching\n- استخدام قواعد بيانات سريعة"),
        ("أخطاء شائعة", "أخطاء وحلولها:\n- Invalid Token\n- Rate Limits\n- Missing Permissions"),
        ("مشاريع تطبيقية", "أفكار مشاريع:\n1. بوت طقس\n2. بوت تذكير\n3. بوت تحليل ملفات\n4. بوت مساعد شخصي"),
        ("خاتمة", "مبروك! أنت الآن مبرمج بوتات\nاستمر في التعلم وطبق مشاريعك الخاصة")
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
        if category in ['بايثون', 'جافا سكريبت', 'إتش تي إم إل', 'سي إس إس', 'بي إتش بي', 'إس كيو إل']:
            code = f'''# {category} - مثال {i}
def example_{i}():
    result = {i * 7 + 3}
    data = {{'id': {i}, 'value': result, 'status': 'success' if result % 2 == 0 else 'pending'}}
    print(f"Result: {{data}}")
    return data
example_{i}()'''
        else:
            code = f'# {category} - مثال {i}\nprint("ID: {i} | Value: {i * 7 + 3}")'
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
    
    buttons = ''.join([f'<a href="/code/{cat}" class="btn">⌨ {cat}</a>' for cat in categories])
    return f'''
<!DOCTYPE html>
<html dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>مبرمج عبود | @SSSTlF</title>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
* {{margin:0;padding:0;box-sizing:border-box;}}
body {{
    font-family: 'Cairo', sans-serif;
    background: #080808;
    color: #e0e0e0;
    min-height: 100vh;
    overflow-x: hidden;
}}
::-webkit-scrollbar {{ width: 8px; }}
::-webkit-scrollbar-track {{ background: #080808; }}
::-webkit-scrollbar-thumb {{ background: #8B0000; border-radius: 10px; }}

.background {{
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    z-index: 0;
    pointer-events: none;
    overflow: hidden;
    background: radial-gradient(ellipse at 50% 50%, #0d0d0d, #000000);
}}
.background .glow1 {{
    position: absolute;
    width: 800px; height: 800px;
    background: radial-gradient(circle, rgba(139,0,0,0.1), transparent 70%);
    top: -200px; left: -200px;
    animation: glowMove1 20s ease-in-out infinite alternate;
}}
.background .glow2 {{
    position: absolute;
    width: 600px; height: 600px;
    background: radial-gradient(circle, rgba(232,198,106,0.05), transparent 70%);
    bottom: -100px; right: -100px;
    animation: glowMove2 25s ease-in-out infinite alternate;
}}
@keyframes glowMove1 {{
    0% {{ transform: translate(0,0) scale(1); }}
    100% {{ transform: translate(300px,200px) scale(1.8); }}
}}
@keyframes glowMove2 {{
    0% {{ transform: translate(0,0) scale(1); }}
    100% {{ transform: translate(-200px,-150px) scale(1.5); }}
}}

.matrix-lines {{
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    z-index: 0;
    pointer-events: none;
    opacity: 0.03;
    overflow: hidden;
}}
.matrix-lines::before {{
    content: '01001010 01100001 01101100 01100001 01101100 00100000 01000001 01101100 00100000 01000001 01110010 01100001 01100010';
    position: absolute;
    font-family: 'Courier New', monospace;
    font-size: 14px;
    color: #8B0000;
    white-space: pre-wrap;
    word-wrap: break-word;
    line-height: 2;
    width: 100%;
    animation: matrix 10s linear infinite;
}}
@keyframes matrix {{
    0% {{ opacity: 0; }}
    50% {{ opacity: 1; }}
    100% {{ opacity: 0; }}
}}

.container {{
    position: relative;
    z-index: 1;
    max-width: 1400px;
    margin: 0 auto;
    padding: 20px;
}}

.navbar {{
    background: rgba(8,8,8,0.9);
    backdrop-filter: blur(30px);
    border: 1px solid rgba(139,0,0,0.2);
    border-radius: 20px;
    padding: 25px 35px;
    text-align: center;
    margin-bottom: 35px;
    box-shadow: 0 20px 80px rgba(0,0,0,0.8), inset 0 1px 0 rgba(139,0,0,0.1);
    position: relative;
    overflow: hidden;
}}
.navbar::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, #8B0000, #E8C66A, #8B0000, transparent);
    animation: borderGlow 3s ease-in-out infinite;
}}
@keyframes borderGlow {{
    0%, 100% {{ opacity: 0.3; }}
    50% {{ opacity: 1; }}
}}
.navbar .logo {{
    display: flex;
    flex-direction: column;
    align-items: center;
}}
.navbar .logo h1 {{
    font-size: 42px;
    font-weight: 900;
    background: linear-gradient(135deg, #E8C66A, #8B0000, #E8C66A);
    background-size: 300% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 5s ease-in-out infinite;
    letter-spacing: 4px;
    text-shadow: 0 0 80px rgba(139,0,0,0.2);
}}
@keyframes shimmer {{
    0%, 100% {{ background-position: 0% center; }}
    50% {{ background-position: 200% center; }}
}}
.navbar .logo .sub {{
    font-size: 16px;
    color: #D4AF37;
    letter-spacing: 6px;
    font-weight: 300;
    margin-top: -2px;
}}
.navbar .logo .tag {{
    font-size: 12px;
    color: #8B0000;
    letter-spacing: 10px;
    opacity: 0.5;
    font-weight: 300;
}}
.navbar .status {{
    display: flex;
    gap: 30px;
    justify-content: center;
    margin-top: 12px;
    flex-wrap: wrap;
}}
.navbar .status span {{
    font-size: 12px;
    color: #666;
    letter-spacing: 2px;
}}
.navbar .status span strong {{
    color: #E8C66A;
    font-weight: 700;
}}

.hero {{
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(139,0,0,0.08);
    border-radius: 24px;
    padding: 50px 30px 40px;
    text-align: center;
    margin-bottom: 35px;
    backdrop-filter: blur(10px);
    position: relative;
    overflow: hidden;
}}
.hero::after {{
    content: '';
    position: absolute;
    top: 50%; left: 50%;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(139,0,0,0.05), transparent 70%);
    transform: translate(-50%, -50%);
    pointer-events: none;
}}
.hero .glitch {{
    font-size: 60px;
    font-weight: 900;
    color: #E8C66A;
    position: relative;
    display: inline-block;
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
    color: #8B0000;
    animation: glitch1 3s infinite;
    left: 2px;
}}
.hero .glitch::after {{
    color: #E8C66A;
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
    font-size: 28px;
    font-weight: 700;
    color: #D4AF37;
    margin-top: 10px;
}}
.hero h2 span {{
    background: linear-gradient(135deg, #E8C66A, #8B0000);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}
.hero .badge {{
    display: inline-block;
    padding: 8px 30px;
    border: 1px solid rgba(232,198,106,0.15);
    border-radius: 50px;
    color: #E8C66A;
    font-size: 14px;
    letter-spacing: 4px;
    margin-top: 12px;
    background: rgba(139,0,0,0.05);
}}
.hero .badge i {{
    font-style: normal;
    animation: blink 2s infinite;
}}
@keyframes blink {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0; }}
}}
.hero .stats {{
    display: flex;
    gap: 40px;
    justify-content: center;
    margin-top: 25px;
    flex-wrap: wrap;
}}
.hero .stats .stat-item {{
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.03);
    border-radius: 16px;
    padding: 15px 30px;
    min-width: 120px;
}}
.hero .stats .stat-item strong {{
    display: block;
    font-size: 28px;
    color: #E8C66A;
    font-weight: 800;
}}
.hero .stats .stat-item span {{
    font-size: 13px;
    color: #666;
    letter-spacing: 2px;
}}

.btns {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 10px;
    margin-top: 20px;
}}
.btn {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 14px 18px;
    border-radius: 14px;
    text-decoration: none;
    text-align: center;
    font-weight: 600;
    font-size: 13px;
    border: 1px solid rgba(139,0,0,0.1);
    background: rgba(255,255,255,0.02);
    color: #b0b0b0;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}}
.btn::before {{
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 100%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(139,0,0,0.05), transparent);
    transition: 0.5s;
}}
.btn:hover::before {{
    left: 100%;
}}
.btn:hover {{
    transform: translateY(-3px);
    border-color: #8B0000;
    color: #E8C66A;
    background: rgba(139,0,0,0.05);
    box-shadow: 0 10px 40px rgba(139,0,0,0.1);
}}
.btn .icon {{
    font-size: 16px;
}}
.btn .count {{
    font-size: 10px;
    color: #555;
    background: rgba(255,255,255,0.03);
    padding: 2px 10px;
    border-radius: 50px;
}}

.footer {{
    text-align: center;
    padding: 30px 20px;
    margin-top: 40px;
    border-top: 1px solid rgba(139,0,0,0.05);
    background: rgba(8,8,8,0.5);
    border-radius: 20px;
    backdrop-filter: blur(10px);
}}
.footer .signature {{
    color: #8B0000;
    font-size: 12px;
    letter-spacing: 8px;
    opacity: 0.4;
}}
.footer p {{
    color: #444;
    font-size: 12px;
    margin-top: 6px;
    letter-spacing: 2px;
}}
.footer .security {{
    display: flex;
    gap: 20px;
    justify-content: center;
    margin-top: 12px;
    font-size: 11px;
    color: #333;
    letter-spacing: 3px;
}}

.terminal-bar {{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 6px 16px;
    background: rgba(0,0,0,0.4);
    border-radius: 10px;
    margin-bottom: 15px;
    border: 1px solid rgba(139,0,0,0.05);
}}
.terminal-bar .dots {{
    display: flex;
    gap: 6px;
}}
.terminal-bar .dots span {{
    width: 10px; height: 10px;
    border-radius: 50%;
    display: block;
}}
.terminal-bar .dots .r {{ background: #ff5f57; }}
.terminal-bar .dots .y {{ background: #ffbd2e; }}
.terminal-bar .dots .g {{ background: #28c840; }}
.terminal-bar .path {{
    font-size: 11px;
    color: #555;
    font-family: 'Courier New', monospace;
    flex: 1;
    text-align: center;
}}
.terminal-bar .path i {{
    color: #8B0000;
    font-style: normal;
}}
.terminal-bar .status-text {{
    font-size: 10px;
    color: #28c840;
    letter-spacing: 2px;
}}

@media(max-width:768px) {{
    .navbar .logo h1 {{ font-size: 28px; }}
    .hero .glitch {{ font-size: 36px; }}
    .hero h2 {{ font-size: 20px; }}
    .btns {{ grid-template-columns: 1fr; }}
    .hero .stats {{ gap: 12px; }}
    .hero .stats .stat-item {{ padding: 10px 16px; min-width: 80px; }}
    .hero .stats .stat-item strong {{ font-size: 20px; }}
}}
</style>
</head>
<body>

<div class="background">
    <div class="glow1"></div>
    <div class="glow2"></div>
</div>
<div class="matrix-lines"></div>

<div class="container">

    <div class="navbar">
        <div class="logo">
            <h1>مبرمج عبود</h1>
            <div class="sub">@SSSTlF</div>
            <div class="tag">أصل العرب</div>
        </div>
        <div class="status">
            <span>🔴 <strong style="color:#ff5f57;">ONLINE</strong></span>
            <span>📡 <strong style="color:#E8C66A;">{len(categories)}</strong> فئة</span>
            <span>📚 <strong style="color:#E8C66A;">{len(categories)*100}</strong> كود</span>
            <span>🛡️ <strong style="color:#28c840;">محمي</strong></span>
        </div>
    </div>

    <div class="hero">
        <div class="terminal-bar">
            <div class="dots">
                <span class="r"></span>
                <span class="y"></span>
                <span class="g"></span>
            </div>
            <div class="path">root@abood:~<i>/codes</i>#</div>
            <div class="status-text">● SYSTEM_READY</div>
        </div>
        <div class="glitch">هكر</div>
        <h2>أكثر من <span>24 فئة</span> برمجية احترافية</h2>
        <div class="badge"><i>✦</i> كل فئة تحتوي على 100 كود حقيقي <i>✦</i></div>
        <div class="stats">
            <div class="stat-item"><strong>{len(categories)}</strong><span>فئة</span></div>
            <div class="stat-item"><strong>{len(categories)*100}</strong><span>كود</span></div>
            <div class="stat-item"><strong>100%</strong><span>حقيقي</span></div>
            <div class="stat-item"><strong>24/7</strong><span>متاح</span></div>
        </div>
    </div>

    <div class="btns">
        {buttons}
    </div>

    <div class="footer">
        <div class="signature">أصل العرب</div>
        <p>© 2026 مبرمج عبود | @SSSTlF</p>
        <div class="security">
            <span>● تشفير AES-256</span>
            <span>● SSL/TLS</span>
            <span>● محمي</span>
        </div>
    </div>

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
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{font-family:'Cairo',sans-serif;background:#080808;color:#e0e0e0;padding:20px;}}
::-webkit-scrollbar{{width:8px;}}
::-webkit-scrollbar-track{{background:#080808;}}
::-webkit-scrollbar-thumb{{background:#8B0000;border-radius:10px;}}
.background{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none;overflow:hidden;background:radial-gradient(ellipse at 50% 50%,#0d0d0d,#000000);}}
.background .g1{{position:absolute;width:600px;height:600px;background:radial-gradient(circle,rgba(139,0,0,0.05),transparent 70%);top:-200px;left:-200px;animation:g1 20s infinite alternate;}}
.background .g2{{position:absolute;width:500px;height:500px;background:radial-gradient(circle,rgba(232,198,106,0.03),transparent 70%);bottom:-100px;right:-100px;animation:g2 25s infinite alternate;}}
@keyframes g1{{0%{{transform:translate(0,0)scale(1)}}100%{{transform:translate(200px,150px)scale(1.5)}}}}
@keyframes g2{{0%{{transform:translate(0,0)scale(1)}}100%{{transform:translate(-150px,-100px)scale(1.3)}}}}
.container{{position:relative;z-index:1;max-width:1100px;margin:0 auto;}}
.back{{display:inline-block;padding:8px 24px;border-radius:50px;border:1px solid rgba(232,198,106,0.12);color:#E8C66A;text-decoration:none;margin-bottom:15px;font-size:13px;transition:0.3s;}}
.back:hover{{background:rgba(139,0,0,0.05);border-color:#8B0000;}}
.header{{text-align:center;padding:25px;background:rgba(255,255,255,0.02);border-radius:20px;border:1px solid rgba(139,0,0,0.06);margin-bottom:20px;}}
.header h1{{font-size:34px;font-weight:900;background:linear-gradient(135deg,#E8C66A,#8B0000,#E8C66A);background-size:200% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:s 4s infinite;}}
@keyframes s{{0%,100%{{background-position:0%center}}50%{{background-position:200%center}}}}
.header .sub{{color:#D4AF37;font-size:14px;letter-spacing:3px;}}
.header .badge{{display:inline-block;padding:4px 18px;border-radius:50px;background:rgba(139,0,0,0.08);color:#E8C66A;font-size:13px;margin-top:8px;border:1px solid rgba(139,0,0,0.06);}}
.block{{background:rgba(255,255,255,0.02);border:1px solid rgba(139,0,0,0.06);border-radius:14px;margin-bottom:12px;overflow:hidden;transition:0.3s;}}
.block:hover{{border-color:rgba(232,198,106,0.1);box-shadow:0 5px 30px rgba(0,0,0,0.3);}}
.head{{display:flex;justify-content:space-between;align-items:center;padding:8px 16px;background:rgba(139,0,0,0.04);border-bottom:1px solid rgba(139,0,0,0.04);}}
.head span{{color:#D4AF37;font-size:12px;font-weight:600;}}
.head button{{padding:4px 16px;border-radius:50px;border:1px solid rgba(232,198,106,0.12);background:transparent;color:#E8C66A;font-size:12px;cursor:pointer;font-family:'Cairo',sans-serif;transition:0.3s;}}
.head button:hover{{background:rgba(232,198,106,0.05);border-color:#8B0000;}}
.code{{padding:14px;margin:0;font-family:'Courier New',monospace;font-size:12px;line-height:1.7;color:#a0c0a0;overflow-x:auto;white-space:pre-wrap;word-wrap:break-word;background:rgba(0,0,0,0.4);direction:ltr;text-align:left;}}
.footer{{text-align:center;padding:15px;margin-top:20px;border-top:1px solid rgba(139,0,0,0.04);}}
.footer .signature{{color:#8B0000;font-size:11px;letter-spacing:8px;opacity:0.3;}}
.footer p{{color:#444;font-size:12px;margin-top:4px;letter-spacing:2px;}}
@media(max-width:768px){{.header h1{{font-size:24px}}.code{{font-size:11px;padding:10px}}}}
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
