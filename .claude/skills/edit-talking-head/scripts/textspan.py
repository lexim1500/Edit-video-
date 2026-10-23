import subprocess, numpy as np, sys
src=sys.argv[1]
def frames(ss,dur):
    cmd=["ffmpeg","-loglevel","error","-ss",str(ss),"-t",str(dur),"-i",src,"-vf","crop=740:130:170:465,format=gray","-f","rawvideo","-"]
    b=subprocess.run(cmd,capture_output=True).stdout; return np.frombuffer(b,np.uint8).reshape(-1,130,740).astype(float)
ref=frames(14.0,0.04)[0]
for ss in (16.1,17.2):
    f=frames(ss,1.2); d=[np.abs(x-ref).mean() for x in f]
    print(ss, " ".join(f"{ss+i/30:.2f}:{v:.0f}" for i,v in enumerate(d)))
late=frames(29.0,0.04)[0]; print("static check 14 vs 29:", np.abs(late-ref).mean())
