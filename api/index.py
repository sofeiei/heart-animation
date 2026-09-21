from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Heart Animation</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background-color: #0b0914;
            overflow: hidden;
            display: flex;
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
        }
        .text-overlay {
            position: relative;
            z-index: 10;
            color: rgba(255, 255, 255, 0.85);
            font-size: 2rem;
            font-weight: 300;
            letter-spacing: 4px;
            pointer-events: none;
            text-shadow: 0 0 20px #ff2a74;
            animation: pulse 2s infinite ease-in-out;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 0.8; }
            50% { transform: scale(1.05); opacity: 1; text-shadow: 0 0 30px #ff0055; }
        }
    </style>
</head>
<body>
    <div class="text-overlay">💖 WITH LOVE 💖</div>
    <canvas id="heartCanvas"></canvas>

    <script>
        const canvas = document.getElementById('heartCanvas');
        const ctx = canvas.getContext('2d');

        let width = canvas.width = window.innerWidth;
        let height = canvas.height = window.innerHeight;

        window.addEventListener('resize', () => {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
        });

        function getHeartPoint(t, scale = 14) {
            const x = 16 * Math.pow(Math.sin(t), 3);
            const y = -(13 * Math.cos(t) - 5 * Math.cos(2 * t) - 2 * Math.cos(3 * t) - Math.cos(4 * t));
            return { x: x * scale, y: y * scale };
        }

        class Particle {
            constructor() { this.reset(); }
            reset() {
                this.t = Math.random() * Math.PI * 2;
                const pos = getHeartPoint(this.t, 13 + Math.random() * 2);
                this.baseX = pos.x;
                this.baseY = pos.y;
                this.x = this.baseX;
                this.y = this.baseY;
                this.vx = (Math.random() - 0.5) * 1.5;
                this.vy = (Math.random() - 0.5) * 1.5;
                this.size = Math.random() * 2.5 + 1;
                this.alpha = Math.random() * 0.7 + 0.3;
                this.decay = Math.random() * 0.015 + 0.005;
                const colors = ['#ff2a74', '#ff528c', '#ff7aa8', '#ffffff', '#e0115f'];
                this.color = colors[Math.floor(Math.random() * colors.length)];
            }
            update(scaleFactor) {
                this.x += this.vx;
                this.y += this.vy;
                this.alpha -= this.decay;
                if (this.alpha <= 0) {
                    this.reset();
                    this.x = this.baseX * scaleFactor;
                    this.y = this.baseY * scaleFactor;
                }
            }
            draw() {
                ctx.save();
                ctx.globalAlpha = Math.max(0, this.alpha);
                ctx.fillStyle = this.color;
                ctx.shadowBlur = 10;
                ctx.shadowColor = this.color;
                ctx.beginPath();
                ctx.arc(width / 2 + this.x, height / 2 + this.y, this.size, 0, Math.PI * 2);
                ctx.fill();
                ctx.restore();
            }
        }

        const particleCount = 700;
        const particles = [];
        for (let i = 0; i < particleCount; i++) {
            particles.push(new Particle());
        }

        let time = 0;
        function animate() {
            ctx.fillStyle = 'rgba(11, 9, 20, 0.2)';
            ctx.fillRect(0, 0, width, height);
            time += 0.05;
            const beat = 1 + Math.pow(Math.sin(time), 63) * 0.2 + Math.sin(time * 2) * 0.05;
            particles.forEach(p => {
                p.update(beat);
                p.draw();
            });
            requestAnimationFrame(animate);
        }
        animate();
    </script>
</body>
</html>
"""

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template_string(HTML_TEMPLATE)