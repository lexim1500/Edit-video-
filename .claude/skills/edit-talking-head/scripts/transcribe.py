import sys, json, wave, numpy as np, sherpa_onnx
m, wav, out = sys.argv[1], sys.argv[2], sys.argv[3]
rec = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f"{m}/encoder.int8.onnx", decoder=f"{m}/decoder.int8.onnx",
    joiner=f"{m}/joiner.int8.onnx", tokens=f"{m}/tokens.txt", model_type="nemo_transducer", num_threads=4)
w = wave.open(wav); a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)/32768; sr=w.getframerate()
words=[]; chunk=30*sr; off=0
while off < len(a):
    seg=a[off:off+chunk]; s=rec.create_stream(); s.accept_waveform(sr, seg); rec.decode_stream(s); r=s.result
    t0=off/sr
    for tok,ts in zip(r.tokens, r.timestamps):
        if tok.startswith(" ") or not words or words[-1].get("_c") != off:
            words.append({"w":tok.strip(),"s":round(t0+ts,2),"_c":off})
        else: words[-1]["w"]+=tok
    off+=chunk
for i,x in enumerate(words):
    x.pop("_c"); x["e"]=round(words[i+1]["s"] if i+1<len(words) else len(a)/sr,2)
json.dump(words, open(out,"w"))
print(" ".join(f"[{x['s']}]{x['w']}" for x in words))
