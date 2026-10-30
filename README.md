# study-kits

Self-contained HTML exam study kits, one folder per course.

## Layout

```
index.html          home page; reads courses.json and links every kit
courses.json        list of courses and their kits (edit this when adding a kit)
<COURSECODE>/       one folder per course, e.g. MECHENG736/
  <part>-<topic>.html   one standalone page per exam part/topic
```

## Adding a kit (instructions for Claude sessions)

1. Put the HTML file in `<COURSECODE>/` (create the folder if new). Use lowercase-hyphenated
   file names, e.g. `part3-hri-devices.html`.
2. Each kit is a single self-contained HTML file (inline CSS/JS; Google Fonts allowed).
   Reuse the styling of `MECHENG736/part1-eeg-sleep.html` so kits look consistent:
   tabs for Plan / Notes / Numbers or Formulas / Calculations / Quiz or Cards / Past papers.
   **Phone layout:** copy the `<style id="mobile-fit">` block (end of `<head>`) and the
   `<script id="mobile-fit-js">` block (end of `<body>`) from any existing kit into the new one,
   unchanged. They wrap the tab bar onto extra lines and turn tables into stacked cards on phones.
   Check the page at ~390px wide before pushing: no sideways scrolling, every tab visible.
3. Add an entry to `courses.json` (new course object, or a new item in its `kits` array).
4. Commit with a message like `Add MECHENG736 part 3 kit` and push to `main`.

Kits are also published as private Claude artifacts; this repo is the shared copy.

## Read-aloud audio (optional)

To turn tabs of a kit into MP3s (e.g. Bookwork and Definitions), follow `tools/audio/README.md`.
Audio lives in `<COURSECODE>/audio/`.

## Past paper PDFs

Follow `MATHS350/topology-exam-kit.html` (see the "Original papers (PDF)" card at the top of its Past papers tab):

1. Put the PDFs in `<COURSECODE>/past-papers/`, named `<year>-exam.pdf`, `<year>-exam-solutions.pdf`,
   `<year>-test.pdf` (lowercase, hyphens). Only commit papers that are actually in the source files.
2. At the top of the kit's Past papers tab, add a card headed "Original papers (PDF)" with a
   `<ul class="paperlist">` of links (`target="_blank" rel="noopener"`), one line per year,
   noting anything missing (e.g. "no official solutions").
3. For courses split into several kits (MECHENG736 parts, MATHS332 parts), the PDFs live once in
   the course's `past-papers/` folder and every part's kit links to them.
4. If the kit doesn't have the `.paperlist` / `.muted` CSS yet, copy those rules from the MATHS350 kit.
