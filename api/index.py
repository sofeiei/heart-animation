from flask import Flask, render_template_string

app = Flask(__name__)

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ray Heart Animation</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            background-color: #000;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        canvas {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
        }
        /* ส่วนของ Footer ด้านล่าง */
        .footer {
            position: fixed;
            bottom: 30px;
            z-index: 10;
            text-align: center;
            color: #ff7597;
            font-size: 1.1rem;
            letter-spacing: 2px;
            font-weight: 300;
            text-shadow: 0 0 12px rgba(255, 34, 85, 0.6);
            animation: pulseText 2.5s infinite ease-in-out;
            pointer-events: none;
        }
        .footer span {
            font-size: 0.85rem;
            opacity: 0.7;
            display: block;
            margin-top: 5px;
            letter-spacing: 1px;
        }
        @keyframes pulseText {
            0%, 100% { opacity: 0.8; transform: scale(1); }
            50% { opacity: 1; transform: scale(1.03); text-shadow: 0 0 20px rgba(255, 34, 85, 0.9); }
        }
    </style>
</head>
<body>
    <canvas id="canvas"></canvas>

    <!-- คุณสามารถแก้ไขข้อความใน Footer ตรงนี้ได้เลย -->
    <div class="footer">
        HAPPY ANNIVERSARY 1 YEAR 🎉
    </div>

    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');

        let width = canvas.width = window.innerWidth;
        let height = canvas.height = window.innerHeight;

        window.addEventListener('resize', () => {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
            resetAnimation();
        });

        // ฟังก์ชันคำนวณพิกัดหัวใจ
        function heart1(m) {
            return 15 * Math.pow(Math.sin(m), 3);
        }

        function heart2(m) {
            return -(12 * Math.cos(m) - 5 * Math.cos(2 * m) - 2 * Math.cos(3 * m) - Math.cos(4 * m));
        }

        let i = 0;
        const maxSteps = 600;
        const scale = 16;
        let pauseTimer = 0;

        function draw() {
            const centerX = width / 2;
            const centerY = height / 2 - 20; // ยกขึ้นเล็กน้อยให้สมดุลกับ footer

            if (i <= maxSteps) {
                // วาดทีละ 3 เส้นต่อเฟรม
                for (let step = 0; step < 3; step++) {
                    if (i <= maxSteps) {
                        const targetX = centerX + heart1(i) * scale;
                        const targetY = centerY + heart2(i) * scale;

                        ctx.strokeStyle = '#ff1a3c';
                        ctx.lineWidth = 1.2;
                        ctx.shadowColor = '#ff2255';
                        ctx.shadowBlur = 8;

                        ctx.beginPath();
                        ctx.moveTo(centerX, centerY);
                        ctx.lineTo(targetX, targetY);
                        ctx.stroke();

                        i++;
                    }
                }
            } else {
                // เมื่อวาดเต็มรูปแล้ว: ให้หยุดโชว์ไว้ประมาณ 1.5 วินาที
                pauseTimer++;
                if (pauseTimer > 60) {
                    // ค่อยๆ เฟดหน้าจอให้มืดลงก่อนเริ่มรอบใหม่
                    ctx.fillStyle = 'black';
                    ctx.fillRect(0, 0, width, height);

                    // เมื่อเฟดจนครบ ให้รีเซ็ตเริ่มวาดใหม่
                    if (pauseTimer > 130) {
                        resetAnimation();
                    }
                }
            }

            requestAnimationFrame(draw);
        }

        function resetAnimation() {
            ctx.clearRect(0, 0, width, height);
            i = 0;
            pauseTimer = 0;
        }

        draw();
    </script>
</body>
</html>
"""

@app.route('/')
@app.route('/<path:path>')
def home(path=''):
    return render_template_string(HTML_CONTENT)

if __name__ == '__main__':
    app.run(debug=True)