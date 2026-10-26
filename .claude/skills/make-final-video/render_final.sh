#!/bin/bash
# The exact render that played cleanly on TikTok and YouTube (High Income Poverty v3).
# usage: render_final.sh <raw.mov> <work_dir with inputs.json + filter.txt> <overlay_frames_dir> <out.mp4>
set -euo pipefail
RAW=$1; W=$2; OV=$3; OUT=$4
C="-colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv"
# 1. Frame-exact intermediate: every frame a keyframe, so each cut starts on the right frame.
ffmpeg -hide_banner -loglevel error -y -i "$RAW" -map 0:v:0 -map 0:a:0 -vf "fps=30,scale=1080:1920:flags=lanczos,format=yuv420p" \
  -c:v libx264 -preset veryfast -crf 14 -g 1 -c:a pcm_s16le -ar 48000 "$W/mezz.mov"
# 2. Safety check: no clip under 0.5s (single-frame zoom flashes look like glitches).
python3 -I -c "import json,sys;a=json.load(open('$W/inputs.json'));d=[float(a[i+3]) for i in range(0,len(a),6)];m=min(d);print('shortest clip',m);sys.exit(1 if m<0.5 else 0)"
# 3. Base edit cut from the intermediate (never from the raw HEVC).
ARGS=$(python3 -I -c "import json,shlex;print(' '.join(shlex.quote(a) for a in json.load(open('$W/inputs.json'))))" | sed "s#MEDIA#$W/mezz.mov#g")
( cd "$W" && eval ffmpeg -hide_banner -loglevel error -y $ARGS -filter_complex_script filter.txt -map "'[base]'" -map "'[aout]'" \
  -c:v libx264 -preset medium -crf 16 -pix_fmt yuv420p $C -c:a pcm_s16le base_mezz.mov )
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$W/base_mezz.mov")
# 4. Composite graphics and export with upload-friendly settings (stays under ~90 MB for 75s).
ffmpeg -hide_banner -loglevel error -y -i "$W/base_mezz.mov" -framerate 30 -i "$OV/f_%05d.png" \
  -filter_complex "[1:v]scale=1080:1920:flags=lanczos,format=rgba[o];[0:v][o]overlay=0:0:eof_action=pass,format=yuv420p[v]" \
  -map "[v]" -map 0:a -c:v libx264 -preset slow -profile:v high -level 4.1 -b:v 7M -maxrate 9M -bufsize 14M \
  -g 30 -keyint_min 30 -sc_threshold 0 -r 30 $C -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart -t "$DUR" "$OUT"
# 5. QA: even frame timing, audio present from 0:00, size.
ffprobe -v error -select_streams v -show_entries frame=pts_time -of csv=p=0 "$OUT" | awk 'NR>1{d=$1-p;if(d<0.03||d>0.037)c++}{p=$1}END{print "irregular frame gaps:",c+0; exit (c>0)}'
ffprobe -v error -show_entries format=duration,size -of compact "$OUT"
