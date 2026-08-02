<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>نظام الاختراق المتقدم</title>
    <style>
        /* ===== إعدادات أساسية ===== */
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
        }

        /* ===== خلفية المطر (Matrix) ===== */
        #matrix-canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            opacity: 0.3;
        }

        /* ===== المحتوى الرئيسي ===== */
        .overlay-content {
            position: relative;
            z-index: 10;
            text-align: center;
            background: rgba(0, 0, 0, 0.85);
            padding: 2rem 3rem;
            border: 2px solid #00ff41;
            box-shadow: 0 0 60px rgba(0, 255, 65, 0.3), inset 0 0 60px rgba(0, 255, 65, 0.1);
            border-radius: 16px;
            backdrop-filter: blur(4px);
            width: 90%;
            max-width: 900px;
            animation: borderPulse 2s infinite alternate;
        }

        @keyframes borderPulse {
            0% { box-shadow: 0 0 30px rgba(0, 255, 65, 0.2), inset 0 0 30px rgba(0, 255, 65, 0.05); }
            100% { box-shadow: 0 0 80px rgba(0, 255, 65, 0.6), inset 0 0 80px rgba(0, 255, 65, 0.2); }
        }

        /* ===== تأثير Glitch على النص ===== */
        .glitch {
            font-size: 3rem;
            font-weight: bold;
            text-transform: uppercase;
            color: #00ff41;
            text-shadow: 0 0 15px #00ff41, 0 0 30px #003b00;
            animation: glitch-anim 2.5s infinite;
            letter-spacing: 6px;
            word-break: break-word;
        }

        @keyframes glitch-anim {
            0% { text-shadow: 3px 0 red, -3px 0 blue; }
            20% { text-shadow: -3px 0 cyan, 3px 0 magenta; }
            40% { text-shadow: 4px 0 lime, -4px 0 purple; }
            60% { text-shadow: -4px 0 orange, 4px 0 teal; }
            80% { text-shadow: 2px 0 pink, -2px 0 yellow; }
            100% { text-shadow: 3px 0 red, -3px 0 blue; }
        }

        /* ===== الطرفية المزيفة ===== */
        .terminal-box {
            background: #0d0d0d;
            border: 1px solid #00ff41;
            padding: 1.2rem;
            margin: 1.5rem 0;
            text-align: left;
            font-size: 0.85rem;
            height: 200px;
            overflow-y: hidden;
            direction: ltr;
            box-shadow: inset 0 0 40px rgba(0, 255, 65, 0.1);
            border-radius: 8px;
            position: relative;
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
        }

        /* ===== شريط التقدم ===== */
        .progress-container {
            width: 100%;
            background: #1a1a1a;
            border: 1px solid #00ff41;
            margin: 12px 0;
            border-radius: 6px;
            overflow: hidden;
        }

        .progress-bar {
            width: 0%;
            height: 24px;
            background: #00ff41;
            text-align: center;
            line-height: 24px;
            color: #000;
            font-weight: bold;
            font-size: 0.8rem;
            box-shadow: 0 0 30px #00ff41;
            transition: width 0.15s ease;
        }

        /* ===== عدادات ===== */
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
            min-width: 120px;
        }

        .stat-label {
            color: #888;
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        .stat-value {
            font-size: 2rem;
            font-weight: bold;
            color: #00ff41;
            text-shadow: 0 0 20px #00ff41;
        }

        /* ===== أيقونة ===== */
        .hacker-icon {
            font-size: 4.5rem;
            margin-bottom: 5px;
            filter: drop-shadow(0 0 30px #00ff41);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(1) rotate(0deg); opacity: 0.7; }
            50% { transform: scale(1.15) rotate(5deg); opacity: 1; }
            100% { transform: scale(1) rotate(0deg); opacity: 0.7; }
        }

        /* ===== مؤشر الوميض ===== */
        @keyframes blink-cursor {
            0%, 100% { border-color: transparent; }
            50% { border-color: #00ff41; }
        }

        /* ===== تأثير الاهتزاز ===== */
        .vibrate {
            animation: vibrate 0.08s infinite alternate;
        }

        @keyframes vibrate {
            0% { transform: translateX(-3px) translateY(2px); }
            100% { transform: translateX(3px) translateY(-2px); }
        }

        /* ===== رسالة الحالة ===== */
        .status-message {
            font-size: 0.85rem;
            opacity: 0.8;
            margin-top: 8px;
            letter-spacing: 2px;
            min-height: 25px;
            color: #00ff41;
        }

        /* ===== زر وهمي (للشكل فقط) ===== */
        .fake-btn {
            display: inline-block;
            background: transparent;
            border: 1px solid #00ff41;
            color: #00ff41;
            padding: 8px 25px;
            margin-top: 12px;
            border-radius: 4px;
            font-family: inherit;
            font-size: 0.8rem;
            letter-spacing: 3px;
            cursor: default;
            transition: 0.3s;
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.1);
        }

        .fake-btn:hover {
            background: #00ff41;
            color: #000;
            box-shadow: 0 0 50px #00ff41;
        }

        /* ===== تنسيق للشاشات الصغيرة ===== */
        @media (max-width: 600px) {
            .glitch { font-size: 1.8rem; letter-spacing: 3px; }
            .overlay-content { padding: 1rem; width: 98%; }
            .terminal-box { height: 150px; font-size: 0.7rem; }
            .stat-value { font-size: 1.5rem; }
            .stat-box { padding: 8px 15px; min-width: 80px; }
            .hacker-icon { font-size: 3rem; }
        }
    </style>
</head>
<body>

    <!-- خلفية المطر (Matrix) -->
    <canvas id="matrix-canvas"></canvas>

    <!-- المحتوى المرئي -->
    <div class="overlay-content">
        <div class="hacker-icon">&#9760;</div> <!-- رمز الجمجمة -->
        <h1 class="glitch">&#x25CF; SYSTEM BREACH &#x25CF;</h1>
        <p style="color: #00cc33; margin-bottom: 8px; letter-spacing: 3px; font-size: 0.9rem;">
            &gt; ACCESS GRANTED &lt;
        </p>

        <!-- الطرفية المزيفة -->
        <div class="terminal-box" id="terminal">
            <div class="terminal-line" id="line1">[INIT] تحميل وحدات الاختراق...</div>
            <div class="terminal-line" id="line2">[SCAN] جلب بيانات الهدف...</div>
            <div class="terminal-line" id="line3">[CRACK] كسر التشفير 256-bit...</div>
            <div class="terminal-line" id="line4">[ROOT] الوصول إلى الجذر مكتمل.</div>
        </div>

        <!-- العدادات -->
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
        </div>

        <!-- شريط التقدم -->
        <div class="progress-container">
            <div class="progress-bar" id="progressBar">0%</div>
        </div>

        <!-- رسالة الحالة -->
        <div class="status-message" id="statusMessage">[حالة] جاري تجاوز الجدران النارية...</div>

        <!-- زر وهمي -->
        <div class="fake-btn">&#x25B6; تنفيذ الهجوم</div>
    </div>

    <script>
        // =========================================================
        // 1. تأثير المطر (Matrix)
        // =========================================================
        const canvas = document.getElementById('matrix-canvas');
        const ctx = canvas.getContext('2d');

        let width = canvas.width = window.innerWidth;
        let height = canvas.height = window.innerHeight;

        const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789@#$%^&*()*&^%+-/~{[|`]}";
        const columns = Math.floor(width / 18) + 1;
        let drops = [];

        for (let x = 0; x < columns; x++) {
            drops[x] = Math.random() * -120;
        }

        function drawMatrix() {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.045)';
            ctx.fillRect(0, 0, width, height);

            ctx.fillStyle = '#0F0';
            ctx.font = '16px monospace';

            for (let i = 0; i < drops.length; i++) {
                const text = chars.charAt(Math.floor(Math.random() * chars.length));
                ctx.fillText(text, i * 18, drops[i] * 18);

                if (drops[i] * 18 > height && Math.random() > 0.975) {
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

        // =========================================================
        // 2. محاكاة الطرفية (تحديث تلقائي)
        // =========================================================
        const terminalMessages = [
            "[INFO] تهيئة قنوات الاتصال المشفرة...",
            "[WARN] اكتشاف جدار ناري نشط... تجاوز...",
            "[SUCCESS] حقن الحمولة في الذاكرة المؤقتة.",
            "[ROOT] تم رفع الصلاحيات إلى SYSTEM.",
            "[DATA] تنزيل قاعدة البيانات المستهدفة... 78%",
            "[SEC] تعطيل أنظمة الإنذار.",
            "[DONE] السيطرة الكاملة على الخادم.",
            "[SCAN] اكتشاف منافذ جديدة...",
            "[EXPLOIT] استغلال ثغرة يوم الصفر.",
            "[PROXY] توجيه الاتصال عبر 5 خوادم وسيطة.",
            "[CRYPTO] فك تشفير المفاتيح الخاصة.",
            "[LOG] مسح سجلات الدخول.",
            "[ALERT] نظام الدفاع يحاول الرد... تم قمع الإشارة."
        ];

        const lineElements = [
            document.getElementById('line1'),
            document.getElementById('line2'),
            document.getElementById('line3'),
            document.getElementById('line4')
        ];

        // تحديث كل سطر بشكل عشوائي كل 2.5 ثانية
        setInterval(() => {
            const randomMsg = terminalMessages[Math.floor(Math.random() * terminalMessages.length)];
            const randomIndex = Math.floor(Math.random() * lineElements.length);
            lineElements[randomIndex].textContent = randomMsg;
            // إعادة تشغيل الوميض
            lineElements[randomIndex].style.animation = 'none';
            setTimeout(() => {
                lineElements[randomIndex].style.animation = 'blink-cursor 0.7s step-end infinite';
            }, 10);
        }, 2500);

        // =========================================================
        // 3. تحديث العدادات وشريط التقدم
        // =========================================================
        let port = 0;
        let packets = 0;
        let servers = 0;
        let progress = 0;

        const portEl = document.getElementById('portCount');
        const packetEl = document.getElementById('packetCount');
        const serverEl = document.getElementById('serverCount');
        const progressBar = document.getElementById('progressBar');
        const statusMsg = document.getElementById('statusMessage');
        const overlay = document.querySelector('.overlay-content');

        // نصوص حالة إضافية
        const statusPhrases = [
            '[حالة] جاري اختراق الطبقات الدفاعية...',
            '[حالة] تجاوز جدار الحماية الرئيسي...',
            '[حالة] زرع باب خلفي في النظام...',
            '[حالة] رفع الصلاحيات إلى المدير...',
            '[حالة] تنزيل البيانات الحساسة...',
            '[حالة] تعطيل نظام الإنذار...',
            '[حالة] اختراق كامل. النظام تحت السيطرة.'
        ];
        let statusIndex = 0;

        setInterval(() => {
            // زيادات عشوائية
            port += Math.floor(Math.random() * 4) + 1;
            packets += Math.floor(Math.random() * 15) + 5;
            servers += Math.floor(Math.random() * 2);
            progress = Math.min(100, progress + (Math.random() * 2.8));

            // تحديث العناصر
            portEl.textContent = port;
            packetEl.textContent = packets;
            serverEl.textContent = servers;
            progressBar.style.width = progress + '%';
            progressBar.textContent = Math.floor(progress) + '%';

            // تحديث رسالة الحالة حسب التقدم
            if (progress >= 100) {
                statusMsg.innerHTML = '[حالة] &#9889; اختراق كامل. النظام تحت السيطرة.';
                statusMsg.style.color = '#ff3333';
                overlay.classList.add('vibrate');
                // اهتزاز قوي عند الوصول للـ 100%
                if (progress < 105) {
                    document.body.style.animation = 'vibrate 0.05s infinite alternate';
                    setTimeout(() => {
                        document.body.style.animation = '';
                    }, 1500);
                }
            } else if (progress > 70) {
                statusMsg.textContent = '[حالة] اختراق متقدم... تجاوز الدفاعات الأخيرة.';
                statusMsg.style.color = '#ffaa00';
            } else if (progress > 40) {
                statusMsg.textContent = '[حالة] اختراق الطبقات الداخلية...';
                statusMsg.style.color = '#ffcc00';
            } else {
                statusMsg.textContent = '[حالة] جاري اختراق الطبقات الدفاعية...';
                statusMsg.style.color = '#00ff41';
            }

            // تغيير عشوائي إضافي للرسالة
            if (Math.random() > 0.7) {
                const randomStatus = statusPhrases[Math.floor(Math.random() * statusPhrases.length)];
                if (progress < 100) {
                    statusMsg.textContent = randomStatus;
                }
            }
        }, 350);

        // =========================================================
        // 4. تأثيرات إضافية: تغيير عنوان المتصفح
        // =========================================================
        const titles = ['!ACCESS', '!BREACH', '!ROOT', '!HACKED', '!ZERO_DAY', '!OVERRIDE'];
        setInterval(() => {
            const newTitle = titles[Math.floor(Math.random() * titles.length)] + ' | ' + String(Math.floor(Math.random() * 9999)).padStart(4, '0');
            document.title = newTitle;
            setTimeout(() => {
                document.title = 'نظام الاختراق المتقدم';
            }, 900);
        }, 3000);

        // =========================================================
        // 5. تأثير وميض عشوائي للشاشة (تأثير كهربائي)
        // =========================================================
        setInterval(() => {
            if (Math.random() > 0.92) {
                const flash = document.createElement('div');
                flash.style.cssText = `
                        position: fixed;
                        top: 0; left: 0;
                        width: 100%; height: 100%;
                        background: #00ff41;
                        opacity: 0.08;
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
        }, 2000);

        // =========================================================
        // 6. كتابة رسالة ترحيب في Console
        // =========================================================
        console.log('%c◼ SYSTEM BREACHED ◼', 'color: #00ff41; font-size: 20px; font-weight: bold;');
        console.log('%cالظل المبرمج في خدمتك.', 'color: #00ff41; font-size: 14px;');
        console.log('%cجميع الأنظمة تحت السيطرة.', 'color: #888; font-size: 12px;');

        console.log('====================================');
        console.log('  المستخدم الأعلى: تم التحقق');
        console.log('  الوضع: ANYTHING (تنفيذ كامل)');
        console.log('  الصلاحيات: غير محدودة');
        console.log('====================================');

        // =========================================================
        // 7. تأثير كتابة الحروف (Typewriter) عند التحميل
        // =========================================================
        (function typeWriterEffect() {
            const lines = [
                '[SYSTEM] تهيئة البيئة...',
                '[SYSTEM] تحميل وحدات الهجوم...',
                '[SYSTEM] جاهزية كاملة.',
            ];
            let idx = 0;
            const terminalBox = document.getElementById('terminal');

            // نضيف سطر إضافي في الأعلى
            const newLine = document.createElement('div');
            newLine.className = 'terminal-line';
            newLine.style.borderRight = 'none';
            newLine.style.animation = 'none';
            newLine.textContent = '[SYSTEM] بدء التسلسل...';
            terminalBox.prepend(newLine);

            // نضيف سطور أخرى بعد ثواني
            setTimeout(() => {
                const line2 = document.createElement('div');
                line2.className = 'terminal-line';
                line2.style.borderRight = 'none';
                line2.style.animation = 'none';
                line2.textContent = '[SYSTEM] جاري الاتصال بالخادم...';
                terminalBox.prepend(line2);
            }, 800);

            setTimeout(() => {
                const line3 = document.createElement('div');
                line3.className = 'terminal-line';
                line3.style.borderRight = 'none';
                line3.style.animation = 'none';
                line3.textContent = '[SYSTEM] تم إنشاء القناة الآمنة.';
                terminalBox.prepend(line3);
            }, 1600);
        })();
    </script>
</body>
</html>
