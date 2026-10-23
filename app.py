import streamlit as st
import streamlit.components.v1 as components
st.set_page_config(page_title="ISSF Trap Preview", page_icon="🎯", layout="wide")
HTML = r"""<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no"><style>
html,body{margin:0;background:#0f1720;color:#fff;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}.app{max-width:1100px;margin:auto;padding:6px}.head{display:flex;justify-content:space-between;align-items:center}.sub{font-size:11px;color:#aab7c4}button{background:#24323c;color:white;border:1px solid #394955;border-radius:9px;padding:7px;font-weight:800}.active{background:#ff681c;border-color:#ff984f}.stage{position:relative;border-radius:14px;overflow:hidden;border:1px solid #33444f}canvas{width:100%;height:53vh;display:block}.info{position:absolute;left:8px;bottom:8px;background:#051014cc;padding:7px 9px;border-radius:8px;font-size:12px}.launch{display:flex;justify-content:center;margin:5px 0}.launch button{width:min(60%,420px);background:#ff681c;border-color:#ff984f;font-size:17px;padding:9px}.controls{display:grid;grid-template-columns:1.05fr .75fr 1.3fr;gap:5px}.panel{background:#18242d;border:1px solid #263740;border-radius:11px;padding:7px}.row{display:flex;justify-content:space-between;font-size:12px;color:#c7d2da}.g10{display:grid;grid-template-columns:repeat(5,1fr);gap:3px;margin-top:5px}.g5{display:grid;grid-template-columns:repeat(5,1fr);gap:3px;margin-top:5px}.g3{display:grid;grid-template-columns:repeat(3,1fr);gap:3px;margin-top:5px}.card{background:#24323c;border:1px solid #394955;border-radius:8px;padding:5px;text-align:center;font-size:11px}.next{background:#101b22;border-radius:8px;padding:6px;margin-top:5px;text-align:center;font-size:12px;font-weight:800}.hidden{display:none}@media(orientation:portrait){.controls{display:block}.panel{margin-top:5px}canvas{height:48vh}.launch button{width:88%}}
</style></head><body><div class="app"><div class="head"><div><b>ISSF Trap Preview</b><div class="sub">2026セット表 Ver.3 ・ iPhone横画面推奨</div></div><div style="display:flex;gap:5px"><button id="flashBtn">発光 ON</button><button id="infoBtn">情報 ON</button></div></div><div class="stage"><canvas id="cv"></canvas><div id="info" class="info hidden"></div></div><div class="launch"><button id="launchBtn">TAP / 次へ</button></div><div class="controls"><div class="panel"><div class="row"><b>セット</b><span id="setL"></span></div><div id="sets" class="g10"></div></div><div class="panel"><div class="row"><b>射台</b><span id="stL"></span></div><div id="sts" class="g5"></div></div><div class="panel"><div class="row"><b>自動進行</b><span>1→5</span></div><div id="cards" class="g3"></div><div id="next" class="next"></div></div></div></div><script>
const SETS={1:[[30,2.50],[10,1.50],[-30,3.00],[40,1.70],[-5,2.00],[-45,2.00],[45,2.00],[-10,3.00],[-45,2.80],[45,2.30],[10,1.80],[-40,1.60],[30,2.00],[-5,1.50],[-35,3.00]],2:[[45,2.30],[10,1.50],[-20,2.80],[45,1.50],[0,2.00],[-45,2.00],[25,2.00],[0,3.00],[-45,1.50],[35,2.20],[10,2.40],[-40,1.50],[30,2.80],[-10,1.50],[-45,2.00]],3:[[45,2.50],[0,1.60],[-20,2.00],[35,2.90],[-5,1.80],[-45,3.00],[35,2.50],[-10,3.00],[-40,2.20],[40,2.00],[-5,2.50],[-30,3.00],[30,2.00],[0,1.80],[-30,3.00]],4:[[30,1.50],[0,3.00],[-20,2.20],[30,2.00],[-10,1.50],[-45,3.00],[25,3.00],[-5,1.50],[-15,1.80],[40,2.80],[-5,1.50],[-35,2.20],[15,3.00],[10,3.00],[-40,1.70]],5:[[20,1.80],[0,3.00],[-25,2.60],[35,3.00],[0,1.60],[-35,3.00],[35,2.30],[-5,1.80],[-35,1.60],[40,2.30],[0,2.30],[-40,3.00],[25,1.80],[-5,2.50],[-45,2.00]],6:[[45,1.90],[0,2.80],[-30,3.00],[40,1.50],[0,1.60],[-40,2.00],[35,2.00],[0,3.00],[-45,2.00],[45,2.30],[5,2.00],[-40,3.00],[25,2.40],[0,1.75],[-35,1.80]],7:[[40,3.00],[0,1.50],[-35,1.50],[45,2.00],[5,2.20],[-45,3.00],[40,1.50],[5,1.90],[-25,2.60],[20,1.80],[0,3.00],[-30,2.20],[35,2.50],[0,3.00],[-40,3.00]],8:[[40,3.00],[-5,3.00],[-15,2.20],[30,2.00],[-5,2.00],[-35,1.80],[40,2.00],[5,1.50],[-35,2.50],[45,1.50],[5,2.00],[-25,3.00],[15,1.50],[0,1.50],[-45,1.60]],9:[[30,1.60],[0,1.50],[-15,2.00],[20,2.40],[-5,3.00],[-35,2.00],[45,2.00],[-5,1.50],[-35,1.50],[45,1.60],[0,2.80],[-45,2.00],[25,3.00],[5,1.50],[-20,3.00]],10:[[45,2.25],[0,1.75],[-25,2.00],[35,1.80],[0,3.00],[-40,2.25],[40,3.00],[5,1.80],[-45,3.00],[45,2.00],[-10,2.50],[-35,1.50],[15,1.80],[10,2.00],[-45,1.50]]}; let setNo=1,station=1,shot=0,flying=false,showInfo=true,flashEnabled=true,raf;const cv=document.getElementById('cv'),ctx=cv.getContext('2d');const at=a=>a>0?`右${a}°`:a<0?`左${Math.abs(a)}°`:'直進';
function resize(){const r=cv.getBoundingClientRect(),d=devicePixelRatio||1;cv.width=r.width*d;cv.height=r.height*d;ctx.setTransform(d,0,0,d,0,0);draw()}
function bg(){
  const w=cv.clientWidth,h=cv.clientHeight,hz=h*.48;
  const sky=ctx.createLinearGradient(0,0,0,hz);sky.addColorStop(0,'#71bae8');sky.addColorStop(1,'#dceff8');ctx.fillStyle=sky;ctx.fillRect(0,0,w,hz);
  const g=ctx.createLinearGradient(0,hz,0,h);g.addColorStop(0,'#789e50');g.addColorStop(1,'#345a2c');ctx.fillStyle=g;ctx.fillRect(0,hz,w,h-hz);

  // Perspective based on an eye height of 1.77m, 15m in front, and a 2m-deep opening.
  const eyeHeight=1.77,viewerDistance=15,openingDepth=2;
  const depression=Math.atan2(eyeHeight,viewerDistance);
  const farScale=viewerDistance/(viewerDistance+openingDepth);
  const houseW=w*.48,houseH=Math.max(28,h*.085),hx=(w-houseW)/2,hy=h*.69;
  const nearW=houseW*.76,farW=nearW*farScale;
  const nearX=(w-nearW)/2,farX=(w-farW)/2;
  const depthPx=Math.max(12,Math.min(28,h*(openingDepth/viewerDistance)*(1.15+Math.sin(depression)*2.5)));
  const nearY=hy,farY=hy-depthPx;

  // Front wall remains rectangular.
  ctx.fillStyle='#4b5961';ctx.fillRect(hx,hy,houseW,houseH);
  ctx.strokeStyle='#26343b';ctx.lineWidth=2;ctx.strokeRect(hx,hy,houseW,houseH);

  // The 2m-deep opening is a perspective trapezoid, seen slightly from above.
  ctx.fillStyle='#11181c';ctx.beginPath();ctx.moveTo(nearX,nearY);ctx.lineTo(nearX+nearW,nearY);ctx.lineTo(farX+farW,farY);ctx.lineTo(farX,farY);ctx.closePath();ctx.fill();
  ctx.strokeStyle='#91a1aa';ctx.lineWidth=1.5;ctx.stroke();
  ctx.strokeStyle='rgba(255,255,255,.22)';ctx.beginPath();ctx.moveTo(nearX,nearY);ctx.lineTo(farX,farY);ctx.moveTo(nearX+nearW,nearY);ctx.lineTo(farX+farW,farY);ctx.stroke();

  // Center reference line and launch point at the middle of the opening.
  const launchY=(nearY+farY)/2;
  ctx.strokeStyle='#ffffff99';ctx.lineWidth=1.5;ctx.beginPath();ctx.moveTo(w/2,launchY);ctx.lineTo(w/2,h);ctx.stroke();
  return {w,h,oy:launchY};
}
function draw(){if(flying)return;const q=bg(),base=(station-1)*3+1;ctx.fillStyle='#0007';ctx.fillRect(0,0,q.w,38);ctx.fillStyle='white';ctx.font='600 13px system-ui';ctx.textAlign='center';ctx.fillText(`${setNo}番セット・${station}番射台・次 放出機${base+shot}`,q.w/2,24)}
function ui(){document.getElementById('setL').textContent=setNo+'番';document.getElementById('stL').textContent=station+'番';document.querySelectorAll('#sets button').forEach((b,i)=>b.className=i+1===setNo?'active':'');document.querySelectorAll('#sts button').forEach((b,i)=>b.className=i+1===station?'active':'');const pool=SETS[setNo].slice((station-1)*3,station*3),base=(station-1)*3+1,c=document.getElementById('cards');c.innerHTML='';pool.forEach(([a,h],i)=>{let d=document.createElement('div');d.className='card '+(i===shot?'active':'');d.innerHTML=`<b>${base+i}</b><br>${at(a)}<br>${h.toFixed(2)}m`;c.appendChild(d)});let [a,h]=pool[shot];document.getElementById('next').textContent=`次 ${base+shot}・${at(a)}・${h.toFixed(2)}m`;draw()}
function ballistics(height){
  const g=9.80665,R=76,x10=10;
  // Vacuum-trajectory approximation. Height is the vertical rise at 10m.
  // y(x)=x*tan(theta)*(1-x/R), with y(R)=0.
  const tanTheta=height/(x10*(1-x10/R));
  const theta=Math.atan(tanTheta);
  const speed=Math.sqrt(g*R/Math.sin(2*theta));
  const flightTime=Math.sqrt(2*R*tanTheta/g);
  return {g,R,tanTheta,theta,speed,flightTime};
}
function launch(){
  if(flying)return;
  flying=true;
  document.getElementById('launchBtn').disabled=true;
  const pool=SETS[setNo].slice((station-1)*3,station*3),current=shot,[angle,height]=pool[current],base=(station-1)*3+1;
  const b=ballistics(height),inf=document.getElementById('info');
  inf.textContent=`放出機 ${base+current}　${at(angle)}　高度 ${height.toFixed(2)}m　初速 ${b.speed.toFixed(1)}m/s　飛翔 ${b.flightTime.toFixed(2)}秒　白発光 ${flashEnabled?'ON':'OFF'} 30m`;
  if(showInfo)inf.classList.remove('hidden');
  const q=bg(),w=q.w,h=q.h,start=performance.now(),dur=b.flightTime*1000,sx=w/2,sy=q.oy;
  const angleRatio=Math.sign(angle)*Math.pow(Math.abs(angle)/45,.72),ex=w/2+angleRatio*w*.70;
  const flashDistance=30,flashDurationMs=140;
  let flashStartedAt=null;
  function f(now){
    const u=Math.min(1,(now-start)/dur);
    bg();
    // Horizontal progress is linear in the no-drag model.
    const range=b.R*u;
    if(flashStartedAt===null && range>=flashDistance) flashStartedAt=now;
    const isFlashing=flashEnabled && flashStartedAt!==null && (now-flashStartedAt)<flashDurationMs;
    const rise=range*b.tanTheta*(1-range/b.R);
    const x=sx+(ex-sx)*u;
    // Every target lands at the same 76m depth; only the arc and time vary.
    const groundY=sy-u*h*.28;
    const y=groundY-rise*h*.060;
    const sc=Math.max(.22,1-.72*u);
    ctx.save();ctx.translate(x,y);
    if(isFlashing){
      // Strong white flash: halo + enlarged white target, then return to orange.
      ctx.save();ctx.scale(sc,sc);ctx.shadowColor='#ffffff';ctx.shadowBlur=28;
      const halo=ctx.createRadialGradient(0,0,3,0,0,34);halo.addColorStop(0,'rgba(255,255,255,1)');halo.addColorStop(.35,'rgba(255,255,255,.95)');halo.addColorStop(1,'rgba(255,255,255,0)');
      ctx.fillStyle=halo;ctx.beginPath();ctx.arc(0,0,34,0,Math.PI*2);ctx.fill();ctx.restore();
    }
    ctx.scale(sc*(isFlashing?1.45:1),sc*.34*(isFlashing?1.45:1));
    ctx.fillStyle=isFlashing?'#ffffff':'#ff5b18';ctx.beginPath();ctx.arc(0,0,14,0,Math.PI*2);ctx.fill();
    ctx.strokeStyle=isFlashing?'#ffffff':'#ffe0bd';ctx.lineWidth=isFlashing?5:2;ctx.stroke();ctx.restore();
    if(u<1)raf=requestAnimationFrame(f);
    else{
      if(current===2){shot=0;station=station===5?1:station+1}else shot=current+1;
      flying=false;document.getElementById('launchBtn').disabled=false;ui();
    }
  }
  raf=requestAnimationFrame(f);
}

for(let i=1;i<=10;i++){let b=document.createElement('button');b.textContent=i;b.onclick=()=>{setNo=i;station=1;shot=0;ui()};document.getElementById('sets').appendChild(b)}for(let i=1;i<=5;i++){let b=document.createElement('button');b.textContent=i;b.onclick=()=>{station=i;shot=0;ui()};document.getElementById('sts').appendChild(b)}document.getElementById('launchBtn').addEventListener('pointerdown',e=>{e.preventDefault();launch()});document.getElementById('flashBtn').onclick=()=>{flashEnabled=!flashEnabled;document.getElementById('flashBtn').textContent='発光 '+(flashEnabled?'ON':'OFF')};document.getElementById('infoBtn').onclick=()=>{showInfo=!showInfo;document.getElementById('infoBtn').textContent='情報 '+(showInfo?'ON':'OFF');if(!showInfo)document.getElementById('info').classList.add('hidden')};window.addEventListener('resize',resize);requestAnimationFrame(()=>{resize();ui()});
</script></body></html>"""
components.html(HTML, height=650, scrolling=True)
