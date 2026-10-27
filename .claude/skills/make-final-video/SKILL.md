---
name: make-final-video
description: Render the final edited video for a @wealth_diet talking-head project after the storyboard is approved. Use ONLY when the user explicitly asks to make, render or export the final video (for example "make the final video"). Never use it on your own after a storyboard, after receiving photos, or after the user says the storyboard looks good without asking for the final video.
---

# Make the final video

Only run this when the user has explicitly asked for the final video.

**Always render with `render_final.sh`** (steps 0, 2, 4 and the timing QA in one script, exactly as it was when the
video played cleanly on TikTok and YouTube). Do not hand-write the ffmpeg render commands or cut from the raw HEVC file:
`render_final.sh <raw.mov> <work_dir> <overlay_frames_dir> <out.mp4>`. It refuses to render if any clip is under 0.5s. Everything before that
(planning, storyboards, revisions) lives in the `edit-talking-head` skill. Its style defaults, environment notes
and scripts apply here too: scripts are in `../edit-talking-head/scripts/`, worked examples in
`../edit-talking-head/examples/` (`*_low_spend_month_natural.*` is the latest approved style).

## Steps

0. **Make a frame-exact intermediate first.** iPhone footage is HEVC; seeking it with `-ss` lands a few frames early,
   so each clip starts with out-of-place frames. That caused stutter on TikTok/YouTube (worst at the start).
   Convert once and cut from this file instead of the raw:
   `ffmpeg -i raw.mov -map 0:v:0 -map 0:a:0 -vf fps=30,format=yuv420p -c:v libx264 -preset veryfast -crf 14 -g 1 -c:a pcm_s16le -ar 48000 mezz.mov`
   Final export: `-profile:v high -level 4.1 -g 30 -keyint_min 30 -sc_threshold 0 -r 30`, AAC 192k 48kHz stereo.

1. **Edit plan** (adapt `examples/edit_low_spend_month_natural.py`). 4K footage is fine: `render_final.sh` scales to 1080×1920.
   - TAKES = the chosen take for each line; cut pauses ≥0.3s inside takes (keep 0.10s after, 0.07s before speech).
   - **Snap every cut to the 30fps frame grid**, otherwise A/V and captions drift.
   - Punch-in zooms (1.1 to 1.15) on new points, anchored at the head-top height (`AY`) so the head top stays put.
   - **Merge slivers:** a zoom point that lands next to a pause cut creates a 1 to 2 frame clip that flashes a different
     zoom. Viewers see it as a glitch on TikTok/YouTube. Merge any clip under 0.25s into its contiguous neighbour
     (the examples do this) and assert the shortest clip is at least 0.5s before rendering.
   - **One `-ss/-t` seeked input per segment** with `trim=end_frame` and `atrim`/`apad`. Never `split` one input many ways.
   - Snap caption words to the nearest kept segment (0.35s before, 0.15s after), fix transcript slips by hand.
   - No end card: hold the last frame about 0.8s (`tpad`/`apad`).
   - Writes `work/filter.txt`, `work/inputs.json`, `overlay/timeline.json`.
2. **Base render**: done by `render_final.sh` from `mezz.mov` (never the raw). Check the duration equals the plan. Tag color on every encode: `-colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv`.
3. **Graphics** (adapt `examples/overlay_low_spend_month_natural.html`; reuse the approved storyboard's overlay as is):
   `node ../edit-talking-head/scripts/render_overlay.js <overlay_dir> <out_dir> 30 all`
   (`NODE_PATH=/opt/node22/lib/node_modules`, 4 parallel pages, 1080×1920 PNGs).
4. **Composite and export**: done by `render_final.sh` (7 Mbps cap, keyframe every 1s, AAC 192k 48kHz).
   **Keep the file under 90 MB**: the Claude phone app won't offer Save Video for files over about 100 MB.
5. **QA**: list clip lengths from `inputs.json` (no clip under 0.5s); `freezedetect` should only flag the end hold;
   frame timestamps evenly spaced. Then a contact sheet (`fps=1/3,scale=216:384,tile=8x3`) and close-ups. Check graphics are centered over the head,
   inside the safe zone, never over the face, and captions read correctly.
6. **Deliver**: copy to a clear filename (`wealth_diet_<topic>.mp4`) and send with SendUserFile.
7. **Post captions** in chat, ready to paste, no emojis (rules in `edit-talking-head`, step 9):
   TikTok with exactly 5 hashtags and SEO-first line; YouTube Shorts title under 100 characters including hashtags
   (count with python).
