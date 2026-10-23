import base64, sys, html
S = sys.argv[1]
b64 = lambda p: base64.b64encode(open(p,"rb").read()).decode()
img = lambda t: "data:image/jpeg;base64," + b64(f"{S}/sb/f{t}.jpg")
font = lambda w: f'@font-face{{font-family:M;font-weight:{w};src:url(data:font/woff2;base64,{b64(f"{S}/fonts/package/files/montserrat-latin-{w}-normal.woff2")})}}'
Y = lambda t, top=0: f'<div class="big">{t}</div>'
CARD = lambda h, b, top=0: f'<div class="card"><b>{h}</b><span>{b}</span></div>'
Q = lambda x,y,s: f'<div class="q" style="left:{x}%;top:{y}%;font-size:{s}px">?</div>'
cap = lambda c: f'<div class="cap">{c}</div>'
NEW = '<span class="new">NEW</span>'
# growth chart: $1.25M, withdraw $50K rising 3%/yr, 10% avg return
pts=[]; b=1.25e6; w=5e4; ws=[]
for y in range(21): pts.append(b); ws.append(w); b=(b-w)*1.10; w*=1.03
X=lambda i: 18+i*4.6; Yb=lambda v: 62-v/4.6e6*50
line=" ".join(f"{X(i):.1f},{Yb(v):.1f}" for i,v in enumerate(pts))
chart=f'''<div class="card"><b>Account Keeps Growing</b>
<svg viewBox="0 0 115 72" width="100%" style="max-height:27px"><g font-size="4.2" fill="#777" font-family="M">
<text x="0" y="13">$4.5M</text><text x="0" y="38">$2.5M</text><text x="0" y="63">$0</text>
<text x="15" y="70">Yr 0</text><text x="60" y="70">10</text><text x="102" y="70">20</text></g>
<line x1="18" y1="62" x2="110" y2="62" stroke="#ccc" stroke-width=".4"/>
<polyline points="{line}" fill="none" stroke="#2f7d4f" stroke-width="1.6"/>
<circle cx="{X(20):.1f}" cy="{Yb(pts[20]):.1f}" r="1.8" fill="#e05a5a"/>
<text x="{X(20)-17:.1f}" y="{Yb(pts[20])+1:.1f}" font-size="5" font-weight="800" font-family="M" fill="#222">$4.5M</text>
<text x="20" y="57" font-size="4" font-family="M" fill="#d9822b" font-weight="700">withdrawing $50K → $90K/yr</text></svg></div>'''
calc = '<img class="calc" src="data:image/png;base64,'+b64(f'{S}/assets/calc.png')+'">'
scenes = [
 ("1.5","0:00","HOOK"+NEW,"“Retirement isn’t an age, it’s a number.”",
  '<div class="big huge">AGE<br>≠ $$$</div>'+cap('Retirement <i>isn’t an age</i>'),
  ["<b>Headline:</b> “AGE ≠ $$$”, extra large","White Montserrat, pops in line by line","Punch-in zoom on “number”"]),
 ("5.5","0:03","CALENDAR vs CALCULATOR"+NEW,"“Stop looking at a calendar… start using a calculator”",
  Y("CALENDAR ✗<br>CALCULATOR ✓",4)+calc+cap('start using a <i>calculator</i>'),
  ["<b>Your calculator photo</b> drops in under the text on “calculator”, with a slight tilt and shadow"]),
 ("11","0:08","THE 4% RULE","“If you can pull out 4% in your first year and live comfortably, you can stop working”",
  CARD("The 4% Rule","Withdraw <em>4%</em> in year one → live comfortably → <em>stop working</em>")+cap('pull out <i>4% in your</i>'),
  ["Cream card slides down above your head (no green circle)"]),
 ("18","0:15","YOUR NUMBER","“Take what you spend each year and multiply it by 25”",
  CARD("Your Number","Yearly spending <em>× 25</em>",20)+cap('multiply it <i>by 25</i>'),
  ["The text you typed on your phone gets blurred out so it doesn’t clash with the card"]),
 ("25","0:20","THE MATH","“$50,000… times 25… $1.25 million. Pull out 4%… there’s your 50,000”",
  CARD("$50,000 × 25","= <em>$1,250,000</em><br>4% of that → $50,000/yr")+cap('what you’ll <i>get is</i>'),
  ["Numbers count up live as you say them"]),
 ("33","0:32","THE OBJECTION","“Won’t the money run out?”",
  Y("WON’T IT<br>RUN OUT?",5)+Q(12,28,30)+Q(62,24,36)+Q(60,44,24)+Q(12,46,28)+cap('won’t the <i>money run out?</i>'),
  ["Floating question marks swirl in, copied from the reference","Tight punch-in for drama"]),
 ("40","0:35","ACCOUNT GROWTH"+NEW,"“The rest is still invested and growing… ~10% a year… bump your withdrawal ~3%”",
  chart+cap('still invested <i>and growing</i>'),
  ["<b>Animated growth chart:</b> the line draws itself as you talk","$1.25M grows to about $4.5M over 20 years, even while withdrawals rise from $50K to $90K a year (10% average return, 3% raises)","Small “illustration, not a guarantee” note in the corner"]),
 ("50","0:48","TWO THINGS","“Two things can change this number. First is taxes.”",
  Y("2 THINGS CAN<br>CHANGE THIS",5)+cap('Two things <i>can change</i>'),
  ["White headline, then “#1 TAXES”"]),
 ("56","0:51","#1 TAXES","“Roth… tax-free. Traditional… taxed when you pull it out. Brokerage… taxed on gains.”",
  '<div class="dash"><div><b>Roth</b>Tax-free</div><div><b>Trad.</b>Taxed out</div><div><b>Broker.</b>Taxed gains</div></div>'+cap('<i>comes out</i> tax-free'),
  ["Three boxes fill in one by one, like the reference’s dashboard"]),
 ("64","1:02","#2 THE MARKET","“That 10% average is not a guarantee… bigger bite out of a smaller pot”",
  CARD("10% ≠ Guaranteed","Bad year? Same $50K = <em>bigger bite</em> of a smaller pot")+cap('not a <i>guarantee</i>'),
  ["Pot graphic shrinks while the $50K slice stays the same"]),
 ("71","1:12","THE TIP","“It’s smart to have some cash on the side for tough times”",
  CARD("Cash Cushion","Keep cash on the side for <em>tough years</em>")+cap('cash on <i>the side</i>'),
  ["Small card, punch-in zoom"]),
 ("80","1:18","CALL TO ACTION","“Want to retire before 70? Link in my bio… money coaching session”",
  Y("RETIRE<br>BEFORE 70?",3)+'<div class="pill">🔗 Book a session · link in bio</div><div class="handle">@wealth_diet</div>'+cap('click the <i>link in my bio</i>'),
  ["White headline, then a “link in bio” button above your head","2-second end card: <b>@wealth_diet</b>"]),
]
rows = "".join(f'''<section><div class="thumb" style="background-image:url({img(t)})"><div class="safe"></div>{ov}</div>
<div class="info"><div class="tc">{tc} · <span>{name}</span></div><p class="say">{html.escape(say)}</p><ul>{"".join(f"<li>{x}</li>" for x in vis)}</ul></div></section>''' for t,tc,name,say,ov,vis in scenes)
print(f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Retirement Storyboard v2</title><style>
{font(600)}{font(700)}{font(800)}
:root{{--bg:#f6f2ea;--ink:#1d1b18;--mut:#6b655c;--line:#e2dacb;--acc:#d9822b}}
body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.4 Inter,system-ui,sans-serif;padding:16px}}
h1{{font:800 26px/1.1 M;margin:4px 0 4px}} .sub{{color:var(--mut);margin:0 0 14px}}
.box{{background:#fff;border:1px solid var(--line);border-radius:14px;padding:12px 14px;margin-bottom:16px}} .box b{{display:block;margin-bottom:4px}} .box li{{margin:3px 0}}
section{{display:flex;gap:12px;background:#fff;border:1px solid var(--line);border-radius:14px;padding:10px;margin-bottom:10px}}
.thumb{{position:relative;flex:0 0 135px;height:240px;border-radius:9px;background-size:cover;background-position:center;overflow:hidden}}
.big{{position:absolute;left:0;right:0;text-align:center;font:800 12px/1.08 M;color:#fff;text-shadow:0 1px 5px rgba(0,0,0,.55);letter-spacing:.2px}} .neq{{font-size:16px}}
.card{{position:absolute;left:7%;right:7%;background:#fbf7ee;border-radius:7px;padding:6px 7px;box-shadow:0 3px 10px rgba(0,0,0,.25);font:600 8px/1.3 M;color:#444}}
.card b{{display:block;font:800 10px M;margin-bottom:2px;color:#222}} .card em{{color:var(--acc);font-style:normal;font-weight:800}}
.dash{{position:absolute;left:5%;right:5%;display:flex;gap:3px;background:#fbf7ee;padding:5px;border-radius:7px;box-shadow:0 3px 10px rgba(0,0,0,.25)}}
.dash div{{flex:1;background:#fff8d8;border:1px solid #c9a94a;font:600 6.5px M;text-align:center;padding:3px 1px;color:#333}} .dash b{{display:block;font:800 7px M}}
.photo{{position:absolute;left:30%;right:30%;top:17%;height:13%;border:1.5px dashed #fff;border-radius:6px;background:rgba(0,0,0,.35);color:#fff;font:700 7px/1.2 M;text-align:center;padding-top:4px;transform:rotate(-6deg)}}
.q{{position:absolute;color:rgba(255,255,255,.75);font-weight:300}}
.pill{{position:absolute;left:10%;right:10%;top:22%;background:#fff;border-radius:20px;text-align:center;font:700 8px M;padding:5px;box-shadow:0 2px 8px rgba(0,0,0,.3)}}
.cap{{position:absolute;left:0;right:0;bottom:16%;text-align:center;color:#fff;font:700 9.5px M;text-shadow:0 1px 3px #000}} .cap i{{font-style:normal;color:rgba(255,255,255,.55)}}
.info{{min-width:0}} .tc{{font-weight:800;font-size:13px}} .tc span{{color:var(--acc)}}
.new{{background:#2f7d4f;color:#fff;font-size:10px;padding:1px 5px;border-radius:6px;margin-left:5px;vertical-align:2px}}
.say{{margin:5px 0;font-style:italic;color:var(--mut);font-size:13.5px}} ul{{margin:0;padding-left:17px;font-size:13.5px}} li{{margin:3px 0}}

.safe{{position:absolute;left:11.1%;right:22.2%;top:13.1%;bottom:33.3%;border:1px dashed rgba(255,80,110,.9);border-radius:2px;z-index:5;pointer-events:none}}
.big{{left:11.1%!important;right:22.2%!important;top:14.5%!important;font-size:9.5px!important;line-height:1.1!important}} .neq{{font-size:11px!important}}
.card{{left:12.5%!important;right:23.5%!important;top:14.5%!important;padding:4px 5px!important;font-size:6.2px!important;line-height:1.25!important}}
.card b{{font-size:7.5px!important;margin-bottom:1px!important}}
.dash{{left:12%!important;right:23%!important;top:14.5%!important;padding:3px!important;gap:2px!important}} .dash div{{font-size:5.2px!important}} .dash b{{font-size:5.8px!important}}
.photo{{left:32%!important;right:42%!important;top:19.5%!important;height:9%!important;font-size:5px!important;padding-top:2px!important}}
.pill{{left:12%!important;right:23%!important;top:24.5%!important;font-size:5.2px!important;padding:3px!important;white-space:nowrap}}
.cap{{left:11.1%!important;right:22.2%!important;bottom:24%!important;font-size:7.5px!important}}
.q{{transform:scale(.6)}}
.big.huge{{font-size:22px!important;line-height:1.02!important;top:15%!important}}
.calc{{position:absolute;left:39.5%;width:12%;top:22.8%;transform:rotate(-7deg);filter:drop-shadow(0 3px 4px rgba(0,0,0,.45))}}
.handle{{position:absolute;left:11.1%;right:22.2%;top:32%;text-align:center;font:800 7.5px M;color:#fff;text-shadow:0 1px 3px #000}}
.big{{font-size:8.6px!important;letter-spacing:0!important}}
.dash div{{min-width:0;overflow:hidden;font-size:4.8px!important}} .dash b{{font-size:5.2px!important}}
.photo{{top:23%!important}}
</style></head><body>
<h1>Storyboard v6</h1><p class="sub">About 1:20 · 9:16 vertical · scenes with changes are tagged <span class="new">NEW</span></p>
<div class="box"><b>New in v3: TikTok safe zone</b><ul>
<li>Every headline, card, photo and caption is smaller and sits inside the dashed box, which matches your TikTok template (60px left, 120px right, 126px top, 320px bottom on a 540×960 frame)</li>
<li>Nothing will be hidden by TikTok’s buttons, username, caption or top tabs</li>
<li>Word-by-word captions sit right above your hands (just below the safe line, see note)</li></ul>
<b style="margin-top:8px">Still in from v2</b><ul>
<li>Opening headline is now “Retirement Age ≠ Dollar Amount”</li>
<li>All headlines are white Montserrat and a bit smaller</li>
<li>Green circles removed from the cards</li>
<li>All cards and headlines sit above your head, never over your face</li>
<li>Your calculator photo instead of the emoji</li>
<li>New investment growth chart when you explain growth</li></ul></div>
{rows}</body></html>''')
