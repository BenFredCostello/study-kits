# Read-aloud audio for a kit

Turns tabs of a kit (e.g. Bookwork, Definitions) into MP3s that read the page in order, so you
can listen while reading. Offline TTS (Piper), works inside a Claude cloud session.

## Steps (for Claude sessions)

1. Pick the tab ids to read: open the kit HTML and find the `<section id="...">` for each tab
   (e.g. `bookwork`, `defs`, `notes`). Tabs that are mostly tables, calculations or quizzes read badly; skip them.
2. Make the spoken scripts:
   ```bash
   cd tools/audio
   python3 make_script.py ../../<COURSE>/<kit>.html out bookwork:Bookwork defs:Definitions
   ```
3. **Read the .txt files before rendering.** `speak()` in `make_script.py` turns symbols into words
   (⊆ → "is a subset of", cl → "the closure of", f⁻¹ → "f inverse", ⇒ → "which implies",
   [a,b] → "the closed interval a to b", {x} → "the set x"). New courses bring new notation:
   grep for leftover non-ASCII (`grep -P '[^\x00-\x7F]' out/*.txt`) and add rules to `speak()`
   (symbol table, `words` regex list) until each line reads naturally aloud. Commit the improved script.
4. Render:
   ```bash
   bash make_audio.sh out <COURSE>        # needs ffmpeg; installs piper-tts + downloads the voice once
   ```
   Roughly 1 minute of audio per 150 words; rendering takes a few minutes.
5. Send the MP3s to the user, and commit them to `<COURSE>/audio/` (64 kbps mono, about 0.5 MB a minute).

## Notes

- The voice (`en-us-lessac-medium`) comes from a GitHub release asset because Hugging Face is
  blocked from Claude sessions. If that ever fails, `pip download piper-tts` still works but needs a voice.
- `make_script.py` skips `<table>`, `<pre>`, `.calc`, SVGs and quiz widgets. Put anything that must be
  heard in `<p>`, `<li>`, `<dt>/<dd>` or `<summary>`.
- Dense formulas (homology boundary maps, long chains) never sound great; say so to the user.
