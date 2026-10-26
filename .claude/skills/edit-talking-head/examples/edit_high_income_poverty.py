import json, sys, re
P=sys.argv[1]; W=json.load(open(f"{P}/work/raw_words.json"))
sil=[tuple(map(float,x.split("-"))) for x in open(f"{P}/work/silences.txt").read().split()]
TAKES=[(4.44,8.56),(8.74,15.46),(25.83,29.33),(79.08,102.13),(112.24,115.88),(129.44,138.52),(208.96,218.77),(225.79,232.16),(239.15,244.19),(244.55,250.29)]
HOLD=0.8
keep=[]
for a,b in TAKES:
    t=a
    for s,e in sil:
        cs,ce=s+0.10,e-0.07
        if cs>a and ce<b and ce-cs>0.12: keep.append((t,cs)); t=ce
    keep.append((t,b))
Z=[(0,1.0),(6.6,1.14),(8.74,1.0),(13.0,1.12),(25.83,1.0),(27.3,1.15),(79.08,1.0),(86.4,1.1),(96.0,1.0),(112.24,1.14),(129.44,1.0),(134.7,1.15),(208.96,1.0),(211.4,1.1),(225.79,1.0),(230.1,1.12),(239.15,1.0),(244.55,1.12),(246.8,1.0)]
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
f=[]; args=[]; n=len(segs); AY=0.31
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
 hook=dict(s=0,b1=E(5.76),e=E(8.5)),
 up=dict(s=E(8.8),e=E(11.3)),
 photos=dict(s=E(11.3),p=[E(11.6),E(12.64),E(13.45),E(14.24),E(14.8)],e=E(15.46)),
 creep=dict(s=E(25.9),b1=E(28.4),e=E(29.3)),
 ex=dict(s=E(80.4),b1=E(81.1),b2=E(84.6),e=E(86.4)),
 bud=dict(s=E(86.5),x=[E(87.6),E(90.6),E(92.4),E(94.9),E(97.0),E(98.4)],gone=E(101.8),e=E(102.13)),
 rich=dict(s=E(112.24),b1=E(115.2),e=E(115.88)),
 prob=dict(s=E(130.4),b1=E(132.4),one=E(135.8),none=E(136.0),e=E(138.52)),
 wealth=dict(s=E(209.0),b1=E(210.5),e=E(211.4)),
 svs=dict(s=E(211.45),b1=E(213.6),b2=E(218.0),e=E(218.77)),
 steps=dict(s=E(225.85),x=[E(227.1),E(230.15),E(239.4)],e=E(244.19)),
 cta=dict(s=E(244.6),b1=E(246.85),e=DUR+HOLD))
json.dump(dict(dur=DUR,total=round(DUR+HOLD,3),caps=caps,ev=ev),open(f"{P}/overlay/timeline.json","w"))
print("segments",n,"duration",DUR)
