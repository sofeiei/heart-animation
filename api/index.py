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

    <!-- ปรับแก้ข้อความที่ Footer ได้ตรงนี้ -->
    <div class="footer">
        HAPPY ANNIVERSARY 1 YEAR, MY LOVE ♥️
    </div>

    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');

        let width = canvas.width = window.innerWidth;
        let height = canvas.height = window.innerHeight;

        window.addEventListener('resize', () => {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
        });

        // คำนวณพิกัดหัวใจ
        function heart1(m) {
            return 15 * Math.pow(Math.sin(m), 3);
        }

        function heart2(m) {
            return -(12 * Math.cos(m) - 5 * Math.cos(2 * m) - 2 * Math.cos(3 * m) - Math.cos(4 * m));
        }

        const maxSteps = 600;
        const scale = 16;
        let currentCount = 0;
        let mode = 'growing'; // 'growing' (ขยายเพิ่ม), 'pause_full', 'shrinking' (หดลดลง), 'pause_empty'
        let pauseTimer = 0;

        function renderFrame() {
            ctx.clearRect(0, 0, width, height);

            const centerX = width / 2;
            const centerY = height / 2 - 20;

            // วาดเส้นตามจำนวน currentCount ณ เฟรมนั้น ๆ
            ctx.strokeStyle = '#ff1a3c';
            ctx.lineWidth = 1.2;
            ctx.shadowColor = '#ff2255';
            ctx.shadowBlur = 8;

            ctx.beginPath();
            for (let step = 0; step < currentCount; step++) {
                const targetX = centerX + heart1(step) * scale;
                const targetY = centerY + heart2(step) * scale;
                ctx.moveTo(centerX, centerY);
                ctx.lineTo(targetX, targetY);
            }
            ctx.stroke();

            // จัดการสเตตัสการเล่นแอนิเมชัน
            if (mode === 'growing') {
                currentCount += 3; // ความเร็วตอนสร้างเส้น
                if (currentCount >= maxSteps) {
                    currentCount = maxSteps;
                    mode = 'pause_full';
                    pauseTimer = 0;
                }
            } else if (mode === 'pause_full') {
                pauseTimer++;
                // พักโชว์หัวใจเต็มดวงประมาณ 1.5 วินาที
                if (pauseTimer > 70) {
                    mode = 'shrinking';
                }
            } else if (mode === 'shrinking') {
                currentCount -= 3; // ความเร็วตอนลดเส้นถอยหลัง
                if (currentCount <= 0) {
                    currentCount = 0;
                    mode = 'pause_empty';
                    pauseTimer = 0;
                }
            } else if (mode === 'pause_empty') {
                pauseTimer++;
                // พักตอนว่างเปล่าประมาณ 0.5 วินาที ก่อนเริ่มสร้างใหม่
                if (pauseTimer > 20) {
                    mode = 'growing';
                }
            }

            requestAnimationFrame(renderFrame);
        }

        renderFrame();
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