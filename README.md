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
3. Add an entry to `courses.json` (new course object, or a new item in its `kits` array).
4. Commit with a message like `Add MECHENG736 part 3 kit` and push to `main`.

Kits are also published as private Claude artifacts; this repo is the shared copy.
