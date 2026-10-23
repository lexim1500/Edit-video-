// usage: node render_overlay.js <overlayDir> <outDir> <fps> <mode: test|all> [times...]
const { chromium } = require('playwright'); const fs=require('fs'); const path=require('path');
(async()=>{
  const [dir,out,fpsS,mode,...times]=process.argv.slice(2); const fps=+fpsS;
  const tl=JSON.parse(fs.readFileSync(path.join(dir,'timeline.json')));
  fs.mkdirSync(out,{recursive:true});
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium',args:['--allow-file-access-from-files']});
  const N=mode==='test'?1:4; const total=Math.round(tl.total*fps);
  const list=mode==='test'?times.map(Number):[...Array(total).keys()];
  await Promise.all([...Array(N).keys()].map(async w=>{
    const p=await b.newPage({viewport:{width:540,height:960},deviceScaleFactor:2});
    await p.goto('file://'+path.join(dir,'overlay.html')); await p.evaluate(tl=>window.init(tl),tl);
    for(let k=w;k<list.length;k+=N){
      const t=mode==='test'?list[k]:list[k]/fps;
      await p.evaluate(t=>window.renderAt(t),t);
      const name=mode==='test'?`t_${t}.png`:`f_${String(list[k]).padStart(5,'0')}.png`;
      await p.screenshot({path:path.join(out,name),omitBackground:true});
    }
  }));
  await b.close(); console.log('done',list.length);
})();
