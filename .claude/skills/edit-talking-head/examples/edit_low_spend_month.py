import json, sys, re
P=sys.argv[1]; W=json.load(open(f"{P}/work/raw_words.json"))
sil=[tuple(map(float,x.split("-"))) for x in open(f"{P}/work/silences.txt").read().split()]
TAKES=[(0.62,8.50),(8.92,13.30),(13.93,17.56),(48.10,56.12),(56.51,61.45),(65.37,67.71),(67.93,73.66),(97.79,101.73),(101.92,112.26),(116.46,120.03),(141.62,162.70),(190.76,197.97),(213.20,218.95)]
HOLD=0.8
keep=[]
for a,b in TAKES:
    t=a
    for s,e in sil:
        cs,ce=s+0.10,e-0.07
        if cs>a and ce<b and ce-cs>0.12: keep.append((t,cs)); t=ce
    keep.append((t,b))
Z=[(0,1.0),(4.6,1.12),(8.92,1.0),(11.0,1.15),(13.93,1.0),(48.10,1.0),(52.0,1.12),(56.51,1.0),(65.37,1.12),(67.93,1.0),(97.79,1.12),(101.92,1.0),(108.08,1.1),(116.46,1.12),(141.62,1.0),(146.4,1.15),(150.16,1.0),(157.2,1.1),(190.76,1.0),(195.68,1.12),(213.20,1.0),(216.0,1.1)]
zoom_at=lambda t:[z for s,z in Z if s<=t+1e-6][-1]
pts=sorted(s for s,_ in Z)
segs=[]
for a,b in keep:
    edges=[a]+[p for p in pts if a<p<b]+[b]
    for x,y in zip(edges,edges[1:]):
        x2,y2=round(x*30)/30,round(y*30)/30
        if y2-x2>0.03: segs.append((round(x2,4),round(y2,4),zoom_at(x)))
# merge slivers (<0.25s) into a contiguous neighbour so no 1-2 frame flashes of a different zoom
merged=[]
for a,b,z in segs:
    if merged and b-a<0.25 and abs(merged[-1][1]-a)<1e-6: merged[-1]=(merged[-1][0],b,merged[-1][2]); continue
    if merged and merged[-1][1]-merged[-1][0]<0.25 and abs(merged[-1][1]-a)<1e-6:
        pa,pb,pz=merged.pop(); merged.append((pa,b,z)); continue
    merged.append((a,b,z))
segs=merged
def m(t):
    acc=0
    for a,b,_ in segs:
        if t<a: return acc
        if t<=b: return acc+(t-a)
        acc+=b-a
    return acc
DUR=round(sum(b-a for a,b,_ in segs),4)
f=[]; args=[]; n=len(segs); AY=0.34
for i,(a,b,z) in enumerate(segs):
    args+=["-ss",f"{a:.4f}","-t",f"{b-a:.4f}","-i","MEDIA"]
    cw,ch=1080/z,1920/z; x=(1080-cw)/2; y=AY*1920*(1-1/z)
    f.append(f"[{i}:v]setpts=PTS-STARTPTS,trim=end_frame={round((b-a)*30)},crop={cw:.0f}:{ch:.0f}:{x:.0f}:{y:.0f},scale=1080:1920:flags=lanczos,setsar=1,fps=30[v{i}]")
    d=b-a; f.append(f"[{i}:a]atrim=end={d:.4f},asetpts=PTS-STARTPTS,apad=whole_dur={d:.4f},afade=t=in:d=0.012,afade=t=out:st={max(0,d-0.012):.3f}:d=0.012[a{i}]")
f.append("".join(f"[v{i}][a{i}]" for i in range(n))+f"concat=n={n}:v=1:a=1[cv][ca]")
f.append(f"[cv]colorbalance=rs=0.03:gs=0.005:bs=-0.04:rm=0.02:bm=-0.03,eq=saturation=1.05:contrast=1.03,tpad=stop_mode=clone:stop_duration={HOLD}[base]")
f.append(f"[ca]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,apad=pad_dur={HOLD}[aout]")
open(f"{P}/work/filter.txt","w").write(";\n".join(f)); json.dump(args,open(f"{P}/work/inputs.json","w"))
# captions from words inside kept segments
def place(t):
    best=None
    for a,b,_ in segs:
        if a<=t<b: return t
        d=a-t if t<a else t-b+0.001
        lim=0.35 if t<a else 0.15
        if d<lim and (best is None or d<best[0]): best=(d,min(max(t,a),b-0.05))
    return best[1] if best else None
words=[]
for x in W:
    t=place(x["s"])
    if t is not None and (not words or m(t)>=words[-1]["s"]): words.append(dict(w=x["w"],s=round(m(t),3)))
for i,w in enumerate(words):
    FIX={"items.":"items,","Tech,":"tech,","on.":"on","Two":"two"}
    if w["w"] in FIX and not (w["w"]=="Two" and (i+1>=len(words) or words[i+1]["w"]!="paychecks")): w["w"]=FIX[w["w"]] if w["w"]!="Two" else "two"
    if w["w"]=="my" and i+1<len(words) and words[i+1]["w"]=="husband" and (i==0 or words[i-1]["w"].endswith(".")): w["w"]="My"
    if w["w"]=="that" and i+1<len(words) and words[i+1]["w"]=="cushion": w["w"]="That"
    if w["w"]=="bi": w["w"]="bio"
    if w["w"]=="A": w["w"]="a"
    if w["w"]=="in" and i+1<len(words) and words[i+1]["w"]=="DoorDash": w["w"]="and"
groups=[]; cur=[]
for i,x in enumerate(words):
    cur.append(x); txt=" ".join(c["w"] for c in cur); nxt=words[i+1]["w"] if i+1<len(words) else ""
    if re.search(r"[.,:?!]$",x["w"]) or len(txt+" "+nxt)>24 or i==len(words)-1: groups.append(cur); cur=[]
caps=[dict(s=g[0]["s"],e=round(min(groups[k+1][0]["s"] if k+1<len(groups) else DUR, g[-1]["s"]+1.6),3),words=g) for k,g in enumerate(groups)]
E=lambda t: round(m(t),3)
ev=dict(
 hook=dict(s=-1,b1=E(5.36),e=E(8.39)),
 cred=dict(s=E(9.84),c0=E(10.56),c1=E(12.08),e=E(13.2)),
 reasons=dict(s=E(13.93),b1=E(16.32),e=E(17.46)),
 h1=dict(s=E(48.1),b1=E(52.4),e=E(56.02)),
 skip=dict(s=E(56.51),x=[E(58.8),E(59.28),E(60.4)],e=E(61.35)),
 rules=dict(s=E(65.37),x=[E(69.36),E(71.52)],e=E(73.56)),
 fun=dict(s=E(97.79),b1=E(101.92),e=E(104.25)),
 photos=dict(p=[E(104.32),E(105.76),E(107.52)]),
 fun2=dict(s=E(108.6),e=E(112.16)),
 rest=dict(s=E(116.46),e=E(119.93)),
 pay=dict(s=E(141.62),b12=E(146.0),b3=E(146.96),e=E(151.5)),
 where=dict(s=E(151.6),b1=E(155.0),b2=E(160.4),e=E(162.6)),
 buf=dict(s=E(190.76),b1=E(192.16),b2=E(194.72),e=E(197.87)),
 cta=dict(s=E(213.2),b1=E(213.84),b2=E(216.08),e=DUR+HOLD))
json.dump(dict(dur=DUR,total=round(DUR+HOLD,3),caps=caps,ev=ev),open(f"{P}/overlay/timeline.json","w"))
print("segments",n,"duration",DUR)
