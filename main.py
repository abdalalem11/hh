from flask import Flask, render_template_string
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>نظام الاختراق المتقدم</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background-color: #0a0a0a;
            color: #00ff41;
            font-family: 'Courier New', Courier, monospace;
            height: 100vh;
            overflow: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            position: relative;
            user-select: none;
        }

        #matrix-canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            opacity: 0.4;
        }

        .glitch-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
            pointer-events: none;
            background: repeating-linear-gradient(
                0deg,
                transparent,
                transparent 2px,
                rgba(0, 255, 65, 0.03) 2px,
                rgba(0, 255, 65, 0.03) 4px
            );
            animation: scanline 8s linear infinite;
        }

        @keyframes scanline {
            0% { transform: translateY(-100%); }
            100% { transform: translateY(100%); }
        }

        .overlay-content {
            position: relative;
            z-index: 10;
            text-align: center;
            background: rgba(0, 0, 0, 0.88);
            padding: 2rem 3rem;
            border: 2px solid #00ff41;
            box-shadow: 0 0 80px rgba(0, 255, 65, 0.4), inset 0 0 80px rgba(0, 255, 65, 0.15);
            border-radius: 16px;
            backdrop-filter: blur(4px);
            width: 92%;
            max-width: 1000px;
            animation: borderPulse 1.5s infinite alternate;
            transform: scale(1);
            transition: all 0.3s;
        }

        @keyframes borderPulse {
            0% { box-shadow: 0 0 30px rgba(0, 255, 65, 0.2), inset 0 0 30px rgba(0, 255, 65, 0.05); }
            100% { box-shadow: 0 0 100px rgba(0, 255, 65, 0.7), inset 0 0 100px rgba(0, 255, 65, 0.25); }
        }

        .glitch {
            font-size: 3.2rem;
            font-weight: bold;
            text-transform: uppercase;
            color: #00ff41;
            text-shadow: 0 0 20px #00ff41, 0 0 40px #003b00;
            animation: glitch-anim 2s infinite;
            letter-spacing: 8px;
            word-break: break-word;
            position: relative;
        }

        .glitch::before,
        .glitch::after {
            content: attr(data-text);
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            opacity: 0.8;
        }

        .glitch::before {
            color: #ff00ff;
            animation: glitch-offset 0.15s infinite alternate;
            clip-path: inset(20% 0 60% 0);
        }

        .glitch::after {
            color: #00ffff;
            animation: glitch-offset2 0.2s infinite alternate;
            clip-path: inset(60% 0 10% 0);
        }

        @keyframes glitch-offset {
            0% { transform: translate(-3px, 2px); }
            100% { transform: translate(3px, -2px); }
        }

        @keyframes glitch-offset2 {
            0% { transform: translate(2px, -3px); }
            100% { transform: translate(-2px, 3px); }
        }

        @keyframes glitch-anim {
            0% { text-shadow: 3px 0 red, -3px 0 blue, 0 0 30px #00ff41; }
            25% { text-shadow: -3px 0 cyan, 3px 0 magenta, 0 0 50px #00ff41; }
            50% { text-shadow: 4px 0 lime, -4px 0 purple, 0 0 70px #00ff41; }
            75% { text-shadow: -4px 0 orange, 4px 0 teal, 0 0 50px #00ff41; }
            100% { text-shadow: 3px 0 red, -3px 0 blue, 0 0 30px #00ff41; }
        }

        .terminal-box {
            background: #0d0d0d;
            border: 1px solid #00ff41;
            padding: 1.2rem;
            margin: 1.5rem 0;
            text-align: left;
            font-size: 0.85rem;
            height: 220px;
            overflow-y: hidden;
            direction: ltr;
            box-shadow: inset 0 0 60px rgba(0, 255, 65, 0.1);
            border-radius: 8px;
            position: relative;
            background: linear-gradient(180deg, #0a0a0a 0%, #0d0d0d 100%);
        }

        .terminal-line {
            color: #00ff41;
            opacity: 0.9;
            line-height: 1.8;
            white-space: nowrap;
            overflow: hidden;
            border-right: 2px solid #00ff41;
            animation: blink-cursor 0.7s step-end infinite;
            padding-right: 5px;
            font-size: 0.8rem;
        }

        .terminal-line.error {
            color: #ff3333;
            border-color: #ff3333;
        }

        .terminal-line.success {
            color: #00ff88;
            border-color: #00ff88;
        }

        .terminal-line.warning {
            color: #ffaa00;
            border-color: #ffaa00;
        }

        .progress-container {
            width: 100%;
            background: #1a1a1a;
            border: 1px solid #00ff41;
            margin: 12px 0;
            border-radius: 6px;
            overflow: hidden;
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.1);
        }

        .progress-bar {
            width: 0%;
            height: 28px;
            background: linear-gradient(90deg, #00ff41, #00ff88, #00ff41);
            text-align: center;
            line-height: 28px;
            color: #000;
            font-weight: bold;
            font-size: 0.85rem;
            box-shadow: 0 0 40px #00ff41;
            transition: width 0.1s ease;
            background-size: 200% 100%;
            animation: progressGradient 2s linear infinite;
        }

        @keyframes progressGradient {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }

        .stats-container {
            display: flex;
            gap: 20px;
            justify-content: center;
            flex-wrap: wrap;
            margin: 15px 0;
        }

        .stat-box {
            border: 1px solid #00ff41;
            padding: 12px 25px;
            border-radius: 6px;
            background: #111;
            min-width: 130px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.05);
            transition: all 0.3s;
        }

        .stat-box::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(0, 255, 65, 0.1) 0%, transparent 70%);
            animation: statGlow 3s infinite alternate;
        }

        @keyframes statGlow {
            0% { transform: translate(-10%, -10%); }
            100% { transform: translate(10%, 10%); }
        }

        .stat-label {
            color: #888;
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            position: relative;
            z-index: 1;
        }

        .stat-value {
            font-size: 2.2rem;
            font-weight: bold;
            color: #00ff41;
            text-shadow: 0 0 30px #00ff41;
            position: relative;
            z-index: 1;
        }

        .stat-value.danger {
            color: #ff3333;
            text-shadow: 0 0 30px #ff3333;
            animation: dangerPulse 0.5s infinite alternate;
        }

        @keyframes dangerPulse {
            0% { opacity: 0.7; }
            100% { opacity: 1; }
        }

        .hacker-icon {
            font-size: 5rem;
            margin-bottom: 5px;
            filter: drop-shadow(0 0 40px #00ff41);
            animation: pulse 1.5s infinite;
            display: block;
        }

        @keyframes pulse {
            0% { transform: scale(1) rotate(0deg); opacity: 0.7; filter: drop-shadow(0 0 20px #00ff41); }
            50% { transform: scale(1.2) rotate(5deg); opacity: 1; filter: drop-shadow(0 0 60px #00ff41); }
            100% { transform: scale(1) rotate(0deg); opacity: 0.7; filter: drop-shadow(0 0 20px #00ff41); }
        }

        @keyframes blink-cursor {
            0%, 100% { border-color: transparent; }
            50% { border-color: #00ff41; }
        }

        .vibrate {
            animation: vibrate 0.06s infinite alternate;
        }

        @keyframes vibrate {
            0% { transform: translateX(-4px) translateY(2px) rotate(-1deg); }
            100% { transform: translateX(4px) translateY(-2px) rotate(1deg); }
        }

        .status-message {
            font-size: 0.9rem;
            opacity: 0.9;
            margin-top: 8px;
            letter-spacing: 2px;
            min-height: 25px;
            color: #00ff41;
            font-weight: bold;
            text-shadow: 0 0 20px rgba(0, 255, 65, 0.3);
        }

        .fake-btn {
            display: inline-block;
            background: transparent;
            border: 1px solid #00ff41;
            color: #00ff41;
            padding: 10px 30px;
            margin-top: 12px;
            border-radius: 4px;
            font-family: inherit;
            font-size: 0.85rem;
            letter-spacing: 4px;
            cursor: pointer;
            transition: 0.3s;
            box-shadow: 0 0 30px rgba(0, 255, 65, 0.1);
            text-transform: uppercase;
            position: relative;
            overflow: hidden;
        }

        .fake-btn::after {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(0, 255, 65, 0.2) 0%, transparent 70%);
            animation: btnPulse 2s infinite;
        }

        @keyframes btnPulse {
            0% { transform: scale(1); opacity: 0.5; }
            50% { transform: scale(1.5); opacity: 0; }
            100% { transform: scale(1); opacity: 0.5; }
        }

        .fake-btn:hover {
            background: #00ff41;
            color: #000;
            box-shadow: 0 0 70px #00ff41;
        }

        .hack-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 999;
            background: rgba(0, 0, 0, 0.95);
            display: none;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            color: #00ff41;
            font-family: 'Courier New', monospace;
            animation: fadeIn 0.5s;
        }

        .hack-overlay.show {
            display: flex;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .hack-overlay h1 {
            font-size: 4rem;
            text-shadow: 0 0 60px #00ff41;
            animation: glitch-anim 0.5s infinite;
        }

        .hack-overlay p {
            font-size: 1.5rem;
            margin-top: 20px;
            letter-spacing: 10px;
        }

        @media (max-width: 600px) {
            .glitch { font-size: 1.8rem; letter-spacing: 3px; }
            .overlay-content { padding: 1rem; width: 98%; }
            .terminal-box { height: 150px; font-size: 0.7rem; }
            .stat-value { font-size: 1.5rem; }
            .stat-box { padding: 8px 15px; min-width: 80px; }
            .hacker-icon { font-size: 3.5rem; }
            .hack-overlay h1 { font-size: 2rem; }
            .hack-overlay p { font-size: 1rem; }
        }
    </style>
</head>
<body>
    <canvas id="matrix-canvas"></canvas>
    <div class="glitch-bg"></div>

    <div class="overlay-content" id="mainContent">
        <div class="hacker-icon">&#9760;</div>
        <h1 class="glitch" data-text="&#x25CF; SYSTEM BREACH &#x25CF;">&#x25CF; SYSTEM BREACH &#x25CF;</h1>
        <p style="color: #00cc33; margin-bottom: 8px; letter-spacing: 4px; font-size: 0.9rem;">
            &gt; ACCESS GRANTED &lt;
        </p>

        <div class="terminal-box" id="terminal">
            <div class="terminal-line" id="line1">[INIT] تحميل وحدات الاختراق...</div>
            <div class="terminal-line" id="line2">[SCAN] جلب بيانات الهدف...</div>
            <div class="terminal-line" id="line3">[CRACK] كسر التشفير 256-bit...</div>
            <div class="terminal-line" id="line4">[ROOT] الوصول إلى الجذر مكتمل.</div>
        </div>

        <div class="stats-container">
            <div class="stat-box">
                <div class="stat-label">المنافذ المخترقة</div>
                <div class="stat-value" id="portCount">0</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">الحزم المرسلة</div>
                <div class="stat-value" id="packetCount">0</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">الخوادم المسيطرة</div>
                <div class="stat-value" id="serverCount">0</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">الأنظمة المخترقة</div>
                <div class="stat-value danger" id="systemCount">0</div>
            </div>
        </div>

        <div class="progress-container">
            <div class="progress-bar" id="progressBar">0%</div>
        </div>

        <div class="status-message" id="statusMessage">[حالة] جاري تجاوز الجدران النارية...</div>

        <div class="fake-btn" id="hackBtn">&#x25B6; تنفيذ الهجوم</div>
    </div>

    <div class="hack-overlay" id="hackOverlay">
        <h1>&#x25CF; SYSTEM COMPROMISED &#x25CF;</h1>
        <p>&gt; ACCESS GRANTED &lt;</p>
        <div style="margin-top: 30px; font-size: 0.8rem; opacity: 0.7;">
            [جميع الأنظمة تحت السيطرة]
        </div>
    </div>

    <script>
        // Matrix Effect
        const canvas = document.getElementById('matrix-canvas');
        const ctx = canvas.getContext('2d');
        let width = canvas.width = window.innerWidth;
        let height = canvas.height = window.innerHeight;
        const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789@#$%^&*()*&^%+-/~{[|`]}";
        const columns = Math.floor(width / 16) + 1;
        let drops = [];
        for (let x = 0; x < columns; x++) {
            drops[x] = Math.random() * -150;
        }

        function drawMatrix() {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.04)';
            ctx.fillRect(0, 0, width, height);
            const colors = ['#0F0', '#0F8', '#0FF', '#0F0'];
            ctx.fillStyle = colors[Math.floor(Math.random() * colors.length)];
            ctx.font = '15px monospace';
            for (let i = 0; i < drops.length; i++) {
                const text = chars.charAt(Math.floor(Math.random() * chars.length));
                ctx.fillText(text, i * 16, drops[i] * 16);
                if (drops[i] * 16 > height && Math.random() > 0.975) {
                    drops[i] = 0;
                }
                drops[i]++;
            }
            requestAnimationFrame(drawMatrix);
        }
        drawMatrix();

        window.addEventListener('resize', () => {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
        });

        // Terminal Simulation
        const terminalMessages = [
            { text: "[INFO] تهيئة قنوات الاتصال المشفرة...", class: "" },
            { text: "[WARN] اكتشاف جدار ناري نشط... تجاوز...", class: "warning" },
            { text: "[SUCCESS] حقن الحمولة في الذاكرة المؤقتة.", class: "success" },
            { text: "[ROOT] تم رفع الصلاحيات إلى SYSTEM.", class: "success" },
            { text: "[DATA] تنزيل قاعدة البيانات المستهدفة... 78%", class: "" },
            { text: "[SEC] تعطيل أنظمة الإنذار.", class: "warning" },
            { text: "[DONE] السيطرة الكاملة على الخادم.", class: "success" },
            { text: "[SCAN] اكتشاف منافذ جديدة...", class: "" },
            { text: "[EXPLOIT] استغلال ثغرة يوم الصفر.", class: "error" },
            { text: "[PROXY] توجيه الاتصال عبر 5 خوادم وسيطة.", class: "" },
            { text: "[CRYPTO] فك تشفير المفاتيح الخاصة.", class: "success" },
            { text: "[LOG] مسح سجلات الدخول.", class: "warning" },
            { text: "[ALERT] نظام الدفاع يحاول الرد... تم قمع الإشارة.", class: "error" },
            { text: "[KERNEL] اختراق النواة...", class: "error" },
            { text: "[MEM] حقن الكود في الذاكرة...", class: "warning" },
        ];

        const lineElements = [
            document.getElementById('line1'),
            document.getElementById('line2'),
            document.getElementById('line3'),
            document.getElementById('line4')
        ];

        setInterval(() => {
            const randomMsg = terminalMessages[Math.floor(Math.random() * terminalMessages.length)];
            const randomIndex = Math.floor(Math.random() * lineElements.length);
            lineElements[randomIndex].textContent = randomMsg.text;
            lineElements[randomIndex].className = 'terminal-line ' + randomMsg.class;
            lineElements[randomIndex].style.animation = 'none';
            setTimeout(() => {
                lineElements[randomIndex].style.animation = 'blink-cursor 0.7s step-end infinite';
            }, 10);
        }, 1500);

        // Hack Logic
        let port = 0, packets = 0, servers = 0, systems = 0, progress = 0, hackActive = false;
        const portEl = document.getElementById('portCount');
        const packetEl = document.getElementById('packetCount');
        const serverEl = document.getElementById('serverCount');
        const systemEl = document.getElementById('systemCount');
        const progressBar = document.getElementById('progressBar');
        const statusMsg = document.getElementById('statusMessage');
        const overlay = document.querySelector('.overlay-content');
        const hackOverlay = document.getElementById('hackOverlay');
        const hackBtn = document.getElementById('hackBtn');

        const statusPhrases = [
            '[حالة] جاري اختراق الطبقات الدفاعية...',
            '[حالة] تجاوز جدار الحماية الرئيسي...',
            '[حالة] زرع باب خلفي في النظام...',
            '[حالة] رفع الصلاحيات إلى المدير...',
            '[حالة] تنزيل البيانات الحساسة...',
            '[حالة] تعطيل نظام الإنذار...',
            '[حالة] اختراق كامل. النظام تحت السيطرة.'
        ];

        const updateInterval = setInterval(() => {
            if (!hackActive) return;

            port += Math.floor(Math.random() * 6) + 2;
            packets += Math.floor(Math.random() * 20) + 10;
            servers += Math.floor(Math.random() * 3);
            systems += Math.floor(Math.random() * 2);
            progress = Math.min(100, progress + (Math.random() * 3.5));

            portEl.textContent = port;
            packetEl.textContent = packets;
            serverEl.textContent = servers;
            systemEl.textContent = systems;
            progressBar.style.width = progress + '%';
            progressBar.textContent = Math.floor(progress) + '%';

            if (progress >= 100) {
                statusMsg.innerHTML = '[حالة] ⚡ اختراق كامل. النظام تحت السيطرة.';
                statusMsg.style.color = '#ff3333';
                overlay.classList.add('vibrate');
                setTimeout(() => {
                    hackOverlay.classList.add('show');
                    setTimeout(() => {
                        hackOverlay.classList.remove('show');
                        resetHack();
                    }, 5000);
                }, 500);

                if (progress < 105) {
                    document.body.style.animation = 'vibrate 0.05s infinite alternate';
                    setTimeout(() => {
                        document.body.style.animation = '';
                    }, 2000);
                }
            } else if (progress > 75) {
                statusMsg.textContent = '[حالة] اختراق متقدم... تجاوز الدفاعات الأخيرة.';
                statusMsg.style.color = '#ffaa00';
            } else if (progress > 45) {
                statusMsg.textContent = '[حالة] اختراق الطبقات الداخلية...';
                statusMsg.style.color = '#ffcc00';
            } else {
                statusMsg.textContent = '[حالة] جاري اختراق الطبقات الدفاعية...';
                statusMsg.style.color = '#00ff41';
            }

            if (Math.random() > 0.7) {
                const randomStatus = statusPhrases[Math.floor(Math.random() * statusPhrases.length)];
                if (progress < 100) {
                    statusMsg.textContent = randomStatus;
                }
            }
        }, 250);

        // Titles
        const titles = ['!ACCESS', '!BREACH', '!ROOT', '!HACKED', '!ZERO_DAY', '!OVERRIDE', '!SYSTEM_DOWN'];
        setInterval(() => {
            if (hackActive) {
                const newTitle = titles[Math.floor(Math.random() * titles.length)] + ' | ' + String(Math.floor(Math.random() * 9999)).padStart(4, '0');
                document.title = newTitle;
                setTimeout(() => {
                    document.title = 'نظام الاختراق المتقدم';
                }, 800);
            }
        }, 2500);

        // Flash effects
        setInterval(() => {
            if (hackActive && Math.random() > 0.85) {
                const flash = document.createElement('div');
                flash.style.cssText = `
                    position: fixed;
                    top: 0; left: 0;
                    width: 100%; height: 100%;
                    background: #00ff41;
                    opacity: 0.1;
                    z-index: 999;
                    pointer-events: none;
                    transition: opacity 0.05s;
                `;
                document.body.appendChild(flash);
                setTimeout(() => {
                    flash.style.opacity = '0';
                    setTimeout(() => {
                        flash.remove();
                    }, 100);
                }, 50);
            }
        }, 1500);

        // Console message
        console.log('%c◼ SYSTEM BREACHED ◼', 'color: #00ff41; font-size: 22px; font-weight: bold;');
        console.log('%cالظل المبرمج في خدمتك.', 'color: #00ff41; font-size: 16px;');
        console.log('%cجميع الأنظمة تحت السيطرة.', 'color: #888; font-size: 14px;');
        console.log('%cتم تفعيل وضع الهجوم الشامل.', 'color: #ff3333; font-size: 14px;');

        // Typewriter effect
        (function typeWriterEffect() {
            const terminalBox = document.getElementById('terminal');
            const systemLines = [
                '[SYSTEM] تهيئة البيئة...',
                '[SYSTEM] تحميل وحدات الهجوم...',
                '[SYSTEM] جاهزية كاملة.',
                '[SYSTEM] في انتظار أمر المستخدم.'
            ];
            systemLines.forEach((line, index) => {
                setTimeout(() => {
                    const newLine = document.createElement('div');
                    newLine.className = 'terminal-line success';
                    newLine.style.borderRight = 'none';
                    newLine.style.animation = 'none';
                    newLine.textContent = line;
                    terminalBox.prepend(newLine);
                }, index * 600);
            });
        })();

        // Hack button
        hackBtn.addEventListener('click', function() {
            if (!hackActive) {
                hackActive = true;
                this.textContent = '⏳ جاري الهجوم...';
                this.style.borderColor = '#ff3333';
                this.style.color = '#ff3333';
                this.style.boxShadow = '0 0 60px rgba(255, 51, 51, 0.3)';
                statusMsg.textContent = '[حالة] بدء الهجوم الشامل...';
                statusMsg.style.color = '#ff3333';
                port = 0; packets = 0; servers = 0; systems = 0; progress = 0;
                portEl.textContent = '0';
                packetEl.textContent = '0';
                serverEl.textContent = '0';
                systemEl.textContent = '0';
                progressBar.style.width = '0%';
                progressBar.textContent = '0%';
                overlay.classList.remove('vibrate');
                document.body.style.animation = '';
                
                // Play sound
                try {
                    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                    const oscillator = audioCtx.createOscillator();
                    const gainNode = audioCtx.createGain();
                    oscillator.connect(gainNode);
                    gainNode.connect(audioCtx.destination);
                    oscillator.type = 'sawtooth';
                    oscillator.frequency.setValueAtTime(200, audioCtx.currentTime);
                    oscillator.frequency.exponentialRampToValueAtTime(800, audioCtx.currentTime + 0.3);
                    gainNode.gain.setValueAtTime(0.3, audioCtx.currentTime);
                    gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.3);
                    oscillator.start(audioCtx.currentTime);
                    oscillator.stop(audioCtx.currentTime + 0.3);
                } catch(e) {}
            }
        });

        function resetHack() {
            hackActive = false;
            hackBtn.textContent = '▶ تنفيذ الهجوم';
            hackBtn.style.borderColor = '#00ff41';
            hackBtn.style.color = '#00ff41';
            hackBtn.style.boxShadow = '0 0 30px rgba(0, 255, 65, 0.1)';
            statusMsg.textContent = '[حالة] جاهز لتنفيذ هجوم جديد.';
            statusMsg.style.color = '#00ff41';
            overlay.classList.remove('vibrate');
            document.body.style.animation = '';
            setTimeout(() => {
                port = 0; packets = 0; servers = 0; systems = 0; progress = 0;
                portEl.textContent = '0';
                packetEl.textContent = '0';
                serverEl.textContent = '0';
                systemEl.textContent = '0';
                progressBar.style.width = '0%';
                progressBar.textContent = '0%';
            }, 1000);
        }

        // Floating texts
        setInterval(() => {
            if (hackActive && Math.random() > 0.9) {
                const floatText = document.createElement('div');
                const texts = ['!ACCESS', '!BREACH', '!ROOT', '!HACKED', '!SYSTEM', '!OVERRIDE'];
                floatText.textContent = texts[Math.floor(Math.random() * texts.length)];
                floatText.style.cssText = `
                    position: fixed;
                    color: #00ff41;
                    font-size: ${Math.random() * 2 + 1}rem;
                    font-weight: bold;
                    opacity: ${Math.random() * 0.3 + 0.1};
                    z-index: 5;
                    pointer-events: none;
                    left: ${Math.random() * 90}%;
                    top: ${Math.random() * 90}%;
                    transform: rotate(${Math.random() * 60 - 30}deg);
                    text-shadow: 0 0 20px #00ff41;
                    animation: fadeOut 2s forwards;
                `;
                document.body.appendChild(floatText);
                const style = document.createElement('style');
                style.textContent = `
                    @keyframes fadeOut {
                        0% { opacity: ${Math.random() * 0.3 + 0.1}; transform: scale(1) rotate(${Math.random() * 60 - 30}deg); }
                        100% { opacity: 0; transform: scale(2) rotate(${Math.random() * 60 - 30 + 20}deg); }
                    }
                `;
                document.head.appendChild(style);
                setTimeout(() => {
                    floatText.remove();
                    style.remove();
                }, 2500);
            }
        }, 3000);
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
