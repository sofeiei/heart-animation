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
        /* เลเยอร์ใส่ภาพป๊อปอัป */
        #popups-container {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 5;
            overflow: hidden;
        }
        .popup-img {
            position: absolute;
            width: 60px;
            height: 60px;
            object-fit: cover;
            border-radius: 0; /* สี่เหลี่ยมจัตุรัส */
            border: 2px solid #ff4d79;
            box-shadow: 0 0 15px rgba(255, 77, 121, 0.7);
            animation: popUpFloat 3.5s ease-out forwards;
        }
        /* แอนิเมชันเด้งป๊อปอัปขยายและลอยขึ้น */
        @keyframes popUpFloat {
            0% {
                transform: translate(-50%, -50%) scale(0) rotate(-10deg);
                opacity: 0;
            }
            20% {
                transform: translate(-50%, -50%) scale(1.15) rotate(5deg);
                opacity: 1;
            }
            35% {
                transform: translate(-50%, -50%) scale(1) rotate(0deg);
                opacity: 0.95;
            }
            80% {
                opacity: 0.8;
            }
            100% {
                transform: translate(-50%, -120px) scale(0.6) rotate(15deg);
                opacity: 0;
            }
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
    <div id="popups-container"></div>

    <div class="footer">
        HAPPY ANNIVERSARY 1 YEAR
    </div>

    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        const popupContainer = document.getElementById('popups-container');

        let width = canvas.width = window.innerWidth;
        let height = canvas.height = window.innerHeight;

        window.addEventListener('resize', () => {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
        });

        // รายการรูปภาพที่จะนำมาสุ่มป๊อปอัป (สามารถใส่ URL รูปภาพของคุณเองได้เลย)
        const photoUrls = [
            '/pic1.jpg',
            '/pic2.jpg',
            '/pic3.jpg'
        ];

        // ฟังก์ชันสร้างรูปป๊อปอัปสุ่มตำแหน่งรอบ ๆ
        function spawnPopup() {
            const img = document.createElement('img');
            img.className = 'popup-img';
            img.src = photoUrls[Math.floor(Math.random() * photoUrls.length)];

            // สุ่มพิกัดรอบ ๆ จุดกึ่งกลางหน้าจอ
            const angle = Math.random() * Math.PI * 2;
            const distance = 80 + Math.random() * 200; // ระยะห่างจากจุดศูนย์กลาง
            const x = (width / 2) + Math.cos(angle) * distance;
            const y = (height / 2 - 20) + Math.sin(angle) * distance;

            img.style.left = `${x}px`;
            img.style.top = `${y}px`;

            popupContainer.appendChild(img);

            // ลบทิ้งเมื่อเล่นแอนิเมชันเสร็จ เพื่อไม่ให้เปลือง Memory
            setTimeout(() => {
                img.remove();
            }, 3500);
        }

        // ให้รูปเด้งขึ้นมาทุก ๆ 1.2 วินาที
        setInterval(spawnPopup, 1200);

        function heart1(m) {
            return 15 * Math.pow(Math.sin(m), 3);
        }

        function heart2(m) {
            return -(12 * Math.cos(m) - 5 * Math.cos(2 * m) - 2 * Math.cos(3 * m) - Math.cos(4 * m));
        }

        const maxSteps = 600;
        const scale = 16;
        let currentCount = 0;
        let mode = 'growing';
        let pauseTimer = 0;

        function renderFrame() {
            ctx.clearRect(0, 0, width, height);

            const centerX = width / 2;
            const centerY = height / 2 - 20;

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

            if (mode === 'growing') {
                currentCount += 3;
                if (currentCount >= maxSteps) {
                    currentCount = maxSteps;
                    mode = 'pause_full';
                    pauseTimer = 0;
                }
            } else if (mode === 'pause_full') {
                pauseTimer++;
                if (pauseTimer > 70) {
                    mode = 'shrinking';
                }
            } else if (mode === 'shrinking') {
                currentCount -= 3;
                if (currentCount <= 0) {
                    currentCount = 0;
                    mode = 'pause_empty';
                    pauseTimer = 0;
                }
            } else if (mode === 'pause_empty') {
                pauseTimer++;
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