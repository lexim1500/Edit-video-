import json, sys, re
P=sys.argv[1]; W=json.load(open(f"{P}/work/raw_words.json"))
sil=[tuple(map(float,x.split("-"))) for x in open(f"{P}/work/silences.txt").read().split()]
TAKES=[(0.55,17.62),(48.05,61.50),(65.30,73.70),(97.70,112.30),(116.40,120.10),(141.55,162.75),(190.70,198.05),(213.15,218.95)]
HOLD=0.8
keep=[]
for a,b in TAKES:
    t=a
    for s,e in sil:
        cs,ce=s+0.22,e-0.18
        if e-s>=0.75 and cs>a and ce<b and ce-cs>0.12: keep.append((t,cs)); t=ce
    keep.append((t,b))
Z=[(0,1.0)]
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
 hook=dict(s=-1,e=E(48.0)),
 sec=[dict(n="1. the holidays are 2 months away",s=E(48.1),e=E(97.6)),
      dict(n="2. free or cheap fun",s=E(97.75),e=E(141.5)),
      dict(n="3. the third paycheck",s=E(141.6),e=E(213.1))],
 photos=dict(p=[E(104.32),E(105.76),E(107.52)]),
 cta=dict(s=E(213.2),e=DUR+HOLD))
json.dump(dict(dur=DUR,total=round(DUR+HOLD,3),caps=caps,ev=ev),open(f"{P}/overlay/timeline.json","w"))
print("segments",n,"duration",DUR)
