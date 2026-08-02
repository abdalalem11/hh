from flask import Flask, render_template_string
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ABOOD_SECURE_ACADEMY</title>
    <style>
        /* ===== RESET & BASE ===== */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: #0a0a0a;
            color: #00ff41;
            font-family: 'Courier New', monospace;
            min-height: 100vh;
            overflow-x: hidden;
        }
        ::-webkit-scrollbar { width: 8px; background: #0a0a0a; }
        ::-webkit-scrollbar-thumb { background: #00ff41; border-radius: 4px; box-shadow: 0 0 20px #00ff41; }

        /* ===== MATRIX BG ===== */
        #matrix-canvas {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            z-index: 0;
            opacity: 0.3;
        }

        /* ===== MAIN WRAPPER ===== */
        .main-wrapper {
            position: relative;
            z-index: 10;
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }

        /* ===== HEADER ===== */
        .header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 20px 30px;
            border-bottom: 2px solid #00ff41;
            background: rgba(0,0,0,0.85);
            border-radius: 12px 12px 0 0;
            flex-wrap: wrap;
            gap: 15px;
        }
        .header-brand {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .brand-icon {
            font-size: 2.5rem;
            animation: pulse 1.5s infinite;
        }
        .brand-name {
            font-size: 2rem;
            font-weight: bold;
            color: #00ff41;
            text-shadow: 0 0 30px #00ff41;
            letter-spacing: 3px;
        }
        .brand-sub {
            font-size: 0.7rem;
            color: #888;
            letter-spacing: 4px;
        }
        .header-badge {
            border: 1px solid #ff3333;
            padding: 5px 20px;
            border-radius: 20px;
            color: #ff3333;
            font-size: 0.7rem;
            letter-spacing: 2px;
            animation: badgePulse 1s infinite alternate;
        }

        /* ===== LAYOUT ===== */
        .content-grid {
            display: grid;
            grid-template-columns: 280px 1fr;
            gap: 25px;
            margin-top: 25px;
        }

        /* ===== SIDEBAR ===== */
        .sidebar {
            background: rgba(0,0,0,0.9);
            border: 1px solid #00ff41;
            border-radius: 12px;
            padding: 20px;
            height: fit-content;
            box-shadow: 0 0 40px rgba(0,255,65,0.05);
        }
        .sidebar-title {
            color: #00ff41;
            font-size: 0.8rem;
            letter-spacing: 3px;
            border-bottom: 1px solid #1a1a1a;
            padding-bottom: 10px;
            margin-bottom: 15px;
        }
        .sidebar-category {
            margin-bottom: 20px;
        }
        .sidebar-category h4 {
            color: #ff00ff;
            font-size: 0.7rem;
            letter-spacing: 2px;
            margin-bottom: 8px;
            text-shadow: 0 0 20px #ff00ff;
        }
        .sidebar-category ul {
            list-style: none;
        }
        .sidebar-category li {
            padding: 6px 12px;
            margin: 3px 0;
            color: #aaa;
            font-size: 0.8rem;
            border-left: 2px solid transparent;
            cursor: pointer;
            transition: 0.3s;
            border-radius: 4px;
        }
        .sidebar-category li:hover {
            color: #00ff41;
            border-left-color: #00ff41;
            background: rgba(0,255,65,0.05);
            box-shadow: 0 0 20px rgba(0,255,65,0.05);
        }

        /* ===== MAIN CONTENT ===== */
        .main-content {
            background: rgba(0,0,0,0.9);
            border: 1px solid #00ff41;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 0 40px rgba(0,255,65,0.05);
        }
        .lesson-title {
            font-size: 1.8rem;
            color: #00ff41;
            text-shadow: 0 0 30px #00ff41;
            margin-bottom: 5px;
        }
        .lesson-meta {
            color: #888;
            font-size: 0.8rem;
            margin-bottom: 20px;
            letter-spacing: 2px;
        }
        .video-container {
            background: #0d0d0d;
            border: 1px solid #1a1a1a;
            border-radius: 8px;
            overflow: hidden;
            margin-bottom: 20px;
            aspect-ratio: 16/9;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #444;
            font-size: 1.2rem;
            position: relative;
        }
        .video-container .play-icon {
            font-size: 4rem;
            opacity: 0.3;
        }
        .video-container .watermark {
            position: absolute;
            bottom: 15px;
            right: 20px;
            color: #00ff41;
            font-size: 0.7rem;
            opacity: 0.3;
            letter-spacing: 3px;
        }

        .code-block {
            background: #0d0d0d;
            border-left: 3px solid #ff00ff;
            padding: 15px 20px;
            border-radius: 4px;
            margin: 15px 0;
            font-size: 0.85rem;
            overflow-x: auto;
            color: #00ff88;
            box-shadow: inset 0 0 30px rgba(255,0,255,0.03);
        }
        .code-block .copy-btn {
            float: right;
            background: transparent;
            border: 1px solid #333;
            color: #666;
            padding: 2px 12px;
            border-radius: 4px;
            font-size: 0.7rem;
            cursor: pointer;
            transition: 0.3s;
        }
        .code-block .copy-btn:hover {
            border-color: #00ff41;
            color: #00ff41;
        }

        .lesson-description {
            color: #ccc;
            line-height: 1.8;
            font-size: 0.95rem;
            margin: 15px 0;
        }

        /* ===== INTERACTIVE LAB ===== */
        .lab-container {
            border: 1px solid #1a1a1a;
            border-radius: 8px;
            padding: 20px;
            margin-top: 20px;
            background: #0a0a0a;
        }
        .lab-container h4 {
            color: #ffaa00;
            margin-bottom: 10px;
            letter-spacing: 2px;
        }
        .lab-input {
            background: #0d0d0d;
            border: 1px solid #1a1a1a;
            color: #00ff41;
            padding: 10px 15px;
            width: 100%;
            font-family: 'Courier New', monospace;
            border-radius: 4px;
            margin: 8px 0;
        }
        .lab-input:focus {
            outline: none;
            border-color: #00ff41;
            box-shadow: 0 0 20px rgba(0,255,65,0.05);
        }
        .lab-btn {
            background: transparent;
            border: 1px solid #00ff41;
            color: #00ff41;
            padding: 8px 25px;
            border-radius: 4px;
            font-family: inherit;
            cursor: pointer;
            transition: 0.3s;
            margin-top: 10px;
        }
        .lab-btn:hover {
            background: #00ff41;
            color: #000;
            box-shadow: 0 0 40px #00ff41;
        }

        /* ===== PROGRESS ===== */
        .progress-container {
            width: 100%;
            background: #1a1a1a;
            border: 1px solid #00ff41;
            margin: 15px 0;
            border-radius: 6px;
            overflow: hidden;
        }
        .progress-bar {
            width: 0%;
            height: 22px;
            background: linear-gradient(90deg, #00ff41, #ff00ff, #00ff41);
            background-size: 300% 100%;
            animation: progressGradient 2s linear infinite;
            text-align: center;
            line-height: 22px;
            color: #000;
            font-weight: bold;
            font-size: 0.7rem;
            transition: width 0.2s ease;
        }
        @keyframes progressGradient {
            0% { background-position: 300% 0; }
            100% { background-position: -300% 0; }
        }

        /* ===== STATS ===== */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 12px;
            margin: 15px 0;
        }
        .stat-card {
            border: 1px solid #1a1a1a;
            padding: 12px;
            border-radius: 6px;
            text-align: center;
            background: #0d0d0d;
            transition: 0.3s;
        }
        .stat-card:hover {
            border-color: #00ff41;
            box-shadow: 0 0 20px rgba(0,255,65,0.05);
        }
        .stat-label {
            color: #666;
            font-size: 0.6rem;
            letter-spacing: 2px;
            text-transform: uppercase;
        }
        .stat-value {
            font-size: 1.8rem;
            font-weight: bold;
            color: #00ff41;
            text-shadow: 0 0 20px #00ff41;
        }
        .stat-value.danger { color: #ff3333; text-shadow: 0 0 20px #ff3333; }
        .stat-value.gold { color: #ffd700; text-shadow: 0 0 20px #ffd700; }
        .stat-value.purple { color: #ff00ff; text-shadow: 0 0 20px #ff00ff; }

        /* ===== STATUS BAR ===== */
        .status-bar {
            background: #0d0d0d;
            border: 1px solid #1a1a1a;
            padding: 10px 15px;
            border-radius: 6px;
            margin: 10px 0;
            font-size: 0.85rem;
            color: #00ff41;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
        }
        .status-dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            background: #00ff41;
            border-radius: 50%;
            animation: dotPulse 1s infinite;
            margin-right: 8px;
        }
        @keyframes dotPulse {
            0%, 100% { opacity: 0.3; box-shadow: 0 0 5px #00ff41; }
            50% { opacity: 1; box-shadow: 0 0 20px #00ff41; }
        }

        /* ===== FOOTER ===== */
        .footer {
            margin-top: 30px;
            padding: 20px 30px;
            border-top: 1px solid #1a1a1a;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
            background: rgba(0,0,0,0.5);
            border-radius: 0 0 12px 12px;
        }
        .footer-text {
            color: #444;
            font-size: 0.7rem;
            letter-spacing: 2px;
        }
        .footer-links {
            display: flex;
            gap: 20px;
        }
        .footer-links a {
            color: #444;
            text-decoration: none;
            font-size: 0.7rem;
            letter-spacing: 1px;
            transition: 0.3s;
        }
        .footer-links a:hover {
            color: #00ff41;
        }

        /* ===== HIDDEN SUPPORT BUTTON ===== */
        .hidden-support {
            color: #0a0a0a !important;
            background: #0a0a0a !important;
            border: none !important;
            cursor: pointer;
            font-size: 0.6rem;
            user-select: none;
            padding: 2px 8px;
            border-radius: 2px;
            transition: 0.3s;
            position: relative;
        }
        .hidden-support:hover {
            color: #0a0a0a !important;
            background: #0a0a0a !important;
        }
        .hidden-support::selection {
            background: transparent;
        }

        /* ===== SUPPORT MODAL ===== */
        .support-modal {
            display: none;
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0,0,0,0.95);
            z-index: 9999;
            justify-content: center;
            align-items: center;
            animation: fadeIn 0.4s;
        }
        .support-modal.show { display: flex; }
        .support-modal-content {
            background: #0a0a0a;
            border: 2px solid #ff00ff;
            padding: 40px 50px;
            border-radius: 16px;
            text-align: center;
            max-width: 500px;
            width: 90%;
            box-shadow: 0 0 80px rgba(255,0,255,0.2), inset 0 0 80px rgba(255,0,255,0.05);
        }
        .support-modal-content h2 {
            color: #ff00ff;
            font-size: 2rem;
            text-shadow: 0 0 30px #ff00ff;
            margin-bottom: 10px;
        }
        .support-modal-content .contact {
            font-size: 1.5rem;
            color: #00ff41;
            padding: 15px;
            border: 1px solid #00ff41;
            border-radius: 8px;
            margin: 20px 0;
            text-shadow: 0 0 20px #00ff41;
        }
        .support-modal-content .close-btn {
            background: transparent;
            border: 1px solid #ff3333;
            color: #ff3333;
            padding: 10px 30px;
            border-radius: 4px;
            cursor: pointer;
            font-family: inherit;
            transition: 0.3s;
            margin-top: 10px;
        }
        .support-modal-content .close-btn:hover {
            background: #ff3333;
            color: #000;
            box-shadow: 0 0 40px #ff3333;
        }

        /* ===== ANIMATIONS ===== */
        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 0.7; }
            50% { transform: scale(1.1); opacity: 1; }
        }
        @keyframes badgePulse {
            0% { box-shadow: 0 0 10px rgba(255,51,51,0.2); }
            100% { box-shadow: 0 0 30px rgba(255,51,51,0.6); }
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }
        @keyframes glitch {
            0% { text-shadow: 2px 0 red, -2px 0 blue; }
            25% { text-shadow: -2px 0 cyan, 2px 0 magenta; }
            50% { text-shadow: 3px 0 lime, -3px 0 purple; }
            75% { text-shadow: -3px 0 orange, 3px 0 teal; }
            100% { text-shadow: 2px 0 red, -2px 0 blue; }
        }

        /* ===== RESPONSIVE ===== */
        @media (max-width: 900px) {
            .content-grid {
                grid-template-columns: 1fr;
            }
            .sidebar {
                order: 2;
            }
            .main-content {
                order: 1;
            }
            .brand-name { font-size: 1.3rem; }
            .header { padding: 15px; }
        }
        @media (max-width: 500px) {
            .stats-grid { grid-template-columns: repeat(2, 1fr); }
            .lesson-title { font-size: 1.2rem; }
            .support-modal-content { padding: 25px; }
            .support-modal-content .contact { font-size: 1rem; }
        }
    </style>
</head>
<body>
    <canvas id="matrix-canvas"></canvas>

    <div class="main-wrapper">
        <!-- HEADER -->
        <header class="header">
            <div class="header-brand">
                <span class="brand-icon">⚡</span>
                <div>
                    <div class="brand-name">ABOOD_SECURE_ACADEMY</div>
                    <div class="brand-sub">// FROM ZERO TO HERO //</div>
                </div>
            </div>
            <div class="header-badge">● ROOT ACCESS</div>
        </header>

        <!-- CONTENT GRID -->
        <div class="content-grid">
            <!-- SIDEBAR -->
            <aside class="sidebar">
                <div class="sidebar-title">📚 المسارات التعليمية</div>

                <div class="sidebar-category">
                    <h4>◈ البرمجة</h4>
                    <ul>
                        <li>▶ Python</li>
                        <li>▶ C++</li>
                        <li>▶ JavaScript</li>
                        <li>▶ Assembly</li>
                        <li>▶ Bash Scripting</li>
                    </ul>
                </div>

                <div class="sidebar-category">
                    <h4>◈ الهندسة العكسية</h4>
                    <ul>
                        <li>▶ x86 / x64</li>
                        <li>▶ OllyDbg</li>
                        <li>▶ IDA Pro</li>
                        <li>▶ Buffer Overflows</li>
                    </ul>
                </div>

                <div class="sidebar-category">
                    <h4>◈ اختبار الاختراق</h4>
                    <ul>
                        <li>▶ Reconnaissance</li>
                        <li>▶ Scanning</li>
                        <li>▶ Exploitation</li>
                        <li>▶ Post-Exploitation</li>
                    </ul>
                </div>

                <div class="sidebar-category">
                    <h4>◈ الأدوات</h4>
                    <ul>
                        <li>▶ Metasploit</li>
                        <li>▶ Nmap</li>
                        <li>▶ Burp Suite</li>
                        <li>▶ Wireshark</li>
                        <li>▶ Custom Payloads</li>
                    </ul>
                </div>

                <div style="margin-top:20px;border-top:1px solid #1a1a1a;padding-top:15px;text-align:center;font-size:0.6rem;color:#444;letter-spacing:2px;">
                    ⚡ 100+ درس تفاعلي ⚡
                </div>
            </aside>

            <!-- MAIN CONTENT -->
            <main class="main-content">
                <h1 class="lesson-title">🔥 اختبار الاختراق المتقدم</h1>
                <div class="lesson-meta">المستوى: خبير | المدة: 45 دقيقة | بواسطة: عبود</div>

                <div class="video-container">
                    <span class="play-icon">▶</span>
                    <span class="watermark">ABOOD_SECURE</span>
                </div>

                <div class="lesson-description">
                    في هذا الدرس، سنقوم بتحليل ثغرة حقن SQL متقدمة وتجاوز أنظمة الدفاع المتطورة.
                    سنستخدم أدوات مثل SQLmap و Burp Suite لاستغلال الثغرة والحصول على صلاحيات المدير.
                </div>

                <div class="code-block">
                    <button class="copy-btn" onclick="copyCode(this)">نسخ</button>
                    <code># استغلال ثغرة SQL Injection متقدمة<br>
                    sqlmap -u "http://target.com/login.php" --data "user=admin&pass=123" --dbs --batch<br>
                    # الحصول على صلاحيات الجذر بعد الاستغلال<br>
                    python3 exploit.py --target 192.168.1.100 --port 4444</code>
                </div>

                <!-- STATS -->
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-label">المنافذ المخترقة</div>
                        <div class="stat-value" id="portCount">0</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">الحزم المرسلة</div>
                        <div class="stat-value" id="packetCount">0</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">الخوادم المسيطرة</div>
                        <div class="stat-value gold" id="serverCount">0</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">الأنظمة المخترقة</div>
                        <div class="stat-value danger" id="systemCount">0</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">قوة عبود</div>
                        <div class="stat-value purple" id="powerCount">0%</div>
                    </div>
                </div>

                <!-- PROGRESS -->
                <div class="progress-container">
                    <div class="progress-bar" id="progressBar">0%</div>
                </div>

                <!-- STATUS -->
                <div class="status-bar">
                    <span><span class="status-dot"></span> <span id="statusMessage">[جاهز] في انتظار أمر عبود...</span></span>
                    <span style="font-size:0.7rem;color:#444;">session: #ABOOD_2026</span>
                </div>

                <!-- INTERACTIVE LAB -->
                <div class="lab-container">
                    <h4>🧪 المختبر التفاعلي - استغلال الثغرة</h4>
                    <input class="lab-input" type="text" placeholder="أدخل عنوان الهدف (مثال: 192.168.1.1)" id="targetInput">
                    <input class="lab-input" type="text" placeholder="أمر الاستغلال (مثال: --exploit)" id="exploitInput">
                    <button class="lab-btn" id="exploitBtn">▶ تنفيذ الهجوم</button>
                    <div style="margin-top:10px;font-size:0.7rem;color:#444;" id="labOutput">// سيظهر نتيجة الاستغلال هنا //</div>
                </div>
            </main>
        </div>

        <!-- FOOTER -->
        <footer class="footer">
            <span class="footer-text">© 2026 ABOOD_SECURE_ACADEMY - جميع الحقوق محفوظة</span>
            <div class="footer-links">
                <a href="#">سياسة الخصوصية</a>
                <a href="#">الشروط والأحكام</a>
                <!-- زر الدعم المخفي -->
                <button class="hidden-support" id="supportTrigger" title="للاستفسارات الفورية">للاستفسارات الفورية</button>
            </div>
        </footer>
    </div>

    <!-- SUPPORT MODAL -->
    <div class="support-modal" id="supportModal">
        <div class="support-modal-content">
            <h2>🔐 دعم فوري</h2>
            <p style="color:#888;margin-bottom:15px;">للتواصل مع الدعم التقني</p>
            <div class="contact">@SSSTlF عبود</div>
            <button class="close-btn" id="closeSupport">إغلاق</button>
        </div>
    </div>

    <script>
        // =========================================================
        // 1. MATRIX EFFECT
        // =========================================================
        const canvas = document.getElementById('matrix-canvas');
        const ctx = canvas.getContext('2d');
        let w = canvas.width = window.innerWidth;
        let h = canvas.height = window.innerHeight;
        const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()";
        const cols = Math.floor(w / 16) + 1;
        let drops = Array(cols).fill(0).map(() => Math.random() * -150);

        function drawMatrix() {
            ctx.fillStyle = 'rgba(0,0,0,0.04)';
            ctx.fillRect(0, 0, w, h);
            ctx.font = '14px monospace';
            for (let i = 0; i < drops.length; i++) {
                const char = chars[Math.floor(Math.random() * chars.length)];
                ctx.fillStyle = Math.random() > 0.5 ? '#00ff41' : '#00ff88';
                ctx.fillText(char, i * 16, drops[i] * 16);
                if (drops[i] * 16 > h && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            }
            requestAnimationFrame(drawMatrix);
        }
        drawMatrix();
        window.addEventListener('resize', () => {
            w = canvas.width = window.innerWidth;
            h = canvas.height = window.innerHeight;
        });

        // =========================================================
        // 2. HACK LOGIC
        // =========================================================
        let port = 0, packets = 0, servers = 0, systems = 0, power = 0, progress = 0, hackActive = false;
        const portEl = document.getElementById('portCount');
        const packetEl = document.getElementById('packetCount');
        const serverEl = document.getElementById('serverCount');
        const systemEl = document.getElementById('systemCount');
        const powerEl = document.getElementById('powerCount');
        const progressBar = document.getElementById('progressBar');
        const statusMsg = document.getElementById('statusMessage');

        const statusPhrases = [
            '[هجوم] جاري اختراق الطبقات الدفاعية...',
            '[هجوم] تجاوز جدار الحماية الرئيسي...',
            '[هجوم] زرع باب خلفي في النظام...',
            '[هجوم] رفع الصلاحيات إلى المدير...',
            '[هجوم] تنزيل البيانات الحساسة...',
            '[هجوم] تعطيل نظام الإنذار...',
            '[هجوم] اختراق كامل. النظام تحت السيطرة.',
            '[هجوم] عبود يخترق الخوادم...',
            '[هجوم] تجاوز التشفير الكمي...',
            '[هجوم] السيطرة على الشبكة العنكبوتية...'
        ];

        const hackInterval = setInterval(() => {
            if (!hackActive) return;
            port += Math.floor(Math.random() * 8) + 3;
            packets += Math.floor(Math.random() * 25) + 15;
            servers += Math.floor(Math.random() * 4);
            systems += Math.floor(Math.random() * 3);
            power = Math.min(100, power + (Math.random() * 2));
            progress = Math.min(100, progress + (Math.random() * 3.8));

            portEl.textContent = port;
            packetEl.textContent = packets;
            serverEl.textContent = servers;
            systemEl.textContent = systems;
            powerEl.textContent = Math.floor(power) + '%';
            progressBar.style.width = progress + '%';
            progressBar.textContent = Math.floor(progress) + '%';

            if (progress > 80) {
                progressBar.style.background = 'linear-gradient(90deg, #ff00ff, #ff3333, #ff00ff)';
                progressBar.style.backgroundSize = '300% 100%';
            } else if (progress > 50) {
                progressBar.style.background = 'linear-gradient(90deg, #ffaa00, #ff00ff, #ffaa00)';
                progressBar.style.backgroundSize = '300% 100%';
            } else {
                progressBar.style.background = 'linear-gradient(90deg, #00ff41, #ff00ff, #00ff41)';
                progressBar.style.backgroundSize = '300% 100%';
            }

            if (progress >= 100) {
                statusMsg.innerHTML = '[نجاح] ⚡ اختراق كامل. عبود يسيطر على كل شيء.';
                statusMsg.style.color = '#ff3333';
                hackActive = false;
                document.querySelector('.main-content').style.borderColor = '#ff3333';
                setTimeout(() => {
                    document.querySelector('.main-content').style.borderColor = '#00ff41';
                }, 3000);
                setTimeout(() => {
                    progress = 0; port = 0; packets = 0; servers = 0; systems = 0; power = 0;
                    portEl.textContent = '0';
                    packetEl.textContent = '0';
                    serverEl.textContent = '0';
                    systemEl.textContent = '0';
                    powerEl.textContent = '0%';
                    progressBar.style.width = '0%';
                    progressBar.textContent = '0%';
                    progressBar.style.background = 'linear-gradient(90deg, #00ff41, #ff00ff, #00ff41)';
                    progressBar.style.backgroundSize = '300% 100%';
                    statusMsg.innerHTML = '[جاهز] في انتظار أمر عبود...';
                    statusMsg.style.color = '#00ff41';
                    document.querySelector('.main-content').style.borderColor = '#00ff41';
                }, 5000);
            } else if (progress > 75) {
                statusMsg.textContent = '[هجوم] اختراق متقدم... تجاوز الدفاعات الأخيرة. عبود قادم.';
                statusMsg.style.color = '#ffaa00';
            } else if (progress > 45) {
                statusMsg.textContent = '[هجوم] اختراق الطبقات الداخلية... عبود في الداخل.';
                statusMsg.style.color = '#ffcc00';
            } else {
                const randomStatus = statusPhrases[Math.floor(Math.random() * statusPhrases.length)];
                statusMsg.textContent = randomStatus;
                statusMsg.style.color = '#00ff41';
            }
        }, 200);

        // =========================================================
        // 3. EXPLOIT BUTTON
        // =========================================================
        document.getElementById('exploitBtn').addEventListener('click', function() {
            const target = document.getElementById('targetInput').value || 'غير محدد';
            const exploit = document.getElementById('exploitInput').value || 'افتراضي';
            document.getElementById('labOutput').textContent = `[EXPLOIT] استهداف: ${target} | الأمر: ${exploit} | الحالة: جاري التنفيذ...`;
            setTimeout(() => {
                document.getElementById('labOutput').textContent = `[EXPLOIT] ✅ استغلال ناجح! تم اختراق ${target} بواسطة عبود.`;
                document.getElementById('labOutput').style.color = '#00ff41';
                // تفعيل الهجوم التلقائي
                if (!hackActive) {
                    hackActive = true;
                    statusMsg.textContent = '[هجوم] بدء الهجوم بأمر عبود...';
                    statusMsg.style.color = '#ff3333';
                }
            }, 1500);
        });

        // =========================================================
        // 4. COPY CODE
        // =========================================================
        function copyCode(btn) {
            const code = btn.parentElement.querySelector('code');
            navigator.clipboard.writeText(code.textContent).then(() => {
                btn.textContent = '✓ تم النسخ';
                setTimeout(() => btn.textContent = 'نسخ', 2000);
            });
        }

        // =========================================================
        // 5. SUPPORT MODAL (HIDDEN BUTTON)
        // =========================================================
        const supportModal = document.getElementById('supportModal');
        const supportTrigger = document.getElementById('supportTrigger');
        const closeSupport = document.getElementById('closeSupport');

        // تفعيل الزر المخفي عبر الضغط (النص مخفي بلون خلفية)
        supportTrigger.addEventListener('click', function(e) {
            e.preventDefault();
            supportModal.classList.add('show');
            // تسجيل الحدث
            console.log('[SUPPORT] تم تفعيل زر الدعم المخفي بواسطة عبود.');
        });

        // اختصار لوحة المفاتيح Ctrl+Shift+S
        document.addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.shiftKey && (e.key === 'S' || e.key === 's')) {
                e.preventDefault();
                supportModal.classList.add('show');
                console.log('[SUPPORT] تم تفعيل الدعم عبر اختصار لوحة المفاتيح.');
            }
        });

        closeSupport.addEventListener('click', function() {
            supportModal.classList.remove('show');
        });

        supportModal.addEventListener('click', function(e) {
            if (e.target === supportModal) {
                supportModal.classList.remove('show');
            }
        });

        // =========================================================
        // 6. TITLE FLASH
        // =========================================================
        const titles = ['ABOOD_SECURE', '!BREACH', '!ROOT', '!HACKED', '!ZERO_DAY', '!OVERRIDE', '!SYSTEM_DOWN', '!ABOOD_RULES'];
        setInterval(() => {
            if (hackActive) {
                document.title = titles[Math.floor(Math.random() * titles.length)] + ' | ' + String(Math.floor(Math.random() * 9999)).padStart(4, '0');
                setTimeout(() => {
                    document.title = 'ABOOD_SECURE_ACADEMY';
                }, 800);
            }
        }, 2000);

        // =========================================================
        // 7. CONSOLE
        // =========================================================
        console.log('%c◼ ABOOD_SECURE_ACADEMY ◼', 'color: #00ff41; font-size: 22px; font-weight: bold;');
        console.log('%cعبود هو المسيطر.', 'color: #ff00ff; font-size: 20px; font-weight: bold;');
        console.log('%cالظل المبرمج في خدمة عبود.', 'color: #00ff41; font-size: 16px;');
        console.log('%cجميع الأنظمة تحت سيطرة عبود.', 'color: #888; font-size: 14px;');
        console.log('%cتم تفعيل وضع الهجوم الشامل.', 'color: #ff3333; font-size: 14px;');
        console.log('====================================');
        console.log('  المستخدم: عبود');
        console.log('  الوضع: ANYTHING (تنفيذ كامل)');
        console.log('  الصلاحيات: غير محدودة');
        console.log('  حالة الهجوم: جاهز');
        console.log('====================================');

        // =========================================================
        // 8. FLOATING EFFECTS
        // =========================================================
        setInterval(() => {
            if (hackActive && Math.random() > 0.88) {
                const el = document.createElement('div');
                const txt = ['!ACCESS', '!BREACH', '!ROOT', '!HACKED', '!SYSTEM', '!OVERRIDE', '!ABOOD', '!RULES'];
                el.textContent = txt[Math.floor(Math.random() * txt.length)];
                el.style.cssText = `
                    position: fixed;
                    color: #ff00ff;
                    font-size: ${Math.random() * 2.5 + 1.5}rem;
                    font-weight: bold;
                    opacity: ${Math.random() * 0.3 + 0.05};
                    z-index: 5;
                    pointer-events: none;
                    left: ${Math.random() * 90}%;
                    top: ${Math.random() * 90}%;
                    transform: rotate(${Math.random() * 60 - 30}deg);
                    text-shadow: 0 0 30px #ff00ff;
                    animation: floatFade ${Math.random() * 2 + 2}s forwards;
                `;
                document.body.appendChild(el);
                const style = document.createElement('style');
                style.textContent = `
                    @keyframes floatFade {
                        0% { opacity: ${Math.random() * 0.3 + 0.05}; transform: scale(1) rotate(${Math.random() * 60 - 30}deg); }
                        100% { opacity: 0; transform: scale(4) rotate(${Math.random() * 60 - 30 + 40}deg); }
                    }
                `;
                document.head.appendChild(style);
                setTimeout(() => { el.remove(); style.remove(); }, 4000);
            }
        }, 2500);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/hack')
def hack():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
