from http.server import HTTPServer, BaseHTTPRequestHandler
import os

# ===== خادم موقع عبود لتعليم البرمجة =====
class AboodHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.end_headers()
            html = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>عبود | تعليم البرمجة</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, sans-serif;
            background: #0f0f1a;
            min-height: 100vh;
            background-image: radial-gradient(circle at 20% 30%, rgba(40, 70, 150, 0.2), transparent 60%),
                              radial-gradient(circle at 80% 70%, rgba(150, 40, 100, 0.15), transparent 50%);
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        
        .header {
            display: flex; justify-content: space-between; align-items: center;
            padding: 20px 0; border-bottom: 1px solid rgba(255,255,255,0.06);
            flex-wrap: wrap; gap: 15px;
        }
        .logo {
            font-size: 32px; font-weight: 900;
            background: linear-gradient(135deg, #00d2ff, #3a7bd5);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .logo i { -webkit-text-fill-color: initial; color: #00d2ff; margin-left: 10px; }
        .nav-links {
            display: flex; gap: 30px; list-style: none; font-weight: 600;
            color: #b0baca; flex-wrap: wrap;
        }
        .nav-links a { color: #b0baca; text-decoration: none; transition: 0.3s; }
        .nav-links a:hover { color: #00d2ff; }
        .btn {
            padding: 12px 28px; border: none; border-radius: 40px; font-weight: 700;
            cursor: pointer; transition: 0.3s; text-decoration: none; display: inline-flex;
            align-items: center; gap: 8px; font-size: 15px;
        }
        .btn-primary {
            background: linear-gradient(135deg, #00d2ff, #3a7bd5);
            color: #fff;
        }
        .btn-primary:hover { transform: scale(1.04); box-shadow: 0 8px 30px rgba(0,210,255,0.3); }
        .btn-outline {
            background: transparent; border: 1.5px solid #00d2ff; color: #00d2ff;
        }
        .btn-outline:hover { background: #00d2ff; color: #0f0f1a; }
        
        .hero {
            text-align: center; padding: 60px 0 40px;
        }
        .hero h1 {
            font-size: 52px; font-weight: 900; color: #fff;
        }
        .hero h1 span {
            background: linear-gradient(135deg, #00d2ff, #3a7bd5);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .hero p {
            color: #8d99b6; font-size: 20px; max-width: 600px; margin: 15px auto 35px;
        }
        
        .courses-grid {
            display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 30px; margin: 40px 0;
        }
        .course-card {
            background: rgba(255,255,255,0.04);
            border-radius: 24px; padding: 28px 22px;
            border: 1px solid rgba(255,255,255,0.06);
            transition: 0.4s; backdrop-filter: blur(4px);
        }
        .course-card:hover {
            transform: translateY(-8px);
            border-color: rgba(0,210,255,0.2);
            box-shadow: 0 20px 40px rgba(0,0,0,0.5);
        }
        .course-tag {
            display: inline-block; background: rgba(0,210,255,0.15);
            color: #00d2ff; font-size: 13px; font-weight: 700;
            padding: 4px 16px; border-radius: 40px; margin-bottom: 14px;
        }
        .course-card h3 { color: #fff; font-size: 22px; margin-bottom: 8px; }
        .course-meta {
            display: flex; gap: 15px; color: #8d99b6; font-size: 14px; margin: 10px 0;
        }
        .course-meta i { color: #00d2ff; margin-left: 5px; }
        .course-card p { color: #b0baca; font-size: 15px; line-height: 1.6; margin-bottom: 18px; }
        .course-card .btn { width: 100%; justify-content: center; }
        
        .footer {
            text-align: center; padding: 30px 0 20px;
            border-top: 1px solid rgba(255,255,255,0.05);
            color: #6b7a98; margin-top: 20px;
        }
        .footer a { color: #8d99b6; text-decoration: none; margin: 0 12px; }
        .footer a:hover { color: #00d2ff; }
        
        @media (max-width: 768px) {
            .header { flex-direction: column; align-items: stretch; gap: 10px; }
            .nav-links { justify-content: center; gap: 16px; }
            .hero h1 { font-size: 32px; }
            .hero p { font-size: 17px; }
        }
    </style>
</head>
<body>
<div class="container">
    <header class="header">
        <div class="logo"><i class="fas fa-code"></i> عبود</div>
        <ul class="nav-links">
            <li><a href="#">الرئيسية</a></li>
            <li><a href="#">الدورات</a></li>
            <li><a href="#">المسارات</a></li>
            <li><a href="#">من نحن</a></li>
            <li><a href="#">تواصل</a></li>
        </ul>
        <div style="display:flex; gap:12px; flex-wrap:wrap;">
            <a href="#" class="btn btn-outline"><i class="fas fa-user"></i> تسجيل الدخول</a>
            <a href="#" class="btn btn-primary"><i class="fas fa-rocket"></i> انضمام</a>
        </div>
    </header>

    <section class="hero">
        <h1>تعلم البرمجة مع <span>عبود</span></h1>
        <p>دروس تفاعلية، مشاريع تطبيقية، ومسارات احترافية للمبتدئين والمحترفين</p>
        <a href="#" class="btn btn-primary" style="font-size:18px; padding:14px 40px;">
            <i class="fas fa-play"></i> ابدأ الآن مجاناً
        </a>
    </section>

    <div class="courses-grid">
        <div class="course-card">
            <span class="course-tag"><i class="fas fa-code"></i> أساسيات</span>
            <h3>مقدمة في البرمجة</h3>
            <div class="course-meta">
                <span><i class="fas fa-clock"></i> ٦ أسابيع</span>
                <span><i class="fas fa-users"></i> مبتدئ</span>
            </div>
            <p>تعلم الأساسيات من الصفر بلغة بايثون بأسلوب مبسط وممتع.</p>
            <a href="#" class="btn btn-primary"><i class="fas fa-external-link-alt"></i> ابدأ التعلم</a>
        </div>
        <div class="course-card">
            <span class="course-tag"><i class="fas fa-globe"></i> ويب</span>
            <h3>تطوير الويب</h3>
            <div class="course-meta">
                <span><i class="fas fa-clock"></i> ٨ أسابيع</span>
                <span><i class="fas fa-users"></i> متوسط</span>
            </div>
            <p>تعلم HTML, CSS, JavaScript وبناء مواقع تفاعلية احترافية.</p>
            <a href="#" class="btn btn-primary"><i class="fas fa-external-link-alt"></i> ابدأ التعلم</a>
        </div>
        <div class="course-card">
            <span class="course-tag"><i class="fas fa-robot"></i> ذكاء</span>
            <h3>الذكاء الاصطناعي</h3>
            <div class="course-meta">
                <span><i class="fas fa-clock"></i> ١٠ أسابيع</span>
                <span><i class="fas fa-users"></i> متقدم</span>
            </div>
            <p>استكشف عالم الذكاء الاصطناعي وابنِ مشاريعك الذكية.</p>
            <a href="#" class="btn btn-primary"><i class="fas fa-external-link-alt"></i> ابدأ التعلم</a>
        </div>
        <div class="course-card">
            <span class="course-tag"><i class="fas fa-mobile-alt"></i> تطبيقات</span>
            <h3>برمجة التطبيقات</h3>
            <div class="course-meta">
                <span><i class="fas fa-clock"></i> ٧ أسابيع</span>
                <span><i class="fas fa-users"></i> متوسط</span>
            </div>
            <p>صمم وطور تطبيقات أندرويد وiOS باستخدام أدوات حديثة.</p>
            <a href="#" class="btn btn-primary"><i class="fas fa-external-link-alt"></i> ابدأ التعلم</a>
        </div>
    </div>

    <footer class="footer">
        <div>
            <a href="#"><i class="fab fa-facebook-f"></i></a>
            <a href="#"><i class="fab fa-twitter"></i></a>
            <a href="#"><i class="fab fa-instagram"></i></a>
            <a href="#"><i class="fab fa-youtube"></i></a>
        </div>
        <p style="margin-top:15px;">&copy; 2026 عبود لتعليم البرمجة. جميع الحقوق محفوظة.</p>
    </footer>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/js/all.min.js"></script>
<script>
    document.querySelectorAll('.course-card .btn-primary').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const course = this.closest('.course-card').querySelector('h3').innerText;
            alert(`سيتم توجيهك إلى دورة: "${course}"\n(ضع رابط الدورة الفعلي هنا)`);
        });
    });
</script>
</body>
</html>"""
            self.wfile.write(html.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        self.send_response(404)
        self.end_headers()

    def log_message(self, format, *args):
        return

# ===== تشغيل الخادم =====
def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), AboodHandler)
    print(f"[✓] موقع عبود لتعليم البرمجة يعمل على المنفذ {port}")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
