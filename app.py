from flask import Flask, render_template_string

app = Flask(__name__)

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width,initial-scale=1.0" />
<title>💘 Diana?</title>

<style>
  *{box-sizing:border-box;font-family:Poppins,system-ui,sans-serif}
  body{
    margin:0;height:100vh;overflow:hidden;
    display:flex;align-items:center;justify-content:center;
    background: radial-gradient(circle at top, #ffe0ec, #fff),
                linear-gradient(135deg,#ffafbd,#ffc3a0);
  }
  canvas{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
  #heartsCanvas{z-index:0}
  #effectsCanvas{z-index:1}

  .glow{
    position:absolute;width:480px;height:480px;border-radius:999px;
    background: radial-gradient(circle, rgba(255,59,107,.45), transparent 65%);
    filter: blur(90px);opacity:.35;z-index:1;
  }
  .glow.one{transform:translate(-180px,-120px)}
  .glow.two{
    background: radial-gradient(circle, rgba(255,170,200,.55), transparent 65%);
    transform:translate(200px,150px);opacity:.30;
  }

  .card{
    position:relative;z-index:3;
    width:min(410px,92vw);
    padding:34px 28px;border-radius:28px;text-align:center;
    background:rgba(255,255,255,.86);
    backdrop-filter:blur(12px);
    border:1px solid rgba(255,255,255,.55);
    box-shadow:0 28px 70px rgba(0,0,0,.18);
    animation:pop .7s ease, pulse 3.6s ease-in-out infinite;
  }
  @keyframes pop{from{transform:scale(.82);opacity:0}to{transform:scale(1);opacity:1}}
  @keyframes pulse{0%,100%{box-shadow:0 28px 70px rgba(0,0,0,.18)}50%{box-shadow:0 32px 84px rgba(255,59,107,.28)}}

  .toprow{font-size:20px;margin-bottom:6px}
  .badge{
    display:inline-block;padding:6px 10px;border-radius:999px;
    background:rgba(255,47,102,.10);color:#ff2f66;
    font-weight:800;font-size:12px;margin-bottom:10px;
  }
  h1{margin:0 0 10px;color:#ff2f66;font-size:28px;letter-spacing:.2px}
  p{margin:0 0 18px;color:#444;font-size:15px;line-height:1.45}

  .buttons{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:6px}
  button{
    border:none;padding:12px 22px;border-radius:16px;
    font-size:16px;font-weight:800;cursor:pointer;
    transition:transform .12s ease, filter .2s ease, box-shadow .2s ease;
    user-select:none;
  }
  button:active{transform:scale(.95)}
  #yes{
    color:#fff;
    background:linear-gradient(135deg,#ff2f66,#ff86ad);
    box-shadow:0 14px 30px rgba(255,47,102,.32);
  }
  #yes:hover{filter:brightness(1.02);box-shadow:0 16px 34px rgba(255,47,102,.38)}
  #no{background:#f1f1f1;color:#333;box-shadow:0 10px 22px rgba(0,0,0,.10);position:relative}

  .tiny{margin-top:10px;font-size:12px;color:#777}
  .footer{margin-top:18px;font-size:12px;color:#777}
</style>
</head>
<body>

<canvas id="heartsCanvas"></canvas>
<canvas id="effectsCanvas"></canvas>

<div class="glow one"></div>
<div class="glow two"></div>

<div class="card">
  <div class="toprow">✨💗✨</div>
  <div class="badge">For Diana</div>
  <h1 id="title">Hey Diana 💘</h1>
  <p id="subtitle">Will you be my Valentine?<br/>I promise snacks, laughs, and all my attention.</p>

  <div class="buttons" id="btnRow">
    <button id="yes">Yes 💕</button>
    <button id="no">No 🙈</button>
  </div>

  <div class="tiny">🔊 Music starts after you press “Yes”</div>
  <div class="footer">💌 From: Karim</div>
</div>

<audio id="bgm" preload="auto">
  <source src="/static/song.mp3" type="audio/mpeg" />
</audio>

<script>
  const herName = "Diana";
  const title = document.getElementById("title");
  const subtitle = document.getElementById("subtitle");
  const btnRow = document.getElementById("btnRow");
  const yesBtn = document.getElementById("yes");
  const noBtn = document.getElementById("no");
  const bgm = document.getElementById("bgm");
  title.textContent = `Hey ${herName} 💘`;

  const heartsCanvas = document.getElementById("heartsCanvas");
  const effectsCanvas = document.getElementById("effectsCanvas");
  const hctx = heartsCanvas.getContext("2d");
  const ectx = effectsCanvas.getContext("2d");

  function resize(){
    heartsCanvas.width = Math.floor(window.innerWidth * devicePixelRatio);
    heartsCanvas.height = Math.floor(window.innerHeight * devicePixelRatio);
    effectsCanvas.width = Math.floor(window.innerWidth * devicePixelRatio);
    effectsCanvas.height = Math.floor(window.innerHeight * devicePixelRatio);
    hctx.setTransform(devicePixelRatio,0,0,devicePixelRatio,0,0);
    ectx.setTransform(devicePixelRatio,0,0,devicePixelRatio,0,0);
  }
  window.addEventListener("resize", resize);
  resize();

  // Background hearts
  const heartEmojis = ["💖","💘","💗","💕","💞","💓"];
  const hearts = [];
  function addHeart(){
    const size = 14 + Math.random()*26;
    hearts.push({
      x: Math.random()*window.innerWidth,
      y: window.innerHeight + 30 + Math.random()*200,
      vy: 0.4 + Math.random()*1.0,
      vx: (Math.random()*0.6 - 0.3),
      rot: Math.random()*Math.PI*2,
      vr: (Math.random()*0.02 - 0.01),
      size,
      a: 0.25 + Math.random()*0.55,
      emoji: heartEmojis[Math.floor(Math.random()*heartEmojis.length)],
      drift: (Math.random()*1.2 - 0.6)
    });
  }
  for(let i=0;i<26;i++) addHeart();
  setInterval(() => { if(hearts.length < 46) addHeart(); }, 800);

  function drawHearts(){
    hctx.clearRect(0,0,window.innerWidth,window.innerHeight);
    hctx.save();
    hctx.textAlign = "center";
    hctx.textBaseline = "middle";
    for(const p of hearts){
      p.x += p.vx + Math.sin(p.y*0.01)*p.drift*0.2;
      p.y -= p.vy;
      p.rot += p.vr;

      if(p.y < -60){
        p.y = window.innerHeight + 60 + Math.random()*120;
        p.x = Math.random()*window.innerWidth;
      }

      hctx.globalAlpha = p.a;
      hctx.font = `${p.size}px system-ui, Apple Color Emoji, Segoe UI Emoji`;
      hctx.save();
      hctx.translate(p.x, p.y);
      hctx.rotate(p.rot);
      hctx.fillText(p.emoji, 0, 0);
      hctx.restore();
    }
    hctx.restore();
    requestAnimationFrame(drawHearts);
  }
  requestAnimationFrame(drawHearts);

  // Confetti + fireworks
  const confetti = [];
  const fireworks = [];

  function confettiBurst(cx, cy, amount=220){
    for(let i=0;i<amount;i++){
      const a = Math.random()*Math.PI*2;
      const s = 2 + Math.random()*6.5;
      confetti.push({
        x: cx, y: cy,
        vx: Math.cos(a)*s,
        vy: Math.sin(a)*s - 2.5,
        g: 0.08 + Math.random()*0.12,
        w: 5 + Math.random()*6,
        h: 5 + Math.random()*10,
        rot: Math.random()*Math.PI,
        vr: (Math.random()*0.25 - 0.125),
        life: 90 + Math.random()*70,
        alpha: 1
      });
    }
  }

  function firework(x, targetY){
    fireworks.push({
      kind:"rocket",
      x, y: window.innerHeight + 30,
      vx: (Math.random()*1.5 - 0.75),
      vy: -(7.5 + Math.random()*3.5),
      targetY,
      life: 120
    });
  }
  function explode(x,y, count=110){
    for(let i=0;i<count;i++){
      const a = Math.random()*Math.PI*2;
      const s = 1.5 + Math.random()*5.5;
      fireworks.push({
        kind:"spark",
        x, y,
        vx: Math.cos(a)*s,
        vy: Math.sin(a)*s,
        g: 0.06 + Math.random()*0.10,
        life: 70 + Math.random()*45,
        alpha: 1,
        size: 1 + Math.random()*2.5
      });
    }
  }

  function drawEffects(){
    ectx.clearRect(0,0,window.innerWidth,window.innerHeight);

    for(let i=confetti.length-1; i>=0; i--){
      const c = confetti[i];
      c.vy += c.g; c.x += c.vx; c.y += c.vy; c.rot += c.vr;
      c.life -= 1; c.alpha = Math.max(0, c.life/120);

      ectx.save();
      ectx.globalAlpha = c.alpha;
      ectx.translate(c.x, c.y);
      ectx.rotate(c.rot);
      const grad = ectx.createLinearGradient(-c.w, -c.h, c.w, c.h);
      grad.addColorStop(0, "rgba(255,47,102,0.95)");
      grad.addColorStop(1, "rgba(255,170,200,0.95)");
      ectx.fillStyle = grad;
      ectx.fillRect(-c.w/2, -c.h/2, c.w, c.h);
      ectx.restore();

      if(c.life <= 0 || c.y > window.innerHeight + 80) confetti.splice(i,1);
    }

    for(let i=fireworks.length-1; i>=0; i--){
      const f = fireworks[i];
      if(f.kind === "rocket"){
        f.x += f.vx; f.y += f.vy; f.life -= 1;

        ectx.save();
        ectx.globalAlpha = 0.85;
        ectx.beginPath();
        ectx.arc(f.x, f.y, 2.2, 0, Math.PI*2);
        ectx.fillStyle = "rgba(255,47,102,0.95)";
        ectx.fill();
        ectx.restore();

        ectx.save();
        ectx.globalAlpha = 0.25;
        ectx.beginPath();
        ectx.moveTo(f.x, f.y+12);
        ectx.lineTo(f.x - f.vx*6, f.y+30);
        ectx.strokeStyle = "rgba(255,170,200,0.9)";
        ectx.lineWidth = 2;
        ectx.stroke();
        ectx.restore();

        if(f.y <= f.targetY || f.life <= 0){
          explode(f.x, f.y, 110);
          fireworks.splice(i,1);
        }
      } else {
        f.vy += f.g; f.x += f.vx; f.y += f.vy; f.life -= 1;
        f.alpha = Math.max(0, f.life/90);

        ectx.save();
        ectx.globalAlpha = f.alpha;
        ectx.beginPath();
        ectx.arc(f.x, f.y, f.size, 0, Math.PI*2);
        ectx.fillStyle = "rgba(255,170,200,0.95)";
        ectx.fill();
        ectx.restore();

        if(f.life <= 0) fireworks.splice(i,1);
      }
    }

    requestAnimationFrame(drawEffects);
  }
  requestAnimationFrame(drawEffects);

  async function playMusicFadeIn(){
    try{
      bgm.volume = 0;
      await bgm.play();
      const fade = setInterval(() => {
        bgm.volume = Math.min(0.75, bgm.volume + 0.05);
        if(bgm.volume >= 0.75) clearInterval(fade);
      }, 140);
    }catch{
      const tip = document.querySelector(".tiny");
      tip.textContent = "Tap once anywhere to start the music 🔊";
      const once = async () => { try{ await bgm.play(); }catch{} document.removeEventListener("click", once); };
      document.addEventListener("click", once);
    }
  }

  noBtn.addEventListener("mouseenter", () => {
    const x = Math.random()*190 - 95;
    const y = Math.random()*140 - 70;
    noBtn.style.transform = `translate(${x}px, ${y}px)`;
  });

  yesBtn.addEventListener("click", async () => {
    title.textContent = `YAY ${herName}! 💖`;
    subtitle.textContent = "It’s official 💍 Get ready for the cutest Valentine ever.";
    btnRow.innerHTML = `<div style="font-size:28px">💞 💞 💞</div>`;

    const rect = document.querySelector(".card").getBoundingClientRect();
    confettiBurst(rect.left + rect.width/2, rect.top + rect.height/2, 220);

    for(let i=0; i<6; i++){
      setTimeout(() => {
        firework(
          window.innerWidth*(0.2 + Math.random()*0.6),
          window.innerHeight*(0.18 + Math.random()*0.28)
        );
      }, i * 380);
    }

    for(let i=0;i<14;i++) setTimeout(addHeart, i*60);
    await playMusicFadeIn();
  });
</script>

</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(debug=True)
