import json, sys, re
S=sys.argv[1]; W=json.load(open(f"{S}/work/raw_words.json")); DUR=84.5
sil=[(13.78,14.09),(14.90,15.48),(20.22,20.59),(22.65,23.09),(27.81,28.62),(31.34,31.83),(34.27,34.69),(35.32,35.84),(37.58,37.91),(39.06,39.56),(42.94,43.38),(47.82,48.21),(49.59,49.98),(52.18,52.54),(58.92,59.26),(61.74,62.35),(63.36,63.69),(65.64,66.11),(67.33,67.80),(77.88,78.68)]
cuts=[(a+0.10,b-0.07) for a,b in sil if (b-0.07)-(a+0.10)>0.12]
keep=[]; t=0
for a,b in cuts: keep.append((t,a)); t=b
keep.append((t,DUR))
# punch-in zoom changes (original time -> zoom)
Z=[(0,1.0),(2.08,1.15),(2.64,1.0),(8.16,1.12),(15.36,1.0),(20.48,1.12),(28.4,1.0),(33.2,1.2),(34.64,1.0),(39.44,1.12),(48.16,1.0),(49.92,1.15),(50.96,1.0),(62.24,1.12),(66.0,1.0),(72.48,1.12),(78.64,1.0),(80.96,1.12)]
def zoom_at(t): return [z for s,z in Z if s<=t+1e-6][-1]
pts=sorted(set([s for s,_ in Z]))
segs=[]
for a,b in keep:
    edges=[a]+[p for p in pts if a<p<b]+[b]
    for x,y in zip(edges,edges[1:]):
        x2,y2=round(x*30)/30,round(y*30)/30
        if y2-x2>0.03: segs.append((round(x2,4),round(y2,4),zoom_at(x)))
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
NEWDUR=round(sum(b-a for a,b,_ in segs),3)
# filter graph
f=[]
n=len(segs)
f.append("[0:v]crop=980:150:50:455,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1,min(min(X,W-1-X),min(Y,H-1-Y))/14)',split="+str(n)+"".join(f"[pt{i}]" for i in range(n)))
args=["-ss","14.0","-t","0.05","-i","MEDIA"]
for i,(a,b,z) in enumerate(segs):
    args+=["-ss",f"{a:.4f}","-t",f"{b-a:.4f}","-i","MEDIA"]
    cw,ch=1080/z,1920/z; x=(1080-cw)/2; y=0.38*1920*(1-1/z)
    k=i+1
    if a<28.26 and b>16.85:
        f.append(f"[{k}:v]setpts=PTS-STARTPTS[r{i}];[r{i}][pt{i}]overlay=50:455:eof_action=repeat:enable='between(t,{16.85-a:.3f},{28.26-a:.3f})'[q{i}]")
    else:
        f.append(f"[{k}:v]setpts=PTS-STARTPTS[q{i}];[pt{i}]nullsink")
    f.append(f"[q{i}]trim=end_frame={round((b-a)*30)},crop={cw:.0f}:{ch:.0f}:{x:.0f}:{y:.0f},scale=1080:1920:flags=lanczos,setsar=1,fps=30[v{i}]")
    d=b-a; f.append(f"[{k}:a]atrim=end={b-a:.4f},asetpts=PTS-STARTPTS,apad=whole_dur={b-a:.4f},afade=t=in:d=0.012,afade=t=out:st={max(0,d-0.012):.3f}:d=0.012[a{i}]")
json.dump(args,open(f"{S}/work/inputs.json","w"))
f.append("".join(f"[v{i}][a{i}]" for i in range(n))+f"concat=n={n}:v=1:a=1[cv][ca]")
f.append("[cv]colorbalance=rs=0.03:gs=0.005:bs=-0.04:rm=0.02:bm=-0.03,eq=saturation=1.06:contrast=1.03,tpad=stop_mode=clone:stop_duration=2.5[base]")
f.append("[ca]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,apad=pad_dur=2.5[aout]")
open(f"{S}/work/filter.txt","w").write(";\n".join(f))
# captions: map words, group into short lines
words=[dict(w=x["w"],s=round(m(x["s"]),3)) for x in W]
groups=[]; cur=[]
for i,x in enumerate(words):
    cur.append(x); txt=" ".join(c["w"] for c in cur)
    nxt=words[i+1]["w"] if i+1<len(words) else ""
    if re.search(r"[.,:?!]$",x["w"]) or len(txt+" "+nxt)>24 or i==len(words)-1:
        groups.append(cur); cur=[]
caps=[]
for gi,g in enumerate(groups):
    end=groups[gi+1][0]["s"] if gi+1<len(groups) else NEWDUR
    caps.append(dict(s=g[0]["s"],e=round(min(end,g[-1]["s"]+1.6),3),words=g))
E=lambda t: round(m(t),3)
ev=dict(
 hook=dict(s=0,a1=0,a2=E(1.76),e=E(2.6)),
 cal=dict(s=E(4.0),a2=E(5.4),e=E(8.1)),
 rule=dict(s=E(8.16),b1=E(11.36),b2=E(13.04),b3=E(14.24),e=E(15.3)),
 num=dict(s=E(15.42),b1=E(18.88),e=E(20.45)),
 math=dict(s=E(20.6),b1=E(24.6),b2=E(26.6),b2e=E(27.9),b3=E(28.8),e=E(31.6)),
 runout=dict(q=E(32.3),s=E(33.2),e=E(34.6)),
 growth=dict(s=E(35.7),d0=E(36.0),d1=E(43.0),b1=E(41.2),b2=E(45.6),e=E(48.1)),
 two=dict(s=E(48.16),b1=E(49.92),e=E(50.9)),
 tax=dict(s=E(51.0),b1=E(52.64),b2=E(55.68),b3=E(59.44),e=E(62.1)),
 market=dict(s=E(62.24),b1=E(66.0),b2=E(70.4),e=E(72.4)),
 cash=dict(s=E(72.48),b1=E(75.9),e=E(78.5)),
 cta=dict(s=E(78.64),b1=E(81.28),e=NEWDUR),
 end=dict(s=NEWDUR,e=NEWDUR+2.5))
json.dump(dict(dur=NEWDUR,total=NEWDUR+2.5,caps=caps,ev=ev),open(f"{S}/work/timeline.json","w"))
print("segments",n,"new duration",NEWDUR,"cut",round(DUR-NEWDUR,2))
