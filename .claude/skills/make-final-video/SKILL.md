---
name: make-final-video
description: Render the final edited video for a @wealth_diet talking-head project after the storyboard is approved. Use ONLY when the user explicitly asks to make, render or export the final video (for example "make the final video"). Never use it on your own after a storyboard, after receiving photos, or after the user says the storyboard looks good without asking for the final video.
---

# Make the final video

Only run this when the user has explicitly asked for the final video. Everything before that
(planning, storyboards, revisions) lives in the `edit-talking-head` skill. Its style defaults, environment notes
and scripts apply here too: scripts are in `../edit-talking-head/scripts/`, worked examples in
`../edit-talking-head/examples/` (`*_high_income_poverty.*` is the latest approved style).

## Steps

1. **Edit plan** (adapt `examples/edit_high_income_poverty.py`):
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
2. **Base render** (background): ffmpeg with the inputs and `-filter_complex_script`, libx264 CRF 16. Check the
   duration equals the plan. Tag color on every encode: `-colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv`.
3. **Graphics** (adapt `examples/overlay_high_income_poverty.html`; reuse the approved storyboard's overlay as is):
   `node ../edit-talking-head/scripts/render_overlay.js <overlay_dir> <out_dir> 30 all`
   (`NODE_PATH=/opt/node22/lib/node_modules`, 4 parallel pages, 1080×1920 PNGs).
4. **Composite**: overlay the PNG sequence on the base, libx264 `-preset slow -b:v 7M -maxrate 9M -bufsize 14M -g 60`,
   `+faststart`, AAC 160k, `-t` = base duration. **Keep the file under 90 MB**: the Claude phone app won't offer
   Save Video for files over about 100 MB (a 106 MB file could not be saved; 67 MB and 95 MB could).
5. **QA**: list clip lengths from `inputs.json` (no clip under 0.5s); `freezedetect` should only flag the end hold;
   frame timestamps evenly spaced. Then a contact sheet (`fps=1/3,scale=216:384,tile=8x3`) and close-ups. Check graphics are centered over the head,
   inside the safe zone, never over the face, and captions read correctly.
6. **Deliver**: copy to a clear filename (`wealth_diet_<topic>.mp4`) and send with SendUserFile.
7. **Post captions** in chat, ready to paste, no emojis (rules in `edit-talking-head`, step 9):
   TikTok with exactly 5 hashtags and SEO-first line; YouTube Shorts title under 100 characters including hashtags
   (count with python).
