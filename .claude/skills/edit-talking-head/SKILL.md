---
name: edit-talking-head
description: Edit a raw talking-head video (finance tips, @wealth_diet) into a TikTok/Reels-ready short in the style of a reference video. Storyboard first, then cut pauses, punch-in zooms, word-by-word captions, animated info cards and charts, and an end card. Use when the user shares a raw video (usually a Google Drive link) and asks to edit it, storyboard it, or copy a reference video's style.
---

# Edit a talking-head video

Proven workflow from the first project ("Retirement is a number", Oct 2026). The
`examples/` folder holds the exact files used there. Copy and adapt them; don't start from zero.

## Creator defaults (from the user's feedback)

- Handle: **@wealth_diet**. CTA: "Book a session · link in bio" button plus handle above the head.
  **No end card** by default (user dropped it on video 2); hold the last frame about 0.8s instead.
- Always send a **storyboard first** (PNG of real frames with mocked overlays), revise until they say "go".
- Headlines: **white Montserrat 800**, smaller rather than huge (the hook can be extra large, e.g. "AGE ≠ $$$").
- Cards: cream "paper" card (#fbf7ee), **no colored corner circles**, Montserrat, orange (#d9822b) for key words.
- **All cards and headlines sit above the speaker's head**, never over the face.
- **TikTok safe zone** on a 540×960 grid: 60px left, 120px right, 126px top, 320px bottom.
  Every graphic stays inside it. Draw it as a dashed box on storyboard frames.
- Captions: word by word (spoken word white, upcoming at 50% white), placed **low, around the mic hand**
  (top of caption block at y=650 of 960, moved down on video 2). That's slightly below the safe line; warn them to keep post descriptions short.
- Use real photos when the user asks for an image. Ask the user for them (stock sites are blocked); they send them in chat.
  Video 2 used polaroid-style photos (76px wide, white border, label, slight tilt) popping in one per word in a row above the head.
  `assets/calc.png` is their calculator cutout.
- Voice only, no music, unless asked. Slight warm grade. Loudness -14 LUFS.
- **No emojis anywhere**: not in post captions, titles, on-screen text, cards, buttons or storyboards. Use plain words or simple drawn icons instead.

## Environment notes (cloud sandbox)

- Drive files: the user must allow `drive.google.com` and `drive.usercontent.google.com` in the
  environment's network settings and share as "Anyone with the link". Then:
  `curl -sSL -o raw.mov "https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t"`.
  The Drive MCP connector cannot carry large videos.
- Hugging Face, Unsplash, Wikimedia and Pexels are blocked. GitHub and npm work.
- Transcription: `pip install sherpa-onnx`, then download Parakeet from GitHub:
  `https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8.tar.bz2`
  and run `scripts/transcribe.py <model_dir> audio16k.wav words.json`. That gives word timestamps.
- Montserrat: `npm pack @fontsource/montserrat` and use `files/montserrat-latin-{500..800}-normal.woff2`.
- Chromium for rendering: `/opt/pw-browsers/chromium`, Playwright at `NODE_PATH=/opt/node22/lib/node_modules`.
- Work in the scratchpad; never commit the videos.

## Steps

1. **Study** both videos: `ffprobe`, contact sheets (`fps=1,scale=180:-1,tile=8x3` with drawtext timestamps),
   a few full frames. List the reference's techniques (headline style, cards, captions, zooms, pacing, end card).
2. **Transcribe** the raw video. She often records each line 2 to 5 times: pick the last clean complete take of each line
   (list them as (start,end) TAKES, then cut pauses inside each take). Transcript word times can be ~0.1s early/late near cuts,
   so snap caption words to the nearest kept segment (0.35s before, 0.15s after) instead of dropping them.
   Then (16 kHz mono wav) and find pauses with
   `silencedetect=n=-35dB:d=0.3`.
3. **Check for burned-in text** the creator typed on their phone. Find its exact frames with
   `scripts/textspan.py`. Remove it by overlaying a feathered clean patch from a text-free frame
   (works when the camera is static), not with blur.
4. **Storyboard**: adapt `examples/storyboard_retirement_number.py` (thumbnail + CSS mock overlays,
   rendered to PNG with `scripts/shot.js`). Send it with SendUserFile and iterate.
5. **Edit plan**: adapt `examples/edit_retirement_number.py`:
   - Cut pauses ≥0.3s, keeping 0.10s after and 0.07s before speech.
   - **Snap every cut to the 30fps frame grid**, otherwise A/V and captions drift.
   - Punch-in zooms (1.12 to 1.2) on new points, anchored at y=0.38 so the head top stays put.
   - Use **one `-ss/-t` seeked input per segment**. Never `split` one input many ways, because it buffers GBs.
   - Map event times through the cut list into `timeline.json` (captions plus scene events).
   - Add `tpad`/`apad` of 2.5s for the end card.
6. **Graphics**: adapt `examples/overlay_retirement_number.html` (540×960 page, `renderAt(t)` is
   deterministic). Render a few test times with `scripts/render_overlay.js <dir> <out> 30 test 1.0 12 ...`,
   composite onto frames and inspect them, then render all frames (`... 30 all`, 4 parallel pages, DPR 2 = 1080×1920 PNGs).
   Watch for text overflowing the safe zone, wrapping titles, and empty cards (lines use display:none until revealed).
7. **Composite**: `overlay` the PNG sequence on the base, libx264 CRF 18 `-preset slow`, `+faststart`, AAC 192k.
8. **QA**: contact sheet of the final plus close-ups around any patch. Then send the MP4 with SendUserFile.

## 9. Post captions (after delivering the video)

Write both captions in chat, ready to paste. No emojis.

**TikTok** (SEO-optimized, exactly **5 hashtags**):
- Line 1 is the search phrase people type, phrased as a question or hook ("How much do you need to retire?").
- Next 2 to 3 short sentences repeat the main keywords naturally (retirement number, 4% rule, retire early) and give the takeaway.
- End with the CTA: "Want to retire before 70? Book a money coaching session, link in bio."
- 5 hashtags: mix broad and niche, e.g. #retirementplanning #4percentrule #financialfreedom #personalfinance #FIRE.
- Keep it short. A long description covers the on-screen captions, which sit just below the safe line.

**YouTube Shorts title**: **under 100 characters including hashtags**. Lead with the searchable question,
add the topic, then 2 to 3 hashtags including #shorts. Count characters with python before sending.

Example from the first video:
- TikTok: "How much do you need to retire? Retirement isn't an age, it's a number. Multiply your yearly spending by 25 to find your retirement number, then use the 4% rule to know when you can stop working. Want to retire before 70? Book a money coaching session, link in bio. #retirementplanning #4percentrule #financialfreedom #personalfinance #FIRE"
- YouTube (87 chars): "How Much Do You Need to Retire? The 4% Rule Explained #retirement #4percentrule #shorts"
