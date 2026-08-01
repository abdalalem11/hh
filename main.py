from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import json
import datetime
import requests
from urllib.parse import parse_qs

# ===== إعدادات البوت =====
BOT_TOKEN = "8875360747:AAHZH8ti8BTzA8_Gzo6QV6ex4OsaJyoBovI"
CHAT_ID = "1170411845"

# ===== دالة إرسال الإشعار =====
def send_telegram_notification(visitor_info):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        message = f"""👤 **زائر جديد للموقع!**
📅 الوقت: {visitor_info['time']}
🌐 IP: {visitor_info['ip']}
🖥️ المتصفح: {visitor_info['user_agent'][:50]}...
📊 إجمالي الزوار: {visitor_info['total_visitors']}
⭐ التقييم: {visitor_info.get('rating', 'لم يقيم')}
💬 التعليق: {visitor_info.get('comment', 'لا يوجد')}"""
        
        requests.post(url, json={
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }, timeout=5)
    except Exception as e:
        print(f"خطأ في الإرسال: {e}")

# ===== ملف لحفظ الإحصائيات =====
STATS_FILE = "visitors.json"

def load_stats():
    try:
        with open(STATS_FILE, "r") as f:
            return json.load(f)
    except:
        return {"total_visitors": 0, "ratings": [], "comments": []}

def save_stats(stats):
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f)

# ===== خادم موقع عبود =====
class AboodHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            # تسجيل الزائر
            stats = load_stats()
            stats["total_visitors"] += 1
            save_stats(stats)
            
            # إرسال إشعار للبوت
            visitor_info = {
                "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "ip": self.client_address[0],
                "user_agent": self.headers.get("User-Agent", "غير معروف"),
                "total_visitors": stats["total_visitors"]
            }
            send_telegram_notification(visitor_info)
            
            self.send_response(200)
            self.end_headers()
            html = self.get_html(stats)
            self.wfile.write(html.encode("utf-8"))
            
        elif self.path == "/submit-rating":
            self.send_response(302)
            self.send_header("Location", "/")
            self.end_headers()
            
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/submit-rating":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length).decode("utf-8")
            data = parse_qs(post_data)
            
            rating = data.get("rating", ["0"])[0]
            comment = data.get("comment", [" "])[0]
            
            stats = load_stats()
            stats["ratings"].append(int(rating))
            stats["comments"].append({"rating": int(rating), "comment": comment, "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
            save_stats(stats)
            
            # إرسال تقييم للبوت
            visitor_info = {
                "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "ip": self.client_address[0],
                "user_agent": self.headers.get("User-Agent", "غير معروف"),
                "total_visitors": stats["total_visitors"],
                "rating": f"{rating}/5 ⭐",
                "comment": comment if comment else "لا يوجد"
            }
            send_telegram_notification(visitor_info)
            
            self.send_response(302)
            self.send_header("Location", "/")
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def get_html(self, stats):
        # حساب متوسط التقييم
        avg_rating = 0
        if stats["ratings"]:
            avg_rating = sum(stats["ratings"]) / len(stats["ratings"])
        
        return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>عبود | تعليم الأمن السيبراني والاختراقات</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, sans-serif;
            background: #0a0a12;
            min-height: 100vh;
            background-image: radial-gradient(circle at 20% 30%, rgba(0, 200, 100, 0.08), transparent 60%),
                              radial-gradient(circle at 80% 70%, rgba(0, 100, 200, 0.08), transparent 50%);
        }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 20px; }}
        
        .header {{
            display: flex; justify-content: space-between; align-items: center;
            padding: 20px 0; border-bottom: 1px solid rgba(255,255,255,0.06);
            flex-wrap: wrap; gap: 15px;
        }}
        .logo {{
            font-size: 32px; font-weight: 900;
            background: linear-gradient(135deg, #00ff88, #00ccff);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }}
        .logo i {{ -webkit-text-fill-color: initial; color: #00ff88; margin-left: 10px; }}
        .nav-links {{
            display: flex; gap: 25px; list-style: none; font-weight: 600;
            color: #b0baca; flex-wrap: wrap;
        }}
        .nav-links a {{ color: #b0baca; text-decoration: none; transition: 0.3s; }}
        .nav-links a:hover {{ color: #00ff88; }}
        
        .btn {{
            padding: 10px 22px; border: none; border-radius: 40px; font-weight: 700;
            cursor: pointer; transition: 0.3s; text-decoration: none; display: inline-flex;
            align-items: center; gap: 8px; font-size: 14px;
        }}
        .btn-primary {{
            background: linear-gradient(135deg, #00ff88, #00ccff);
            color: #0a0a12;
        }}
        .btn-primary:hover {{ transform: scale(1.04); box-shadow: 0 8px 30px rgba(0,255,136,0.2); }}
        .btn-outline {{
            background: transparent; border: 1.5px solid #00ff88; color: #00ff88;
        }}
        .btn-outline:hover {{ background: #00ff88; color: #0a0a12; }}
        .btn-support {{
            background: linear-gradient(135deg, #ff6b6b, #ee5a24);
            color: #fff;
        }}
        .btn-support:hover {{ transform: scale(1.04); box-shadow: 0 8px 30px rgba(255,107,107,0.3); }}
        .btn-telegram {{
            background: linear-gradient(135deg, #0088cc, #005f8a);
            color: #fff;
        }}
        .btn-telegram:hover {{ transform: scale(1.04); box-shadow: 0 8px 30px rgba(0,136,204,0.3); }}
        .btn-danger {{
            background: linear-gradient(135deg, #ff0000, #cc0000);
            color: #fff;
        }}
        .btn-danger:hover {{ transform: scale(1.04); box-shadow: 0 8px 30px rgba(255,0,0,0.3); }}
        
        /* ===== قسم الإحصائيات والتقييم ===== */
        .stats-section {{
            background: linear-gradient(135deg, rgba(0,255,136,0.05), rgba(0,204,255,0.05));
            border: 1px solid rgba(0,255,136,0.1);
            border-radius: 20px;
            padding: 20px 30px;
            margin: 20px 0 30px;
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            gap: 15px;
        }}
        .stats-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            color: #b0baca;
        }}
        .stats-item i {{ color: #00ff88; font-size: 24px; }}
        .stats-item .number {{
            font-size: 28px; font-weight: 900;
            background: linear-gradient(135deg, #00ff88, #00ccff);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }}
        .stats-item .label {{ color: #8d99b6; font-size: 14px; }}
        .stars {{
            color: #ffd700;
            font-size: 20px;
            letter-spacing: 2px;
        }}
        
        .rating-form {{
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }}
        .rating-form select, .rating-form input {{
            padding: 8px 14px;
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 12px;
            color: #fff;
            font-size: 14px;
        }}
        .rating-form select:focus, .rating-form input:focus {{
            outline: none;
            border-color: #00ff88;
        }}
        .rating-form input {{
            min-width: 150px;
        }}
        .rating-form .btn {{
            padding: 8px 20px;
            font-size: 13px;
        }}
        
        .hero {{
            text-align: center; padding: 40px 0 30px;
        }}
        .hero h1 {{
            font-size: 44px; font-weight: 900; color: #fff;
        }}
        .hero h1 span {{
            background: linear-gradient(135deg, #00ff88, #00ccff);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }}
        .hero p {{
            color: #8d99b6; font-size: 18px; max-width: 700px; margin: 15px auto 30px;
        }}
        
        /* ===== قسم الأدوات المحرمة ===== */
        .blackhat-section {{
            background: linear-gradient(135deg, rgba(255,0,0,0.08), rgba(200,0,0,0.05));
            border: 2px solid rgba(255,0,0,0.2);
            border-radius: 24px;
            padding: 35px 40px;
            margin: 30px 0 40px;
            backdrop-filter: blur(8px);
            position: relative;
        }}
        .blackhat-section::before {{
            content: '⚠️ تحذير: للأغراض التعليمية فقط';
            position: absolute;
            top: -12px;
            right: 30px;
            background: #cc0000;
            color: #fff;
            padding: 4px 20px;
            border-radius: 40px;
            font-size: 13px;
            font-weight: 700;
        }}
        .blackhat-header {{
            display: flex; align-items: center; gap: 15px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }}
        .blackhat-header h2 {{
            color: #ff3333; font-size: 28px; font-weight: 800;
        }}
        .blackhat-header i {{ color: #ff3333; font-size: 32px; }}
        .blackhat-header .badge-danger {{
            background: rgba(255,0,0,0.2);
            color: #ff3333; padding: 4px 16px; border-radius: 40px;
            font-size: 13px; font-weight: 700;
        }}
        
        .support-section {{
            background: linear-gradient(135deg, rgba(255,107,107,0.08), rgba(238,90,36,0.05));
            border: 1px solid rgba(255,107,107,0.15);
            border-radius: 24px;
            padding: 35px 40px;
            margin: 30px 0 40px;
            backdrop-filter: blur(8px);
        }}
        .support-header {{
            display: flex; align-items: center; gap: 15px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }}
        .support-header h2 {{
            color: #ff6b6b; font-size: 28px; font-weight: 800;
        }}
        .support-header i {{ color: #ff6b6b; font-size: 32px; }}
        .support-header .badge-support {{
            background: rgba(255,107,107,0.2);
            color: #ff6b6b; padding: 4px 16px; border-radius: 40px;
            font-size: 13px; font-weight: 700;
        }}
        .support-grid {{
            display: grid; grid-template-columns: 1fr 1fr;
            gap: 30px; margin-top: 15px;
        }}
        .support-card {{
            background: rgba(255,255,255,0.04);
            border-radius: 18px; padding: 25px;
            border: 1px solid rgba(255,255,255,0.06);
            transition: 0.3s;
        }}
        .support-card:hover {{
            border-color: rgba(255,107,107,0.2);
            transform: translateY(-4px);
        }}
        .support-card h3 {{
            color: #fff; font-size: 20px; margin-bottom: 12px;
        }}
        .support-card h3 i {{ color: #ff6b6b; margin-left: 10px; }}
        .support-card p {{
            color: #b0baca; font-size: 15px; line-height: 1.6; margin-bottom: 18px;
        }}
        .support-card .btn {{ width: 100%; justify-content: center; padding: 14px; }}
        .support-card .btn i {{ font-size: 18px; }}
        
        .support-form {{
            background: rgba(255,255,255,0.03);
            border-radius: 18px; padding: 25px;
            border: 1px solid rgba(255,255,255,0.06);
        }}
        .support-form input, .support-form textarea {{
            width: 100%; padding: 14px 16px;
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 12px; color: #fff; font-size: 15px;
            margin-bottom: 14px; font-family: inherit;
        }}
        .support-form input:focus, .support-form textarea:focus {{
            outline: none; border-color: #ff6b6b;
        }}
        .support-form textarea {{ min-height: 100px; resize: vertical; }}
        .support-form .btn {{ width: 100%; justify-content: center; padding: 14px; }}
        
        .category-title {{
            color: #fff; font-size: 26px; font-weight: 800;
            margin: 40px 0 20px;
            padding-right: 15px;
            border-right: 4px solid #00ff88;
        }}
        .category-title i {{ color: #00ff88; margin-left: 10px; }}
        .category-title.danger-title {{
            border-right-color: #ff3333;
        }}
        .category-title.danger-title i {{ color: #ff3333; }}
        
        .links-grid {{
            display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
            gap: 15px; margin: 15px 0 30px;
        }}
        .link-card {{
            background: rgba(255,255,255,0.04);
            border-radius: 16px; padding: 14px 18px;
            border: 1px solid rgba(255,255,255,0.06);
            transition: 0.3s; text-align: center;
            backdrop-filter: blur(4px);
        }}
        .link-card:hover {{
            transform: translateY(-4px);
            border-color: rgba(0,255,136,0.2);
            box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        }}
        .link-card a {{
            color: #e4e9f2; text-decoration: none; font-size: 14px; font-weight: 600;
            display: flex; flex-direction: column; align-items: center; gap: 6px;
        }}
        .link-card a i {{ font-size: 24px; color: #00ff88; }}
        .link-card a:hover {{ color: #00ff88; }}
        .link-card .badge {{
            font-size: 10px; background: rgba(0,255,136,0.15);
            color: #00ff88; padding: 2px 10px; border-radius: 20px;
            margin-top: 4px;
        }}
        .link-card .badge-danger {{
            font-size: 10px; background: rgba(255,0,0,0.2);
            color: #ff3333; padding: 2px 10px; border-radius: 20px;
            margin-top: 4px;
        }}
        .link-card.danger-card {{
            border-color: rgba(255,0,0,0.15);
        }}
        .link-card.danger-card:hover {{
            border-color: rgba(255,0,0,0.3);
        }}
        .link-card.danger-card a i {{ color: #ff3333; }}
        .link-card.danger-card a:hover {{ color: #ff3333; }}
        
        .footer {{
            text-align: center; padding: 30px 0 20px;
            border-top: 1px solid rgba(255,255,255,0.05);
            color: #6b7a98; margin-top: 20px;
        }}
        .footer a {{ color: #8d99b6; text-decoration: none; margin: 0 12px; }}
        .footer a:hover {{ color: #00ff88; }}
        
        @media (max-width: 768px) {{
            .header {{ flex-direction: column; align-items: stretch; gap: 10px; }}
            .nav-links {{ justify-content: center; gap: 12px; font-size: 14px; }}
            .hero h1 {{ font-size: 28px; }}
            .support-grid {{ grid-template-columns: 1fr; }}
            .support-section {{ padding: 20px; }}
            .blackhat-section {{ padding: 20px; }}
            .links-grid {{ grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); }}
            .stats-section {{ flex-direction: column; align-items: stretch; text-align: center; }}
            .rating-form {{ justify-content: center; }}
        }}
    </style>
</head>
<body>
<div class="container">
    <header class="header">
        <div class="logo"><i class="fas fa-shield-halved"></i> عبود</div>
        <ul class="nav-links">
            <li><a href="/">الرئيسية</a></li>
            <li><a href="#courses">الدورات</a></li>
            <li><a href="#tools">أدوات</a></li>
            <li><a href="#blackhat">أدوات محرمة</a></li>
            <li><a href="#support">الدعم</a></li>
            <li><a href="#resources">مصادر</a></li>
        </ul>
        <div style="display:flex; gap:10px; flex-wrap:wrap;">
            <a href="#support" class="btn btn-support"><i class="fas fa-headset"></i> الدعم الفني</a>
            <a href="#blackhat" class="btn btn-danger"><i class="fas fa-skull"></i> أدوات محرمة</a>
        </div>
    </header>

    <!-- ===== قسم الإحصائيات والتقييم ===== -->
    <div class="stats-section">
        <div class="stats-item">
            <i class="fas fa-users"></i>
            <div>
                <span class="number">{stats["total_visitors"]}</span>
                <span class="label">زائر</span>
            </div>
        </div>
        <div class="stats-item">
            <i class="fas fa-star"></i>
            <div>
                <span class="number">{avg_rating:.1f}</span>
                <span class="label">/ 5</span>
                <div class="stars">{'⭐' * int(round(avg_rating))}{'☆' * (5 - int(round(avg_rating)))}</div>
            </div>
        </div>
        <form action="/submit-rating" method="POST" class="rating-form">
            <select name="rating" required>
                <option value="">تقييمك</option>
                <option value="1">⭐ 1</option>
                <option value="2">⭐⭐ 2</option>
                <option value="3">⭐⭐⭐ 3</option>
                <option value="4">⭐⭐⭐⭐ 4</option>
                <option value="5">⭐⭐⭐⭐⭐ 5</option>
            </select>
            <input type="text" name="comment" placeholder="تعليقك (اختياري)">
            <button type="submit" class="btn btn-primary"><i class="fas fa-paper-plane"></i> تقييم</button>
        </form>
    </div>

    <section class="hero">
        <h1>تعلم <span>الأمن السيبراني</span> والاختراقات</h1>
        <p>أكثر من 150 مصدر تعليمي حقيقي لتعلم كل شيء عن الأمن السيبراني، الاختراقات الأخلاقية، وأدوات القرصنة</p>
        <a href="#courses" class="btn btn-primary" style="font-size:16px; padding:12px 35px;">
            <i class="fas fa-arrow-down"></i> استكشف المصادر
        </a>
    </section>

    <!-- ===== قسم الأدوات المحرمة ===== -->
    <section class="blackhat-section" id="blackhat">
        <div class="blackhat-header">
            <i class="fas fa-skull-crossbones"></i>
            <h2>أدوات اختراق محرمة وخطيرة</h2>
            <span class="badge-danger">للأغراض التعليمية فقط</span>
        </div>
        <p style="color:#ff6666; font-size:15px; margin-bottom:15px;">
            <i class="fas fa-exclamation-triangle"></i> 
            هذه الأدوات تستخدم في الاختراقات المتقدمة. استخدامها بدون إذن يعتبر جريمة. التعليم فقط!
        </p>
        
        <div class="links-grid">
            <div class="link-card danger-card"><a href="https://github.com/gentilkiwi/mimikatz" target="_blank"><i class="fas fa-key"></i> Mimikatz <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/beefproject/beef" target="_blank"><i class="fas fa-bug"></i> BeEF <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/sqlmapproject/sqlmap" target="_blank"><i class="fas fa-database"></i> SQLMap <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/rapid7/metasploit-framework" target="_blank"><i class="fas fa-bolt"></i> Metasploit <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/trustedsec/social-engineer-toolkit" target="_blank"><i class="fas fa-users"></i> SEToolkit <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/offensive-security/exploitdb" target="_blank"><i class="fas fa-database"></i> Exploit-DB <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/danielmiessler/SecLists" target="_blank"><i class="fas fa-list"></i> SecLists <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/vanhauser-thc/thc-hydra" target="_blank"><i class="fas fa-key"></i> THC-Hydra <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/openwall/john" target="_blank"><i class="fas fa-lock"></i> John the Ripper <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/aircrack-ng/aircrack-ng" target="_blank"><i class="fas fa-wifi"></i> Aircrack-ng <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/ReFirmLabs/binwalk" target="_blank"><i class="fas fa-microchip"></i> Binwalk <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/volatilityfoundation/volatility" target="_blank"><i class="fas fa-memory"></i> Volatility <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/radareorg/radare2" target="_blank"><i class="fas fa-microchip"></i> Radare2 <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/NationalSecurityAgency/ghidra" target="_blank"><i class="fas fa-cogs"></i> Ghidra <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/xorrior/Random-C2" target="_blank"><i class="fas fa-robot"></i> Random C2 <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/EmpireProject/Empire" target="_blank"><i class="fas fa-crown"></i> Empire <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/byt3bl33d3r/CrackMapExec" target="_blank"><i class="fas fa-network-wired"></i> CrackMapExec <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/BloodHoundAD/BloodHound" target="_blank"><i class="fas fa-dog"></i> BloodHound <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/kerberoasting/kerberoast" target="_blank"><i class="fas fa-user-secret"></i> Kerberoast <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/gentilkiwi/kekeo" target="_blank"><i class="fas fa-key"></i> Kekeo <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/Ne0nd0g/merlin" target="_blank"><i class="fas fa-magic"></i> Merlin <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/mwrlabs/Sharp-Suite" target="_blank"><i class="fas fa-code"></i> Sharp-Suite <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/GhostPack/Seatbelt" target="_blank"><i class="fas fa-seatbelt"></i> Seatbelt <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/GhostPack/SharpUp" target="_blank"><i class="fas fa-arrow-up"></i> SharpUp <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/cobbr/Covenant" target="_blank"><i class="fas fa-handshake"></i> Covenant <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/PowerShellMafia/PowerSploit" target="_blank"><i class="fas fa-bolt"></i> PowerSploit <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/SamRothCA/evil-winrm" target="_blank"><i class="fas fa-terminal"></i> Evil-WinRM <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/rasta-mouse/Sherlock" target="_blank"><i class="fas fa-search"></i> Sherlock <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/matterpreter/OffensiveCSharp" target="_blank"><i class="fas fa-csharp"></i> OffensiveCSharp <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/Arno0x/DNSExfiltrator" target="_blank"><i class="fas fa-dns"></i> DNSExfiltrator <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/zer0yu/RedTeam" target="_blank"><i class="fas fa-shield"></i> RedTeam Tools <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/CiscoCXSecurity/linux_enum" target="_blank"><i class="fab fa-linux"></i> Linux Enum <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/rebootuser/LinEnum" target="_blank"><i class="fab fa-linux"></i> LinEnum <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/AlessandroZ/LaZagne" target="_blank"><i class="fas fa-key"></i> LaZagne <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/behindthefirewalls/Mimikatz" target="_blank"><i class="fas fa-key"></i> Mimikatz Extras <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/Mr-Un1k0d3r/ADHunt" target="_blank"><i class="fas fa-search"></i> ADHunt <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/Mr-Un1k0d3r/RedTeam-Cookbook" target="_blank"><i class="fas fa-book"></i> RedTeam Cookbook <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/TechNowTools/Shellcode" target="_blank"><i class="fas fa-code"></i> Shellcode <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/ParrotSec/parrot-tools" target="_blank"><i class="fas fa-parrot"></i> Parrot Tools <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/0x4D31/fatt" target="_blank"><i class="fas fa-fingerprint"></i> FATT <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/SpiderLabs/Responder" target="_blank"><i class="fas fa-respond"></i> Responder <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/infosec-au/altdns" target="_blank"><i class="fas fa-dns"></i> Altdns <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/aboul3la/Sublist3r" target="_blank"><i class="fas fa-search"></i> Sublist3r <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/OWASP/Amass" target="_blank"><i class="fas fa-search"></i> Amass <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/blechschmidt/massdns" target="_blank"><i class="fas fa-dns"></i> MassDNS <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/projectdiscovery/nuclei" target="_blank"><i class="fas fa-biohazard"></i> Nuclei <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/projectdiscovery/httpx" target="_blank"><i class="fas fa-http"></i> HTTPX <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/projectdiscovery/subfinder" target="_blank"><i class="fas fa-search"></i> Subfinder <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/ffuf/ffuf" target="_blank"><i class="fas fa-sitemap"></i> FFUF <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/OJ/gobuster" target="_blank"><i class="fas fa-sitemap"></i> Gobuster <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/digininja/DNSChef" target="_blank"><i class="fas fa-chef"></i> DNSChef <span class="badge-danger">خطير</span></a></div>
            <div class="link-card danger-card"><a href="https://github.com/DavidBuchanan314/dns-dumpster" target="_blank"><i class="fas fa-dumpster"></i> DNS Dumpster <span class="badge-danger">خطير</span></a></div>
        </div>
        
        <div style="margin-top:20px; padding:15px; background:rgba(255,0,0,0.05); border-radius:12px; border:1px solid rgba(255,0,0,0.1);">
            <p style="color:#ff6666; font-size:14px; text-align:center;">
                <i class="fas fa-gavel"></i> 
                <strong>تنبيه قانوني:</strong> استخدام هذه الأدوات بدون إذن صريح يعتبر جريمة يعاقب عليها القانون. 
                هذه الروابط للأغراض التعليمية والبحثية فقط.
            </p>
        </div>
    </section>

    <!-- ===== قسم الدعم ===== -->
    <section class="support-section" id="support">
        <div class="support-header">
            <i class="fas fa-headset"></i>
            <h2>مركز الدعم الفني</h2>
            <span class="badge-support">تحت إشراف المبرمج عبود</span>
        </div>
        <p style="color:#b0baca; font-size:16px; margin-bottom:10px;">
            <i class="fas fa-info-circle" style="color:#ff6b6b;"></i> 
            فريق الدعم متاح 24/7 للإجابة على استفساراتك وحل مشاكلك التقنية
        </p>
        
        <div class="support-grid">
            <div class="support-card">
                <h3><i class="fab fa-telegram"></i> تواصل عبر تيليجرام</h3>
                <p>احصل على دعم فوري عبر تيليجرام من فريق الدعم المختص. أرسل رسالتك وسنرد عليك في أقرب وقت.</p>
                <a href="https://t.me/SSSTlF" target="_blank" class="btn btn-telegram">
                    <i class="fab fa-telegram"></i> @SSSTlF - تواصل الآن
                </a>
            </div>
            
            <div class="support-form">
                <h3 style="color:#fff; font-size:18px; margin-bottom:12px;">
                    <i class="fas fa-envelope" style="color:#ff6b6b;"></i> أرسل رسالتك
                </h3>
                <form action="https://formsubmit.co/your-email@example.com" method="POST">
                    <input type="text" name="name" placeholder="الاسم الكامل" required>
                    <input type="email" name="email" placeholder="البريد الإلكتروني" required>
                    <input type="text" name="subject" placeholder="موضوع الرسالة" required>
                    <textarea name="message" placeholder="اكتب رسالتك هنا..." required></textarea>
                    <input type="hidden" name="_captcha" value="false">
                    <input type="hidden" name="_next" value="/">
                    <button type="submit" class="btn btn-support">
                        <i class="fas fa-paper-plane"></i> إرسال الرسالة
                    </button>
                </form>
                <p style="color:#6b7a98; font-size:12px; margin-top:10px; text-align:center;">
                    <i class="fas fa-lock"></i> رسالتك مشفرة وآمنة
                </p>
            </div>
        </div>
        
        <div style="display:flex; flex-wrap:wrap; gap:20px; margin-top:25px; padding-top:20px; border-top:1px solid rgba(255,255,255,0.06);">
            <div style="display:flex; align-items:center; gap:10px; color:#b0baca;">
                <i class="fas fa-user-cog" style="color:#ff6b6b;"></i>
                <span>المشرف: <strong style="color:#fff;">المبرمج عبود</strong></span>
            </div>
            <div style="display:flex; align-items:center; gap:10px; color:#b0baca;">
                <i class="fas fa-clock" style="color:#ff6b6b;"></i>
                <span>ساعات الدعم: 24/7</span>
            </div>
            <div style="display:flex; align-items:center; gap:10px; color:#b0baca;">
                <i class="fas fa-shield-alt" style="color:#ff6b6b;"></i>
                <span>جميع المحادثات خاصة ومشفرة</span>
            </div>
        </div>
    </section>

    <!-- ===== بقية الأقسام (مختصرة للاختصار) ===== -->
    <h2 class="category-title" id="courses"><i class="fas fa-graduation-cap"></i> منصات تعليمية - دورات مجانية</h2>
    <div class="links-grid">
        <div class="link-card"><a href="https://www.coursera.org/courses?query=cybersecurity" target="_blank"><i class="fas fa-school"></i> Coursera <span class="badge">مجاني</span></a></div>
        <div class="link-card"><a href="https://www.edx.org/learn/cybersecurity" target="_blank"><i class="fas fa-university"></i> edX <span class="badge">مجاني</span></a></div>
        <div class="link-card"><a href="https://www.udemy.com/topic/cyber-security/" target="_blank"><i class="fas fa-video"></i> Udemy <span class="badge">مدفوع</span></a></div>
        <div class="link-card"><a href="https://www.cybrary.it/" target="_blank"><i class="fas fa-users"></i> Cybrary <span class="badge">مجاني</span></a></div>
        <div class="link-card"><a href="https://www.khanacademy.org/computing/computer-science" target="_blank"><i class="fas fa-lightbulb"></i> Khan Academy <span class="badge">مجاني</span></a></div>
        <div class="link-card"><a href="https://www.pluralsight.com/browse/security" target="_blank"><i class="fas fa-chart-line"></i> Pluralsight <span class="badge">مدفوع</span></a></div>
        <div class="link-card"><a href="https://www.linkedin.com/learning/topics/cybersecurity" target="_blank"><i class="fab fa-linkedin"></i> LinkedIn Learning <span class="badge">مدفوع</span></a></div>
        <div class="link-card"><a href="https://www.sans.org/cyber-security-courses/" target="_blank"><i class="fas fa-shield"></i> SANS <span class="badge">مدفوع</span></a></div>
        <div class="link-card"><a href="https://www.offensive-security.com/courses/" target="_blank"><i class="fas fa-skull"></i> Offensive Security <span class="badge">مدفوع</span></a></div>
        <div class="link-card"><a href="https://www.eccouncil.org/training-courses/" target="_blank"><i class="fas fa-certificate"></i> EC-Council <span class="badge">مدفوع</span></a></div>
    </div>

    <!-- ===== قسم 2: أدوات الاختراق ===== -->
    <h2 class="category-title" id="tools"><i class="fas fa-tools"></i> أدوات الاختراق والتحليل</h2>
    <div class="links-grid">
        <div class="link-card"><a href="https://www.kali.org/tools/" target="_blank"><i class="fas fa-skull-crossbones"></i> Kali Tools</a></div>
        <div class="link-card"><a href="https://www.metasploit.com/" target="_blank"><i class="fas fa-bolt"></i> Metasploit</a></div>
        <div class="link-card"><a href="https://www.wireshark.org/" target="_blank"><i class="fas fa-wifi"></i> Wireshark</a></div>
        <div class="link-card"><a href="https://nmap.org/" target="_blank"><i class="fas fa-network-wired"></i> Nmap</a></div>
        <div class="link-card"><a href="https://www.burpsuite.com/" target="_blank"><i class="fas fa-bug"></i> Burp Suite</a></div>
        <div class="link-card"><a href="https://www.aircrack-ng.org/" target="_blank"><i class="fas fa-wifi"></i> Aircrack-ng</a></div>
        <div class="link-card"><a href="https://www.sqlmap.org/" target="_blank"><i class="fas fa-database"></i> SQLmap</a></div>
        <div class="link-card"><a href="https://www.ettercap-project.org/" target="_blank"><i class="fas fa-arrows-alt-h"></i> Ettercap</a></div>
        <div class="link-card"><a href="https://www.hydra-project.org/" target="_blank"><i class="fas fa-key"></i> THC Hydra</a></div>
        <div class="link-card"><a href="https://www.john-the-ripper.cc/" target="_blank"><i class="fas fa-lock"></i> John the Ripper</a></div>
        <div class="link-card"><a href="https://www.nessus.org/" target="_blank"><i class="fas fa-search"></i> Nessus</a></div>
        <div class="link-card"><a href="https://www.openvas.org/" target="_blank"><i class="fas fa-shield-virus"></i> OpenVAS</a></div>
        <div class="link-card"><a href="https://www.radare.org/" target="_blank"><i class="fas fa-microchip"></i> Radare2</a></div>
        <div class="link-card"><a href="https://www.ghidra-sre.org/" target="_blank"><i class="fas fa-cogs"></i> Ghidra</a></div>
        <div class="link-card"><a href="https://www.immunitysec.com/products-canvas.html" target="_blank"><i class="fas fa-paint-brush"></i> Canvas</a></div>
        <div class="link-card"><a href="https://www.coresecurity.com/core-impact" target="_blank"><i class="fas fa-crosshairs"></i> Core Impact</a></div>
    </div>

    <!-- ===== قسم 3: قنوات يوتيوب ===== -->
    <h2 class="category-title"><i class="fab fa-youtube"></i> قنوات يوتيوب - اختراقات وأمن سيبراني</h2>
    <div class="links-grid">
        <div class="link-card"><a href="https://www.youtube.com/@NetworkChuck" target="_blank"><i class="fab fa-youtube"></i> NetworkChuck</a></div>
        <div class="link-card"><a href="https://www.youtube.com/@DavidBombal" target="_blank"><i class="fab fa-youtube"></i> David Bombal</a></div>
        <div class="link-card"><a href="https://www.youtube.com/@TheCyberMentor" target="_blank"><i class="fab fa-youtube"></i> The Cyber Mentor</a></div>
        <div class="link-card"><a href="https://www.youtube.com/@LiveOverflow" target="_blank"><i class="fab fa-youtube"></i> LiveOverflow</a></div>
        <div class="link-card"><a href="https://www.youtube.com/@IppSec" target="_blank"><i class="fab fa-youtube"></i> IppSec</a></div>
        <div class="link-card"><a href="https://www.youtube.com/@JohnHammond" target="_blank"><i class="fab fa-youtube"></i> John Hammond</a></div>
        <div class="link-card"><a href="https://www.youtube.com/@HackerSploit" target="_blank"><i class="fab fa-youtube"></i> HackerSploit</a></div>
        <div class="link-card"><a href="https://www.youtube.com/@SecurityTube" target="_blank"><i class="fab fa-youtube"></i> SecurityTube</a></div>
        <div class="link-card"><a href="https://www.youtube.com/@SANSInstitute" target="_blank"><i class="fab fa-youtube"></i> SANS Institute</a></div>
        <div class="link-card"><a href="https://www.youtube.com/@BlackHat" target="_blank"><i class="fab fa-youtube"></i> Black Hat</a></div>
        <div class="link-card"><a href="https://www.youtube.com/@DEFCONConference" target="_blank"><i class="fab fa-youtube"></i> DEFCON</a></div>
        <div class="link-card"><a href="https://www.youtube.com/@HackerOne" target="_blank"><i class="fab fa-youtube"></i> HackerOne</a></div>
        <div class="link-card"><a href="https://www.youtube.com/@Bugcrowd" target="_blank"><i class="fab fa-youtube"></i> Bugcrowd</a></div>
        <div class="link-card"><a href="https://www.youtube.com/@SecurityNow" target="_blank"><i class="fab fa-youtube"></i> Security Now</a></div>
        <div class="link-card"><a href="https://www.youtube.com/@Computerphile" target="_blank"><i class="fab fa-youtube"></i> Computerphile</a></div>
    </div>

    <!-- ===== قسم 4: كتب ومكتبات ===== -->
    <h2 class="category-title" id="resources"><i class="fas fa-book"></i> كتب ومراجع مجانية</h2>
    <div class="links-grid">
        <div class="link-card"><a href="https://www.oreilly.com/online-learning/" target="_blank"><i class="fas fa-book-open"></i> O'Reilly</a></div>
        <div class="link-card"><a href="https://www.packtpub.com/free-ebooks" target="_blank"><i class="fas fa-book"></i> Packt Free eBooks</a></div>
        <div class="link-card"><a href="https://www.nostarch.com/catalog/security" target="_blank"><i class="fas fa-archive"></i> No Starch Press</a></div>
        <div class="link-card"><a href="https://www.sans.org/reading-room/" target="_blank"><i class="fas fa-file-alt"></i> SANS Reading Room</a></div>
        <div class="link-card"><a href="https://www.cs.utexas.edu/~byoung/cs361/reading.html" target="_blank"><i class="fas fa-university"></i> UT Austin Security</a></div>
        <div class="link-card"><a href="https://www.springer.com/gp/computer-science/security" target="_blank"><i class="fas fa-leaf"></i> Springer Security</a></div>
        <div class="link-card"><a href="https://www.gnu.org/software/coreutils/manual/" target="_blank"><i class="fas fa-terminal"></i> GNU Coreutils</a></div>
        <div class="link-card"><a href="https://www.kernel.org/doc/html/latest/security/index.html" target="_blank"><i class="fas fa-linux"></i> Linux Security Docs</a></div>
        <div class="link-card"><a href="https://www.owasp.org/index.php/Main_Page" target="_blank"><i class="fas fa-globe"></i> OWASP</a></div>
        <div class="link-card"><a href="https://www.cisa.gov/cybersecurity" target="_blank"><i class="fas fa-government"></i> CISA Cybersecurity</a></div>
        <div class="link-card"><a href="https://www.nist.gov/cyberframework" target="_blank"><i class="fas fa-balance-scale"></i> NIST Framework</a></div>
        <div class="link-card"><a href="https://www.enisa.europa.eu/topics/cybersecurity" target="_blank"><i class="fas fa-europe"></i> ENISA</a></div>
    </div>

    <!-- ===== قسم 5: منتديات ومجتمعات ===== -->
    <h2 class="category-title"><i class="fas fa-users"></i> منتديات ومجتمعات اختراق</h2>
    <div class="links-grid">
        <div class="link-card"><a href="https://www.reddit.com/r/cybersecurity/" target="_blank"><i class="fab fa-reddit"></i> r/cybersecurity</a></div>
        <div class="link-card"><a href="https://www.reddit.com/r/HowToHack/" target="_blank"><i class="fab fa-reddit"></i> r/HowToHack</a></div>
        <div class="link-card"><a href="https://www.reddit.com/r/netsec/" target="_blank"><i class="fab fa-reddit"></i> r/netsec</a></div>
        <div class="link-card"><a href="https://www.reddit.com/r/blackhat/" target="_blank"><i class="fab fa-reddit"></i> r/blackhat</a></div>
        <div class="link-card"><a href="https://www.reddit.com/r/hacking/" target="_blank"><i class="fab fa-reddit"></i> r/hacking</a></div>
        <div class="link-card"><a href="https://www.hackthebox.com/" target="_blank"><i class="fas fa-box"></i> HackTheBox</a></div>
        <div class="link-card"><a href="https://www.tryhackme.com/" target="_blank"><i class="fas fa-gamepad"></i> TryHackMe</a></div>
        <div class="link-card"><a href="https://www.overthewire.org/wargames/" target="_blank"><i class="fas fa-gamepad"></i> OverTheWire</a></div>
        <div class="link-card"><a href="https://www.root-me.org/" target="_blank"><i class="fas fa-root"></i> Root-Me</a></div>
        <div class="link-card"><a href="https://www.ctftime.org/" target="_blank"><i class="fas fa-flag"></i> CTFTime</a></div>
        <div class="link-card"><a href="https://www.vulnhub.com/" target="_blank"><i class="fas fa-download"></i> VulnHub</a></div>
        <div class="link-card"><a href="https://www.pwnablekr.com/" target="_blank"><i class="fas fa-terminal"></i> PwnableKr</a></div>
        <div class="link-card"><a href="https://www.hackerrank.com/domains/security" target="_blank"><i class="fas fa-code"></i> HackerRank Security</a></div>
        <div class="link-card"><a href="https://www.codewars.com/" target="_blank"><i class="fas fa-code"></i> Codewars</a></div>
        <div class="link-card"><a href="https://www.leetcode.com/" target="_blank"><i class="fas fa-code"></i> LeetCode</a></div>
    </div>

    <!-- ===== قسم 6: شهادات مهنية ===== -->
    <h2 class="category-title"><i class="fas fa-certificate"></i> شهادات احترافية في الأمن السيبراني</h2>
    <div class="links-grid">
        <div class="link-card"><a href="https://www.eccouncil.org/ceh/" target="_blank"><i class="fas fa-certificate"></i> CEH</a></div>
        <div class="link-card"><a href="https://www.isc2.org/certifications/cissp" target="_blank"><i class="fas fa-certificate"></i> CISSP</a></div>
        <div class="link-card"><a href="https://www.comptia.org/certifications/security" target="_blank"><i class="fas fa-certificate"></i> CompTIA Security+</a></div>
        <div class="link-card"><a href="https://www.offensive-security.com/pwk-oscp/" target="_blank"><i class="fas fa-certificate"></i> OSCP</a></div>
        <div class="link-card"><a href="https://www.eccouncil.org/ecsa/" target="_blank"><i class="fas fa-certificate"></i> ECSA</a></div>
        <div class="link-card"><a href="https://www.isc2.org/certifications/ccsp" target="_blank"><i class="fas fa-certificate"></i> CCSP</a></div>
        <div class="link-card"><a href="https://www.giac.org/certifications/" target="_blank"><i class="fas fa-certificate"></i> GIAC</a></div>
        <div class="link-card"><a href="https://www.comptia.org/certifications/cybersecurity-analyst" target="_blank"><i class="fas fa-certificate"></i> CySA+</a></div>
        <div class="link-card"><a href="https://www.comptia.org/certifications/pen-test" target="_blank"><i class="fas fa-certificate"></i> PenTest+</a></div>
        <div class="link-card"><a href="https://www.isaca.org/credentials/cism" target="_blank"><i class="fas fa-certificate"></i> CISM</a></div>
        <div class="link-card"><a href="https://www.isaca.org/credentials/cisa" target="_blank"><i class="fas fa-certificate"></i> CISA</a></div>
        <div class="link-card"><a href="https://www.eccouncil.org/chfi/" target="_blank"><i class="fas fa-certificate"></i> CHFI</a></div>
    </div>

    <!-- ===== قسم 7: هجمات وحماية ===== -->
    <h2 class="category-title"><i class="fas fa-bug"></i> تقنيات الهجوم والدفاع</h2>
    <div class="links-grid">
        <div class="link-card"><a href="https://www.owasp.org/index.php/OWASP_Top_Ten_Cheat_Sheet" target="_blank"><i class="fas fa-list"></i> OWASP Top 10</a></div>
        <div class="link-card"><a href="https://portswigger.net/web-security" target="_blank"><i class="fas fa-globe"></i> Web Security Academy</a></div>
        <div class="link-card"><a href="https://www.exploit-db.com/" target="_blank"><i class="fas fa-database"></i> Exploit-DB</a></div>
        <div class="link-card"><a href="https://www.securityfocus.com/vulnerabilities" target="_blank"><i class="fas fa-bullseye"></i> SecurityFocus</a></div>
        <div class="link-card"><a href="https://www.cvedetails.com/" target="_blank"><i class="fas fa-exclamation-triangle"></i> CVE Details</a></div>
        <div class="link-card"><a href="https://nvd.nist.gov/" target="_blank"><i class="fas fa-database"></i> NVD - NIST</a></div>
        <div class="link-card"><a href="https://www.mitre.org/cybersecurity" target="_blank"><i class="fas fa-shield"></i> MITRE</a></div>
        <div class="link-card"><a href="https://attack.mitre.org/" target="_blank"><i class="fas fa-crosshairs"></i> MITRE ATT&CK</a></div>
        <div class="link-card"><a href="https://www.cyber.gov.au/" target="_blank"><i class="fas fa-globe"></i> ASD Cyber</a></div>
        <div class="link-card"><a href="https://www.ncsc.gov.uk/" target="_blank"><i class="fas fa-globe"></i> NCSC UK</a></div>
        <div class="link-card"><a href="https://www.us-cert.gov/" target="_blank"><i class="fas fa-globe"></i> US-CERT</a></div>
        <div class="link-card"><a href="https://www.cert.org/" target="_blank"><i class="fas fa-certificate"></i> CERT</a></div>
    </div>

    <!-- ===== قسم 8: برمجيات خبيثة ===== -->
    <h2 class="category-title"><i class="fas fa-virus"></i> تحليل البرمجيات الخبيثة</h2>
    <div class="links-grid">
        <div class="link-card"><a href="https://www.virustotal.com/" target="_blank"><i class="fas fa-shield-virus"></i> VirusTotal</a></div>
        <div class="link-card"><a href="https://www.hybrid-analysis.com/" target="_blank"><i class="fas fa-microscope"></i> Hybrid Analysis</a></div>
        <div class="link-card"><a href="https://www.joesandbox.com/" target="_blank"><i class="fas fa-box"></i> Joe Sandbox</a></div>
        <div class="link-card"><a href="https://www.any.run/" target="_blank"><i class="fas fa-play"></i> ANY.RUN</a></div>
        <div class="link-card"><a href="https://www.malwarebytes.com/" target="_blank"><i class="fas fa-shield"></i> Malwarebytes</a></div>
        <div class="link-card"><a href="https://www.emsisoft.com/" target="_blank"><i class="fas fa-shield"></i> Emsisoft</a></div>
        <div class="link-card"><a href="https://www.kaspersky.com/" target="_blank"><i class="fas fa-shield"></i> Kaspersky</a></div>
        <div class="link-card"><a href="https://www.sophos.com/" target="_blank"><i class="fas fa-shield"></i> Sophos</a></div>
        <div class="link-card"><a href="https://www.crowdstrike.com/" target="_blank"><i class="fas fa-shield"></i> CrowdStrike</a></div>
        <div class="link-card"><a href="https://www.sentinelone.com/" target="_blank"><i class="fas fa-shield"></i> SentinelOne</a></div>
        <div class="link-card"><a href="https://www.fireeye.com/" target="_blank"><i class="fas fa-fire"></i> FireEye</a></div>
        <div class="link-card"><a href="https://www.mandiant.com/" target="_blank"><i class="fas fa-eye"></i> Mandiant</a></div>
    </div>

    <!-- ===== قسم 9: بلوكشين ===== -->
    <h2 class="category-title"><i class="fas fa-link"></i> أمن البلوكشين والعملات الرقمية</h2>
    <div class="links-grid">
        <div class="link-card"><a href="https://ethereum.org/en/security/" target="_blank"><i class="fab fa-ethereum"></i> Ethereum Security</a></div>
        <div class="link-card"><a href="https://bitcoin.org/en/security" target="_blank"><i class="fab fa-bitcoin"></i> Bitcoin Security</a></div>
        <div class="link-card"><a href="https://www.blockchain.com/security" target="_blank"><i class="fas fa-link"></i> Blockchain Security</a></div>
        <div class="link-card"><a href="https://www.cryptocompare.com/" target="_blank"><i class="fas fa-chart-line"></i> CryptoCompare</a></div>
        <div class="link-card"><a href="https://www.coingecko.com/" target="_blank"><i class="fas fa-chart-line"></i> CoinGecko</a></div>
        <div class="link-card"><a href="https://www.coinmarketcap.com/" target="_blank"><i class="fas fa-chart-line"></i> CoinMarketCap</a></div>
        <div class="link-card"><a href="https://www.ledger.com/academy/security" target="_blank"><i class="fas fa-hard-hat"></i> Ledger Academy</a></div>
        <div class="link-card"><a href="https://www.trezor.io/learn/security" target="_blank"><i class="fas fa-hard-hat"></i> Trezor Security</a></div>
        <div class="link-card"><a href="https://www.coinbase.com/learn" target="_blank"><i class="fab fa-coinbase"></i> Coinbase Learn</a></div>
        <div class="link-card"><a href="https://www.binance.com/en/learn" target="_blank"><i class="fas fa-graduation-cap"></i> Binance Learn</a></div>
        <div class="link-card"><a href="https://www.kraken.com/learn" target="_blank"><i class="fas fa-graduation-cap"></i> Kraken Learn</a></div>
        <div class="link-card"><a href="https://www.gemini.com/learn" target="_blank"><i class="fas fa-graduation-cap"></i> Gemini Learn</a></div>
    </div>

    <!-- ===== قسم 10: إنترنت الأشياء ===== -->
    <h2 class="category-title"><i class="fas fa-microchip"></i> أمن إنترنت الأشياء (IoT)</h2>
    <div class="links-grid">
        <div class="link-card"><a href="https://www.iotsecurityfoundation.org/" target="_blank"><i class="fas fa-shield"></i> IoT Security Foundation</a></div>
        <div class="link-card"><a href="https://www.iotevolutionworld.com/security/" target="_blank"><i class="fas fa-globe"></i> IoT Evolution Security</a></div>
        <div class="link-card"><a href="https://www.iotforall.com/security" target="_blank"><i class="fas fa-globe"></i> IoT For All Security</a></div>
        <div class="link-card"><a href="https://www.armis.com/" target="_blank"><i class="fas fa-shield"></i> Armis</a></div>
        <div class="link-card"><a href="https://www.paloaltonetworks.com/cyberpedia/iot-security" target="_blank"><i class="fas fa-shield"></i> Palo Alto IoT</a></div>
        <div class="link-card"><a href="https://www.cisco.com/c/en/us/solutions/internet-of-things/security.html" target="_blank"><i class="fas fa-shield"></i> Cisco IoT Security</a></div>
        <div class="link-card"><a href="https://www.symantec.com/iot-security" target="_blank"><i class="fas fa-shield"></i> Symantec IoT</a></div>
        <div class="link-card"><a href="https://www.mcafee.com/enterprise/en-us/security-awareness/iot.html" target="_blank"><i class="fas fa-shield"></i> McAfee IoT</a></div>
        <div class="link-card"><a href="https://www.trendmicro.com/vinfo/us/security/news/internet-of-things" target="_blank"><i class="fas fa-shield"></i> TrendMicro IoT</a></div>
        <div class="link-card"><a href="https://www.fortinet.com/resources/cyberglossary/iot-security" target="_blank"><i class="fas fa-shield"></i> Fortinet IoT</a></div>
    </div>

    <!-- ===== قسم 11: أمن السحابة ===== -->
    <h2 class="category-title"><i class="fas fa-cloud"></i> أمن الحوسبة السحابية</h2>
    <div class="links-grid">
        <div class="link-card"><a href="https://aws.amazon.com/security/" target="_blank"><i class="fab fa-aws"></i> AWS Security</a></div>
        <div class="link-card"><a href="https://azure.microsoft.com/en-us/security/" target="_blank"><i class="fab fa-microsoft"></i> Azure Security</a></div>
        <div class="link-card"><a href="https://cloud.google.com/security/" target="_blank"><i class="fab fa-google"></i> GCP Security</a></div>
        <div class="link-card"><a href="https://www.ibm.com/cloud/security" target="_blank"><i class="fab fa-ibm"></i> IBM Cloud Security</a></div>
        <div class="link-card"><a href="https://www.oracle.com/security/" target="_blank"><i class="fab fa-oracle"></i> Oracle Cloud Security</a></div>
        <div class="link-card"><a href="https://www.digitalocean.com/security" target="_blank"><i class="fas fa-cloud"></i> DigitalOcean Security</a></div>
        <div class="link-card"><a href="https://www.linode.com/security/" target="_blank"><i class="fas fa-cloud"></i> Linode Security</a></div>
        <div class="link-card"><a href="https://www.vultr.com/security/" target="_blank"><i class="fas fa-cloud"></i> Vultr Security</a></div>
        <div class="link-card"><a href="https://www.heroku.com/security" target="_blank"><i class="fas fa-cloud"></i> Heroku Security</a></div>
        <div class="link-card"><a href="https://www.netlify.com/security/" target="_blank"><i class="fas fa-cloud"></i> Netlify Security</a></div>
    </div>

    <footer class="footer">
        <div>
            <a href="#"><i class="fab fa-facebook-f"></i></a>
            <a href="#"><i class="fab fa-twitter"></i></a>
            <a href="#"><i class="fab fa-instagram"></i></a>
            <a href="#"><i class="fab fa-youtube"></i></a>
            <a href="#"><i class="fab fa-github"></i></a>
            <a href="https://t.me/SSSTlF" target="_blank"><i class="fab fa-telegram"></i></a>
        </div>
        <p style="margin-top:15px;">&copy; 2026 عبود | تعليم الأمن السيبراني والاختراقات الأخلاقية</p>
        <p style="color:#555; font-size:12px;">
            جميع الروابط تعليمية وتوعوية - للأغراض التعليمية فقط<br>
            للدعم والتواصل: <a href="https://t.me/SSSTlF" target="_blank" style="color:#ff6b6b; text-decoration:none;">@SSSTlF</a>
        </p>
    </footer>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/js/all.min.js"></script>
</body>
</html>"""

    def log_message(self, format, *args):
        return

# ===== تشغيل الخادم =====
def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), AboodHandler)
    print(f"[✓] موقع عبود للأمن السيبراني يعمل على المنفذ {port}")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
