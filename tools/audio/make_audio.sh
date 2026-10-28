#!/usr/bin/env bash
# Render every .txt in DIR to an MP3 with Piper TTS (offline).
# Usage: bash make_audio.sh DIR PREFIX      e.g. bash make_audio.sh out MATHS350
set -euo pipefail
DIR=${1:?dir with .txt scripts}; PREFIX=${2:?file prefix, e.g. course code}
VOICE_DIR=${VOICE_DIR:-/tmp/piper-voice}
if [ ! -f "$VOICE_DIR/en-us-lessac-medium.onnx" ]; then
  mkdir -p "$VOICE_DIR"
  # Hugging Face is blocked in Claude sessions; this GitHub release asset works.
  curl -sL https://github.com/rhasspy/piper/releases/download/v0.0.2/voice-en-us-lessac-medium.tar.gz | tar xz -C "$VOICE_DIR"
fi
python3 -c "import piper" 2>/dev/null || pip install -q --break-system-packages piper-tts
for f in "$DIR"/*.txt; do
  n=$(basename "$f" .txt)
  grep -v '^$' "$f" | python3 -m piper -m "$VOICE_DIR/en-us-lessac-medium.onnx" --sentence-silence 0.45 -f "$DIR/$n.wav"
  ffmpeg -y -loglevel error -i "$DIR/$n.wav" -ac 1 -b:a 64k -metadata title="$PREFIX $n" "$DIR/$PREFIX-$n.mp3"
  rm "$DIR/$n.wav"
  echo "$DIR/$PREFIX-$n.mp3  $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$DIR/$PREFIX-$n.mp3" | cut -d. -f1)s"
done
