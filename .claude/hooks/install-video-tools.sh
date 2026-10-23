#!/bin/bash
# Installs FFmpeg, yt-dlp and HyperFrames for Claude Code cloud sessions.
set -e
[ "$CLAUDE_CODE_REMOTE" = "true" ] || exit 0

if ! command -v ffmpeg >/dev/null; then
  apt-get update -qq && apt-get install -y -qq ffmpeg
fi
command -v yt-dlp >/dev/null || pip install -q -U yt-dlp
command -v hyperframes >/dev/null || npm install -g -q hyperframes
