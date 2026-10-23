import base64, sys, html
S, P = sys.argv[1], sys.argv[2]
b64=lambda p: base64.b64encode(open(p,"rb").read()).decode()
img=lambda t: "data:image/jpeg;base64,"+b64(f"{P}/sb/f{t}.jpg")
font=lambda w: f'@font-face{{font-family:M;font-weight:{w};src:url(data:font/woff2;base64,{b64(f"{S}/fonts/package/files/montserrat-latin-{w}-normal.woff2")})}}'
H=lambda t,cls="": f'<div class="big {cls}">{t}</div>'
CARD=lambda h,b: f'<div class="card"><b>{h}</b><span>{b}</span></div>'
cap=lambda c: f'<div class="cap">{c}</div>'
PH=lambda labels: '<div class="photos">'+"".join(f'<div class="ph">{l}</div>' for l in labels)+'</div>'
NEQ='<span class="neq">=</span>'
scenes=[
 ("6","0:00","HOOK","“Making six figures and have zero savings? That’s high income poverty.”",
  H("HIGH INCOME<br>POVERTY","huge")+cap('Making six <i>figures and</i>'),
  ["Extra-large white headline on frame one","Small line underneath pops in: “6 figures, $0 saved”"]),
 ("13","0:04","EVERYTHING WENT UP","“Your income went up, but so did everything else. The bigger apartment, the nicer car, the designer bag, the trips, the dinners out.”",
  PH(["Apartment","Car","Bag","Trip","Dinner"])+cap('the designer <i>bag,</i>'),
  ["<b>Photos</b> pop in one at a time, each on the exact word: apartment, car, bag, trip, dinner","Small polaroid-style frames with a slight tilt and shadow, in a row above your head"]),
 ("27","0:11","LIFESTYLE CREEP","“That’s lifestyle creep, and it’s sneaky because it happens a little at a time.”",
  H("LIFESTYLE<br>CREEP")+cap('it’s sneaky <i>because</i>'),
  ["Photos slide away, headline lands","Punch-in zoom on “sneaky”"]),
 ("85","0:15","THE EXAMPLE","“Say you make $150,000 a year after taxes. That’s around $9,000 a month.”",
  CARD("$150,000 a year","after taxes ≈ <em>$9,000/month</em>")+cap('That’s around <i>$9,000</i>'),
  ["Card with the numbers counting up"]),
 ("100","0:22","WHERE IT GOES","“Rent $3,500, car $800, credit cards $600, eating out and DoorDash $1,200, shopping $1,000, subscriptions, travel… gone.”",
  '<div class="card"><b>$9,000 → <span style="color:#d64545">$0</span></b><div class="bar"><i style="width:100%"></i></div><span>DoorDash <em style=\'color:#d64545\'>−$1,200</em></span></div>'+cap('that $9,000 <i>is gone</i>'),
  ["<b>Draining balance:</b> one expense at a time swaps in as you say it (rent, car, cards, DoorDash, shopping, subscriptions) and the $9,000 counts down","Bar shrinks to $0 and turns red on “gone”"]),
 ("114","0:37","RICH vs BROKE","“On paper, you look rich, but in your bank account, you’re actually broke.”",
  '<div class="two"><div><small>On paper</small><b>$150K</b><em>RICH</em></div><div><small>Bank account</small><b>$0</b><em style="color:#d64545">BROKE</em></div></div>'+cap('you’re <i>actually broke</i>'),
  ["Two side-by-side cards, the second slams in on “broke”"]),
 ("133","0:41","THE PROBLEM","“If you lost your job tomorrow, how many months could you actually last? If the answer is one or none…”",
  CARD("Lost your job?","How many months could you last?<div class='months'><i></i><i></i><i></i><i></i><i></i><i></i></div>")+cap('how many <i>months could</i>'),
  ["Six empty month boxes; one blinks in, then drops back to zero on “none”"]),
 ("213","0:50","SAVER vs SPENDER","“Someone making $70,000 who invests every month can end up richer than someone making $200,000 who spends it all.”",
  CARD("Saver vs Spender","$70K, invests → <em>~$590K</em><br>$200K, spends it all → $0")+cap('who spends <i>it all</i>'),
  ["First a headline: “Wealth ≠ what you earn”","Then this card: investing $1,000/month at an 8% average return grows to about $590K in 20 years (labeled as an illustration)"]),
 ("231","1:00","HOW TO GET OUT","“First, figure out where your money is actually going. Second, pay yourself first. Third, when you get a raise…”",
  CARD("How to get out","1  Track where it goes<br>2  Pay yourself first<br>3  <em>Split every raise</em>")+cap('pay yourself <i>first</i>'),
  ["Checklist: each step ticks in on “first / second / third”"]),
 ("248","1:10","CALL TO ACTION","“If you’re making good money but still feel broke, click the link in my bio…”",
  H("GOOD MONEY<br>BUT STILL BROKE?","sm")+'<div class="pill">Book a session · <span>link in bio</span></div><div class="handle">@wealth_diet</div>'+cap('click the <i>link in my bio</i>'),
  ["Button and handle above your head","2-second end card with @wealth_diet"]),
]
rows="".join(f'''<section><div class="thumb" style="background-image:url({img(t)})"><div class="safe"></div>{ov}</div>
<div class="info"><div class="tc">{tc} · <span>{n}</span></div><p class="say">{html.escape(say)}</p><ul>{"".join(f"<li>{x}</li>" for x in v)}</ul></div></section>''' for t,tc,n,say,ov,v in scenes)
print(f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>High Income Poverty Storyboard</title><style>
{font(600)}{font(700)}{font(800)}
:root{{--bg:#f6f2ea;--line:#e2dacb;--mut:#6b655c;--acc:#d9822b}}
body{{margin:0;background:var(--bg);color:#1d1b18;font:15px/1.4 Inter,system-ui,sans-serif;padding:16px}}
h1{{font:800 26px/1.1 M;margin:4px 0}} .sub{{color:var(--mut);margin:0 0 14px}}
.box{{background:#fff;border:1px solid var(--line);border-radius:14px;padding:12px 14px;margin-bottom:16px}} .box b{{display:block;margin-bottom:4px}} .box li{{margin:3px 0}}
section{{display:flex;gap:12px;background:#fff;border:1px solid var(--line);border-radius:14px;padding:10px;margin-bottom:10px}}
.thumb{{position:relative;flex:0 0 135px;height:240px;border-radius:9px;background-size:cover;background-position:center;overflow:hidden}}
.safe{{position:absolute;left:11.1%;right:22.2%;top:13.1%;bottom:33.3%;border:1px dashed rgba(255,80,110,.9);z-index:5}}
.big{{position:absolute;left:11.1%;right:22.2%;top:14.5%;text-align:center;font:800 8.6px/1.1 M;color:#fff;text-shadow:0 1px 5px rgba(0,0,0,.55)}}
.big.huge{{font-size:15px;line-height:1.02;top:15%}} .big.sm{{font-size:7.4px}}
.neq{{position:relative;display:inline-block}} .neq:after{{content:"";position:absolute;left:50%;top:50%;width:.12em;height:.95em;background:currentColor;transform:translate(-50%,-52%) rotate(28deg)}}
.card{{position:absolute;left:12.5%;right:23.5%;top:14.5%;background:#fbf7ee;border-radius:5px;padding:3px 4px;box-shadow:0 2px 6px rgba(0,0,0,.25);font:600 5px/1.3 M;color:#444}}
.big.sm+.card{{top:21%}}
.card b{{display:block;font:800 6.3px M;color:#222;margin-bottom:1px;white-space:nowrap}} .card em{{color:var(--acc);font-style:normal;font-weight:800}}
.bar{{height:3px;background:#eee;border-radius:2px;margin:2px 0}} .bar i{{display:block;height:100%;background:#d64545;border-radius:2px}}
.months{{display:flex;gap:1.5px;margin-top:2px}} .months i{{flex:1;height:5px;border:.6px solid #c9a94a;border-radius:1px;background:#fff6d6}}
.photos{{position:absolute;left:11.5%;right:22.5%;top:15.5%;display:flex;gap:1.5px}}
.ph{{flex:1;height:17px;background:#fff;border:1.5px solid #fff;box-shadow:0 1px 3px rgba(0,0,0,.4);font:700 3.4px/17px M;text-align:center;color:#888;background-image:linear-gradient(#ddd,#bbb);background-clip:content-box}}
.ph:nth-child(odd){{transform:rotate(-5deg)}} .ph:nth-child(even){{transform:rotate(4deg) translateY(2px)}}
.two{{position:absolute;left:12%;right:23%;top:14.5%;display:flex;gap:3px}} .two div{{flex:1;background:#fbf7ee;border-radius:4px;text-align:center;padding:2px;box-shadow:0 2px 6px rgba(0,0,0,.25);font:700 4px M;color:#666}}
.two b{{display:block;font:800 8px M;color:#222}} .two em{{font:800 5px M;color:#2f7d4f;font-style:normal}} .two small{{font-size:4px}}
.pill{{position:absolute;left:14%;right:25%;top:22%;background:#fff;border-radius:20px;text-align:center;font:800 5.2px M;padding:3px;box-shadow:0 2px 6px rgba(0,0,0,.3);white-space:nowrap}} .pill span{{color:var(--acc)}}
.handle{{position:absolute;left:11.1%;right:22.2%;top:27.5%;text-align:center;font:800 6px M;color:#fff;text-shadow:0 1px 3px #000}}
.cap{{position:absolute;left:11.1%;right:22.2%;top:67.7%;text-align:center;color:#fff;font:700 7.5px M;text-shadow:0 1px 3px #000}} .cap i{{font-style:normal;color:rgba(255,255,255,.55)}}
.info{{min-width:0}} .tc{{font-weight:800;font-size:13px}} .tc span{{color:var(--acc)}}
.say{{margin:5px 0;font-style:italic;color:var(--mut);font-size:13.5px}} ul{{margin:0;padding-left:17px;font-size:13.5px}} li{{margin:3px 0}}
</style></head><body>
<h1>“High Income Poverty”</h1><p class="sub">Storyboard · about 1:12 final length · 9:16 vertical</p>
<div class="box"><b>Same style as the last video, plus</b><ul>
<li><b style="display:inline">Best takes only:</b> you recorded most lines 2 to 5 times, so I keep the cleanest full take of each and cut the rest (4:22 of footage down to about 1:12)</li>
<li><b style="display:inline">Photos:</b> apartment, car, designer bag, trip and dinner pop in as you name them</li>
<li><b style="display:inline">Captions lower:</b> moved down about 5% from last time, just under your mic hand</li>
<li>Your head sits higher in this video, so cards are more compact to stay above it and inside the safe zone</li></ul></div>
{rows}</body></html>''')
