from flask import Flask, request, jsonify
import os
import requests
import datetime

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
    user_agent = request.headers.get('User-Agent', 'غير معروف')
    send_telegram(f"""🔥 <b>زائر جديد للموقع</b>
🌐 <b>IP:</b> {visitor_ip}
💻 <b>المتصفح:</b> {user_agent[:100]}
⏰ <b>الوقت:</b> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

<b>مبرمج عبود | @SSSTlF</b>""")
    
    return '''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>مبرمج عبود | @SSSTlF</title>
        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Cairo', sans-serif;
                background: #05070D;
                color: #F8FAFC;
                overflow-x: hidden;
                min-height: 100vh;
            }
            
            ::-webkit-scrollbar { width: 6px; }
            ::-webkit-scrollbar-track { background: #05070D; }
            ::-webkit-scrollbar-thumb { background: #E8C66A; border-radius: 10px; }

            .aurora {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 0;
                overflow: hidden;
            }
            .aurora::before {
                content: '';
                position: absolute;
                width: 600px;
                height: 600px;
                background: radial-gradient(circle, rgba(232, 198, 106, 0.08), transparent 70%);
                top: -10%;
                left: -10%;
                animation: aurora1 15s ease-in-out infinite alternate;
            }
            .aurora::after {
                content: '';
                position: absolute;
                width: 500px;
                height: 500px;
                background: radial-gradient(circle, rgba(59, 130, 246, 0.08), transparent 70%);
                bottom: -10%;
                right: -10%;
                animation: aurora2 20s ease-in-out infinite alternate;
            }
            @keyframes aurora1 {
                0% { transform: translate(0, 0) scale(1); }
                100% { transform: translate(200px, 100px) scale(1.5); }
            }
            @keyframes aurora2 {
                0% { transform: translate(0, 0) scale(1); }
                100% { transform: translate(-200px, -100px) scale(1.5); }
            }

            .container {
                position: relative;
                z-index: 1;
                max-width: 1400px;
                margin: 0 auto;
                padding: 20px;
            }

            /* Navbar */
            .navbar {
                background: rgba(5, 7, 13, 0.7);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(232, 198, 106, 0.1);
                border-radius: 24px;
                padding: 16px 32px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 40px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
            }
            .navbar .logo h1 {
                font-size: 28px;
                font-weight: 800;
                background: linear-gradient(135deg, #E8C66A, #F8FAFC, #E8C66A);
                background-size: 200% auto;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                animation: shimmer 3s ease-in-out infinite;
            }
            @keyframes shimmer {
                0%, 100% { background-position: 0% center; }
                50% { background-position: 200% center; }
            }
            .navbar .logo span {
                font-size: 12px;
                color: #AEB8C4;
                letter-spacing: 2px;
            }
            .navbar .logo .sub {
                font-size: 10px;
                color: #D4AF37;
                letter-spacing: 4px;
                opacity: 0.6;
            }

            /* Hero */
            .hero {
                text-align: center;
                padding: 60px 20px 40px;
                background: rgba(255,255,255,0.02);
                border-radius: 32px;
                border: 1px solid rgba(232, 198, 106, 0.05);
                margin-bottom: 40px;
            }
            .hero h1 {
                font-size: 64px;
                font-weight: 800;
                background: linear-gradient(135deg, #E8C66A, #F8FAFC, #E8C66A);
                background-size: 200% auto;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                animation: shimmer 3s ease-in-out infinite;
            }
            .hero .subtitle {
                font-size: 20px;
                color: #AEB8C4;
                margin: 10px 0;
            }
            .hero .tag {
                display: inline-block;
                padding: 8px 24px;
                border: 1px solid rgba(232, 198, 106, 0.2);
                border-radius: 50px;
                color: #D4AF37;
                font-size: 14px;
                letter-spacing: 4px;
                margin-top: 10px;
            }

            /* Profile Cards */
            .profiles {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 24px;
                margin-bottom: 40px;
            }
            .profile-card {
                background: rgba(255, 255, 255, 0.03);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-radius: 24px;
                padding: 30px;
                text-align: center;
                transition: 0.4s;
            }
            .profile-card:hover {
                transform: translateY(-10px);
                border-color: #E8C66A;
                box-shadow: 0 20px 60px rgba(232, 198, 106, 0.1);
            }
            .profile-card .avatar {
                font-size: 56px;
                margin-bottom: 12px;
            }
            .profile-card h3 {
                font-size: 20px;
                font-weight: 700;
                color: #F8FAFC;
            }
            .profile-card .role {
                color: #D4AF37;
                font-size: 14px;
                margin: 4px 0 12px;
            }
            .profile-card p {
                color: #AEB8C4;
                font-size: 14px;
                line-height: 1.6;
            }

            /* Buttons Grid - 2000+ buttons */
            .buttons-section {
                margin: 40px 0;
            }
            .buttons-section h2 {
                font-size: 32px;
                font-weight: 700;
                text-align: center;
                margin-bottom: 10px;
            }
            .buttons-section h2 span {
                background: linear-gradient(135deg, #E8C66A, #3B82F6);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .buttons-section .desc {
                text-align: center;
                color: #AEB8C4;
                margin-bottom: 30px;
                font-size: 16px;
            }
            .buttons-grid {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                justify-content: center;
            }
            .btn-inline {
                padding: 8px 16px;
                border-radius: 50px;
                font-size: 12px;
                font-weight: 600;
                border: none;
                cursor: pointer;
                transition: 0.3s;
                font-family: 'Cairo', sans-serif;
                background: rgba(255,255,255,0.05);
                color: #AEB8C4;
                border: 1px solid rgba(255,255,255,0.05);
                position: relative;
                overflow: hidden;
            }
            .btn-inline::before {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: conic-gradient(from 0deg, transparent, rgba(232, 198, 106, 0.05), transparent);
                animation: btnRotate 6s linear infinite;
                opacity: 0;
                transition: 0.3s;
            }
            .btn-inline:hover::before {
                opacity: 1;
            }
            @keyframes btnRotate {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            .btn-inline:hover {
                transform: scale(1.05);
                border-color: #E8C66A;
                color: #F8FAFC;
                box-shadow: 0 0 20px rgba(232, 198, 106, 0.1);
            }
            .btn-inline.gold {
                background: linear-gradient(135deg, #E8C66A, #D4AF37);
                color: #05070D;
            }
            .btn-inline.gold:hover {
                box-shadow: 0 0 30px rgba(232, 198, 106, 0.3);
            }
            .btn-inline.purple {
                background: linear-gradient(135deg, #6D28D9, #4F1C9E);
                color: #fff;
            }
            .btn-inline.purple:hover {
                box-shadow: 0 0 30px rgba(109, 40, 217, 0.3);
            }
            .btn-inline.blue {
                background: linear-gradient(135deg, #3B82F6, #1D4ED8);
                color: #fff;
            }
            .btn-inline.blue:hover {
                box-shadow: 0 0 30px rgba(59, 130, 246, 0.3);
            }
            .btn-inline.green {
                background: linear-gradient(135deg, #10B981, #059669);
                color: #fff;
            }
            .btn-inline.green:hover {
                box-shadow: 0 0 30px rgba(16, 185, 129, 0.3);
            }
            .btn-inline.red {
                background: linear-gradient(135deg, #EF4444, #DC2626);
                color: #fff;
            }
            .btn-inline.red:hover {
                box-shadow: 0 0 30px rgba(239, 68, 68, 0.3);
            }
            .btn-inline.pink {
                background: linear-gradient(135deg, #EC4899, #DB2777);
                color: #fff;
            }
            .btn-inline.pink:hover {
                box-shadow: 0 0 30px rgba(236, 72, 153, 0.3);
            }
            .btn-inline.cyan {
                background: linear-gradient(135deg, #06B6D4, #0891B2);
                color: #fff;
            }
            .btn-inline.cyan:hover {
                box-shadow: 0 0 30px rgba(6, 182, 212, 0.3);
            }
            .btn-inline.orange {
                background: linear-gradient(135deg, #F59E0B, #D97706);
                color: #fff;
            }
            .btn-inline.orange:hover {
                box-shadow: 0 0 30px rgba(245, 158, 11, 0.3);
            }
            .btn-inline.glass {
                background: rgba(255,255,255,0.05);
                backdrop-filter: blur(10px);
                border-color: rgba(255,255,255,0.1);
            }
            .btn-inline.glass:hover {
                background: rgba(232, 198, 106, 0.1);
                border-color: #E8C66A;
            }

            /* Footer */
            .footer {
                text-align: center;
                padding: 40px 20px;
                border-top: 1px solid rgba(255,255,255,0.05);
                margin-top: 40px;
                background: rgba(5, 7, 13, 0.5);
                backdrop-filter: blur(10px);
                border-radius: 24px;
            }
            .footer h3 {
                font-size: 24px;
                font-weight: 700;
                background: linear-gradient(135deg, #E8C66A, #F8FAFC);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .footer .sub {
                color: #AEB8C4;
                font-size: 14px;
                letter-spacing: 2px;
            }
            .footer .signature {
                color: #D4AF37;
                font-size: 12px;
                letter-spacing: 6px;
                opacity: 0.5;
                margin-top: 8px;
            }

            @media (max-width: 768px) {
                .hero h1 { font-size: 36px; }
                .navbar { flex-direction: column; gap: 12px; padding: 16px; }
                .profiles { grid-template-columns: 1fr; }
                .btn-inline { font-size: 10px; padding: 6px 12px; }
            }
        </style>
    </head>
    <body>
        <div class="aurora"></div>
        
        <div class="container">
            <!-- Navbar -->
            <nav class="navbar">
                <div class="logo">
                    <h1>مبرمج عبود</h1>
                    <div class="sub">@SSSTlF</div>
                </div>
                <div style="display:flex; gap:12px; flex-wrap:wrap;">
                    <button class="btn-inline gold" onclick="alert('مرحباً بك في عالم عبود!')">🚀 ابدأ الآن</button>
                    <button class="btn-inline glass" onclick="document.getElementById('buttons').scrollIntoView({behavior:'smooth'})">🔘 الأزرار</button>
                    <button class="btn-inline glass" onclick="document.getElementById('profiles').scrollIntoView({behavior:'smooth'})">👤 البروفايلات</button>
                </div>
            </nav>

            <!-- Hero -->
            <section class="hero">
                <h1>مبرمج عبود</h1>
                <div class="subtitle">@SSSTlF — أصل العرب</div>
                <div class="tag">✦ 2000+ زر تفاعلي ✦</div>
                <p style="color:#AEB8C4; max-width:600px; margin:20px auto; line-height:1.8;">
                    منصة فخمة تضم أكثر من 2000 زر حقيقي، بروفايلات احترافية، وتصميم سينمائي. كل الأزرار تعمل وتؤدي أوامر حقيقية.
                </p>
            </section>

            <!-- Profiles -->
            <section id="profiles" class="profiles">
                <div class="profile-card">
                    <div class="avatar">👨‍💻</div>
                    <h3>عبود</h3>
                    <div class="role">مبرمج رئيسي | @SSSTlF</div>
                    <p>خبير في تطوير الأنظمة، الذكاء الاصطناعي، والأمن السيبراني. صانع المحتوى التقني.</p>
                </div>
                <div class="profile-card">
                    <div class="avatar">🧠</div>
                    <h3>الذكاء الاصطناعي</h3>
                    <div class="role">AI Assistant</div>
                    <p>مساعد ذكي متطور قادر على تنفيذ الأوامر البرمجية والتحليلية بسرعة فائقة.</p>
                </div>
                <div class="profile-card">
                    <div class="avatar">🛡️</div>
                    <h3>الأمن السيبراني</h3>
                    <div class="role">Cyber Security</div>
                    <p>حماية متقدمة، اختبار اختراق، وتأمين الأنظمة ضد الهجمات الرقمية.</p>
                </div>
                <div class="profile-card">
                    <div class="avatar">☁️</div>
                    <h3>الحوسبة السحابية</h3>
                    <div class="role">Cloud Computing</div>
                    <p>بنية تحتية سحابية مرنة وقابلة للتوسع مع دعم عالمي.</p>
                </div>
            </section>

            <!-- 2000+ Buttons -->
            <section id="buttons" class="buttons-section">
                <h2>🔘 أكثر من <span>2000 زر</span> تفاعلي</h2>
                <p class="desc">جميع الأزرار حقيقية وتعمل — اضغط على أي زر لتجربة التفاعل الفوري</p>
                <div class="buttons-grid" id="buttonsGrid">
                </div>
            </section>

            <!-- Footer -->
            <footer class="footer">
                <h3>مبرمج عبود</h3>
                <div class="sub">@SSSTlF</div>
                <div class="signature">أصل العرب</div>
                <p style="color:#AEB8C4; font-size:13px; margin-top:16px;">
                    © 2026 جميع الحقوق محفوظة — تصميم فخم بأكثر من 2000 زر
                </p>
            </footer>
        </div>

        <script>
            // ===== توليد 2000+ زر حقيقي =====
            const colors = ['', 'gold', 'purple', 'blue', 'green', 'red', 'pink', 'cyan', 'orange', 'glass'];
            const labels = [
                'ابدأ', 'تنفيذ', 'تشغيل', 'تحميل', 'حفظ', 'إرسال', 'بحث', 'تصفح', 'تحديث', 'حذف',
                'إضافة', 'تعديل', 'عرض', 'طباعة', 'تصدير', 'استيراد', 'نسخ', 'لصق', 'قص', 'تراجع',
                'إعادة', 'تكبير', 'تصغير', 'تدوير', 'فلتر', 'فرز', 'تجميع', 'تقسيم', 'دمج', 'تحويل',
                'برمجة', 'تصميم', 'تطوير', 'تحليل', 'اختبار', 'نشر', 'تشغيل', 'إيقاف', 'إعادة تشغيل',
                'تسجيل', 'تسجيل دخول', 'تسجيل خروج', 'تأكيد', 'إلغاء', 'موافق', 'رفض', 'تخطي',
                'متابعة', 'رجوع', 'التالي', 'السابق', 'الأول', 'الأخير', 'توسيط', 'محاذاة',
                'إظهار', 'إخفاء', 'تبديل', 'تحديد الكل', 'إلغاء التحديد', 'عكس التحديد',
                'رفع', 'تنزيل', 'تثبيت', 'إزالة', 'تحديث', 'ترقية', 'تهيئة', 'إصلاح',
                'تحسين', 'تسريع', 'تبسيط', 'تطوير', 'إعادة هيكلة', 'تقييم', 'مراجعة',
                'اعتماد', 'رفض', 'تعليق', 'إعادة توجيه', 'إعادة توجيه آمن', 'إعادة توجيه سريع',
                'تحليل عميق', 'تحليل سريع', 'تحليل شامل', 'تحليل أساسي', 'تحليل متقدم',
                'ذكاء اصطناعي', 'تعلم آلي', 'تعلم عميق', 'شبكات عصبية', 'معالجة لغة طبيعية',
                'رؤية حاسوبية', 'معالجة صوتية', 'توليد نصوص', 'توليد صور', 'ترجمة فورية',
                'نسخ احتياطي', 'استعادة نسخة', 'تشفير', 'فك تشفير', 'توقيع رقمي', 'مصادقة'
            ];

            const extraLabels = [];
            for (let i = 1; i <= 150; i++) {
                extraLabels.push(`أمر ${i}`);
                extraLabels.push(`تنفيذ ${i}`);
                extraLabels.push(`زر ${i}`);
                extraLabels.push(`كود ${i}`);
                extraLabels.push(`دالة ${i}`);
                extraLabels.push(`متغير ${i}`);
                extraLabels.push(`مشروع ${i}`);
                extraLabels.push(`تطبيق ${i}`);
                extraLabels.push(`خدمة ${i}`);
                extraLabels.push(`منصة ${i}`);
            }

            const allLabels = [...labels, ...extraLabels];
            const buttonsContainer = document.getElementById('buttonsGrid');

            // توليد 2000+ زر
            for (let i = 0; i < 2050; i++) {
                const btn = document.createElement('button');
                const label = allLabels[i % allLabels.length];
                const colorClass = colors[i % colors.length];
                btn.className = `btn-inline ${colorClass}`;
                btn.textContent = `✦ ${label}`;
                
                // كل زر له وظيفة مختلفة
                const actions = [
                    `alert('✅ تم تنفيذ الأمر: ${label}')`,
                    `console.log('${label} clicked')`,
                    `document.body.style.background = '#' + Math.floor(Math.random()*16777215).toString(16)`,
                    `alert('🔄 جاري تنفيذ ${label}...')`,
                    `fetch('/ping').then(r=>r.text()).then(console.log)`,
                    `alert('📌 ${label} — تم بنجاح')`,
                    `console.log('🟢 ${label} — عبود @SSSTlF')`,
                    `alert('🚀 ${label} — تحت أمرك يا سيدي')`,
                    `alert('🌟 ${label} — أصل العرب')`,
                    `document.getElementById('buttonsGrid').style.background = '#' + Math.floor(Math.random()*16777215).toString(16)`
                ];
                
                btn.onclick = new Function(actions[i % actions.length]);
                buttonsContainer.appendChild(btn);
            }

            console.log('✅ تم توليد ' + buttonsContainer.children.length + ' زر تفاعلي');
            console.log('🔹 مبرمج عبود | @SSSTlF | أصل العرب');
        </script>
    </body>
    </html>
    '''

@app.route('/ping')
def ping():
    return 'pong'

if __name__ == '__main__':
    send_telegram(f"""🔥 <b>تم تشغيل الموقع الفخم</b>
🎯 <b>مبرمج عبود | @SSSTlF</b>
🔘 <b>2000+ زر تفاعلي</b>
⏰ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}""")
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
