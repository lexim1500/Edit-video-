import base64, sys, html
S,P=sys.argv[1],sys.argv[2]
b64=lambda p: base64.b64encode(open(p,"rb").read()).decode()
img=lambda t: "data:image/jpeg;base64,"+b64(f"{P}/sb/f{t}.jpg")
jfont=lambda w: f'@font-face{{font-family:J;font-weight:{w};src:url(data:font/woff2;base64,{b64(f"{S}/fonts/package/files/montserrat-latin-{w}-normal.woff2")})}}'
font=lambda w: f'@font-face{{font-family:M;font-weight:{w};src:url(data:font/woff2;base64,{b64(f"{S}/fonts2/package/files/tiktok-sans-latin-{w}-normal.woff2")})}}'
H=lambda t,cls="": f'<div class="big {cls}">{t}</div>'
CARD=lambda h,b: f'<div class="card"><b>{h}</b><span>{b}</span></div>'
cap=lambda c: f'<div class="cap">{c}</div>'
X='<span class="x">x</span>'
scenes=[
 ("3","0:00","HOOK","“If you feel stressed about money and stuck living paycheck to paycheck, now until Thanksgiving is the perfect time to do a low spend month.”",
  H("Low Spend<br>Month<div class='subin'>now until Thanksgiving</div>","huge")+cap('stuck living <i>paycheck to</i>'),
  ["Extra-large headline on frame one, centered","Small line under it: “now until Thanksgiving”"]),
 ("11","0:08","CREDIBILITY","“This is coming from someone who has $600,000 invested by 28.”",
  H("$600K Invested<br>by 28")+cap('$600,000 <i>invested by</i>'),
  ["Number counts up from $0 to $600K as you say it"]),
 ("15","0:12","3 REASONS","“Hear me out. I have three reasons and the last is the biggest one.”",
  H("3 Reasons<div class='subin'>the last one is the biggest</div>")+cap('three reasons <i>and the</i>'),
  ["Numbered list format: your best performer lately (Deinfluencing) was a list too"]),
 ("50","0:16","#1 HOLIDAYS","“We are two months away from the holidays. Put it on your gift wish list or buy it on sale for Black Friday.”",
  CARD("#1 Holidays are 2 months away","Need it? <em>Gift wish list</em> or <em>Black Friday</em>")+cap('your gift <i>wish list</i>'),
  ["Card lines appear as you say them"]),
 ("58","0:24","SKIP FOR A MONTH","“You can survive one month without buying clothes, beauty items, tech, etc.”",
  CARD("Skip for 1 month",f"<span style=\"white-space:nowrap\">{X} Clothes {X} Beauty {X} Tech</span>")+cap('clothes, <i>beauty items</i>'),
  ["Each item gets a red strike-through on its word"]),
 ("70","0:29","OUR RULES","“My husband and I are doing a no-spend month. We deleted Amazon off our phones and didn’t give ourselves blow funds.”",
  CARD("Our rules this month",f"{X} Amazon app deleted<br>{X} No blow money")+cap('deleted <i>Amazon off</i>'),
  ["Two rules tick in, one per sentence"]),
 ("99","0:36","#2 FREE FUN","“Two, there are so many free or cheap things to do in most cities.”",
  CARD("#2 Free or cheap fun","Fall is the perfect time")+cap('free or <i>cheap things</i>'),
  ["Card, then your photos one at a time"]),
 ("103.5","0:40","PHOTO: FALL WALK","“It’s the perfect time for fall walks or hikes…”",'<div class="photos"><div class="ph" style="background:url(data:image/jpeg;base64,'+b64(f'{P}/overlay/hike.jpg')+') center/cover"></div></div>'+cap('fall walks <i>or hikes</i>'),["Your hike photo pops in large, centered over you, on “hikes”, about 1 second"]),
 ("105.9","0:42","PHOTO: SPORTS ON TV","“…watch a sports game on TV…”",'<div class="photos"><div class="ph" style="background:url(data:image/jpeg;base64,'+b64(f'{P}/overlay/sports.jpg')+') center/cover"></div></div>'+cap('a sports <i>game on TV</i>'),["Your sports bar photo on “sports game”"]),
 ("107.6","0:43","PHOTO: BOARD GAME","“…or play a board game. Enjoy the Halloween festivities…”",'<div class="photos"><div class="ph" style="background:url(data:image/jpeg;base64,'+b64(f'{P}/overlay/boardgame.jpg')+') center/cover"></div></div>'+cap('a board <i>game</i>'),["Your board game photo on “board game”. Its pumpkins carry into the Halloween line"]),
 ("118","0:47","THE RESTAURANT","“…fun doesn’t have to be expensive. And that expensive restaurant will also be there next month.”",
  H("Fun Doesn’t Have<br>to Be Expensive","sm")+cap('there <i>next month</i>'),
  ["Headline, then “It’ll be there next month” line"]),
 ("145","0:54","#3 THE 3RD PAYCHECK","“If you get paid bi-weekly, you get a third paycheck this month. You’re already used to living on two.”",
  CARD("#3 The 3rd paycheck","<div class='pay'><i>1</i><i>2</i><i class='on'>3</i></div>Bi-weekly? You get a <em>bonus paycheck</em>")+cap('a third <i>paycheck</i>'),
  ["Three paycheck boxes fill in; the third one lights up orange"]),
 ("155","1:03","WHERE IT GOES","“Put that extra paycheck into your emergency fund or investments… don’t rely on high interest debt.”",
  CARD("Paycheck #3 goes to","Emergency fund <em>or</em> investments<br>Not high-interest debt")+cap('emergency <i>fund or</i>'),
  ["Arrow from the 3rd paycheck to the two buckets"]),
 ("194","1:12","THE BUFFER","“That cushion will help you financially, but it will also make you feel better emotionally.”",
  H("A Buffer = Peace<br>of Mind","sm")+cap('better <i>emotionally</i>'),
  ["Headline on “financially”, second line on “emotionally”"]),
 ("215","1:19","CALL TO ACTION","“Tell me if you’re doing a low spend month. I’ll be sharing my journey and tips along the way.”",
  H("Doing a Low<br>Spend Month?","sm")+'<div class="pill">Comment <span>“me too”</span></div><div class="handle">Follow along @wealth_diet</div>'+cap('tell me <i>if you’re doing</i>'),
  ["Comment prompt instead of a booking button, since you ask viewers to tell you","No end card"]),
]
rows="".join(f'''<section><div class="thumb" style="background-image:url({img(t)})"><div class="safe"></div>{ov}</div>
<div class="info"><div class="tc">{tc} · <span>{n}</span></div><p class="say">{html.escape(say)}</p><ul>{"".join(f"<li>{x}</li>" for x in v)}</ul></div></section>''' for t,tc,n,say,ov,v in scenes)
print(f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Low Spend Month Storyboard</title><style>
{font(500)}{font(700)}{font(800)}{jfont(500)}{jfont(600)}{jfont(700)}{jfont(800)}
:root{{--bg:#f6f2ea;--line:#e2dacb;--mut:#6b655c;--acc:#d9822b}}
body{{margin:0;background:var(--bg);color:#1d1b18;font:15px/1.4 Inter,system-ui,sans-serif;padding:16px}}
h1{{font:800 26px/1.1 M;margin:4px 0}} .lead{{color:var(--mut);margin:0 0 14px}}
.box{{background:#fff;border:1px solid var(--line);border-radius:14px;padding:12px 14px;margin-bottom:16px}} .box b{{display:block;margin-bottom:4px}} .box li{{margin:3px 0}}
section{{display:flex;gap:12px;background:#fff;border:1px solid var(--line);border-radius:14px;padding:10px;margin-bottom:10px}}
.thumb{{position:relative;flex:0 0 135px;height:240px;border-radius:9px;background-size:cover;background-position:center;overflow:hidden}}
.safe{{position:absolute;left:11.1%;right:22.2%;top:13.1%;bottom:33.3%;border:1px dashed rgba(255,80,110,.9);z-index:5}}
.big{{position:absolute;left:11.1%;right:11.1%;top:15.5%;text-align:center;font:800 9.6px/1.0 J;color:#fff;text-shadow:0 1px 5px rgba(0,0,0,.5)}} .subin{{font:600 5.6px/1.2 J;margin-top:2px}}
.big.huge{{font-size:15px;line-height:0.98;top:15%}} .big.sm{{font-size:8.6px}}
.sub{{position:absolute;left:11.1%;right:11.1%;top:27.2%;text-align:center;font:500 6.2px J;color:#fff;text-shadow:0 1px 3px rgba(0,0,0,.6)}}
.card{{position:absolute;left:20.5%;right:20.5%;top:15%;background:#fbf7ee;border-radius:5px;padding:3px 4px;box-shadow:0 2px 6px rgba(0,0,0,.25);font:500 5px/1.2 J;color:#444;text-align:center}}
.card b{{display:block;font:800 6px/1.05 J;color:#222;margin-bottom:1px}} .card em{{color:var(--acc);font-style:normal;font-weight:800}}
.x{{display:inline-block;width:6px;height:6px;line-height:6px;border-radius:50%;background:#d64545;color:#fff;font:800 4px/6px M;text-align:center}}
.pay{{display:flex;gap:2px;justify-content:center;margin:1px 0 2px}} .pay i{{width:10px;height:7px;border:.6px solid #c9a94a;border-radius:1px;font:800 4px/7px M;font-style:normal;background:#fff6d6}} .pay i.on{{background:var(--acc);color:#fff}}
.photos{{position:absolute;left:18.5%;right:18.5%;top:29.2%;height:39.6%}} .ph{{height:100%;border-radius:6px;box-shadow:0 3px 10px rgba(0,0,0,.35);background:linear-gradient(#cfc6b8,#a99f90);font:700 4px M;color:#fff;display:flex;align-items:center;justify-content:center}}
.pill{{position:absolute;left:25%;right:25%;top:27%;background:#fff;border-radius:20px;text-align:center;font:800 5.2px J;padding:3px;box-shadow:0 2px 6px rgba(0,0,0,.3);white-space:nowrap}} .pill span{{color:var(--acc)}}
.handle{{position:absolute;left:11.1%;right:11.1%;top:32.5%;text-align:center;font:800 5.4px J;color:#fff;text-shadow:0 1px 3px #000}}
.cap{{position:absolute;left:20.4%;right:20.4%;top:77.6%;text-align:center;color:#fff;font:500 6.6px M;white-space:nowrap;text-shadow:0 1px 2px rgba(0,0,0,.7)}} .cap i{{font-style:normal;color:rgba(255,255,255,.55)}}
.info{{min-width:0}} .tc{{font-weight:800;font-size:13px}} .tc span{{color:var(--acc)}}
.say{{margin:5px 0;font-style:italic;color:var(--mut);font-size:13.5px}} ul{{margin:0;padding-left:17px;font-size:13.5px}} li{{margin:3px 0}}
</style></head><body>
<h1>“Low Spend Month” v5</h1><p class="lead">Storyboard · about 1:22 · 9:16 vertical</p>
<div class="box"><b>What I took from your page (last 7 days)</b><ul>
<li>Your best recent post is <b>Deinfluencing: overconsumption habits</b> (about 8,100 views, 13.5x your usual). Second is the <b>Theranos reaction</b> (about 2,500 views, 4.2x).</li>
<li>Both are opinion or list style with a timely hook. The pure explainers (Retirement, Budgeting) sit around 300 views.</li>
<li>So this edit leans in: a timely hook (Thanksgiving), your <b>$600K by 28</b> credibility in the first 10 seconds, and a clear numbered 1, 2, 3 list.</li></ul>
<b style="margin-top:8px">New in v2 and v3</b><ul><li><b style="display:inline">White Montserrat</b> titles in Title Case, with two-line titles stacked tightly</li><li><b style="display:inline">Small lines</b> (like “the last one is the biggest”) sit right under their title, no gap</li><li><b style="display:inline">Captions:</b> plain and lighter, like the captions on your videos</li><li><b style="display:inline">Your 3 photos</b> are now large and centered on screen, over your face: hike, sports on TV, board game. Plain, one at a time, about 1 second each, on the word</li></ul><b style="margin-top:8px">Edit choices</b><ul>
<li><b style="display:inline">Best takes only:</b> 3:40 of footage down to about 1:22</li>
<li><b style="display:inline">All top text centered</b> horizontally on the frame</li>
<li><b style="display:inline">Captions lower</b> than last time, at chest height</li>
<li>Style from your last two videos: cream cards, punch-in zooms, no emojis, no end card</li></ul></div>
{rows}</body></html>''')
