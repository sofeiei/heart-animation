from flask import Flask, render_template_string

app = Flask(__name__)

# หน้าเว็บที่เรนเดอร์แอนิเมชันเส้นรังสีรูปหัวใจแบบในคลิป
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
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        canvas {
            display: block;
        }
    </style>
</head>
<body>
    <canvas id="canvas"></canvas>

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

        // ฟังก์ชันคำนวณตามสูตรคณิตศาสตร์ในคลิป
        function heart1(m) {
            return 15 * Math.pow(Math.sin(m), 3);
        }

        function heart2(m) {
            // ติดลบเพื่อให้แกน Y พุ่งขึ้นด้านบน
            return -(12 * Math.cos(m) - 5 * Math.cos(2 * m) - 2 * Math.cos(3 * m) - Math.cos(4 * m));
        }

        let i = 0;
        const maxSteps = 600;
        const scale = 16;

        function draw() {
            const centerX = width / 2;
            const centerY = height / 2;

            // วาดทีละ 2-3 เส้นต่อเฟรมเพื่อสร้างจังหวะวิ่งค่อยๆ แผ่กิ่งก้าน
            for (let step = 0; step < 3; step++) {
                if (i <= maxSteps) {
                    const targetX = centerX + heart1(i) * scale;
                    const targetY = centerY + heart2(i) * scale;

                    ctx.strokeStyle = '#ff1a3c';
                    ctx.lineWidth = 1.2;
                    ctx.shadowColor = '#ff2255';
                    ctx.shadowBlur = 8;

                    // ลากเส้นจากจุดศูนย์กลาง (0, 0) ไปยังเส้นรอบรูปหัวใจ
                    ctx.beginPath();
                    ctx.moveTo(centerX, centerY);
                    ctx.lineTo(targetX, targetY);
                    ctx.stroke();

                    i++;
                }
            }

            requestAnimationFrame(draw);
        }

        function resetAnimation() {
            ctx.clearRect(0, 0, width, height);
            i = 0;
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