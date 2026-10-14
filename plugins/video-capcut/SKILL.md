---
name: video-capcut
description: CapCut lens for short-form vertical video. Edit a CapCut desktop project by writing its draft JSON directly (no UI automation) to add source footage, full-length text overlays and styled hooks. Use when footage already exists (talking head, phone clip, b-roll) and the deliverable is a CapCut project the creator will finish or export. Pair with video-discipline for pacing, storyboard and delivery-bundle rules.
license: MIT
prerequisites: [video-discipline]
provides: capcut-project-json-editing
---

# video-capcut

CapCut is a project-file target, not a renderer you drive. The desktop app stores each project as plain JSON on disk. An agent can build or amend a timeline by editing those files, which is faster and more repeatable than clicking through the UI.

The engine-agnostic rules (pacing, voice lock, density floor, version control, delivery bundle) live in **video-discipline**. This skill covers only what is specific to CapCut project files.

## When to use

- Source footage already exists and the job is overlays, hook cards, or captions on top of it
- The creator wants to open the result in CapCut and finish or export it there
- 9:16 short-form where a strong on-screen hook is the main edit

## When NOT to use

- Fully generated or animated video with TTS narration (use `video-remotion` or `video-hyperframes`)
- Anything that needs frame-accurate effects, keyframes, or transitions beyond a plain text overlay (do those in the app, then hand the file back)
- Exporting an MP4 headlessly (CapCut has no CLI render; export is a manual step in the app)

## Hard rules

1. **CapCut must be closed.** If it is running it overwrites the project on save. Check `pgrep -il capcut` first.
2. **Back up before writing.** Copy every file you touch to `<file>.pre-<change>`.
3. **Write both timeline copies.** The timeline lives at `<project>/draft_info.json` and `<project>/Timelines/<main_timeline_id>/draft_info.json`. Update `draft_meta_info.json` too (`tm_duration`, `draft_materials`).
4. **Check the project is not empty.** A freshly created project has `tracks: []` and no media. If so, import the source file path into the JSON yourself or ask for it. Never assume footage is present.
5. **Verify in the app.** JSON validity and a resolvable media path are necessary, not sufficient. The creator opening the project is the real check; say what was and was not verified.

## Pipeline

```
SOURCE PROBE -> PROJECT PROBE -> BUILD JSON -> BACKUP + WRITE -> OPEN IN APP -> ADJUST
```

| Stage | Action | Done when |
|---|---|---|
| SOURCE PROBE | `ffprobe` width, height, duration, audio | Orientation and duration known; canvas set to match the source |
| PROJECT PROBE | Read `draft_info.json`, `draft_meta_info.json`, `Timelines/project.json` | Track count, materials, and `main_timeline_id` known |
| BUILD JSON | Copy a segment and its `extra_material_refs` from a project that already has the item type, regenerate ids, set media path and durations | New segments reference materials that exist in `materials.*` |
| BACKUP + WRITE | Backups first, then both timeline copies and the meta file | All files parse as JSON |
| OPEN IN APP | Creator opens the project | Renders as intended, or a concrete defect is reported |
| ADJUST | Edit the same JSON values, re-write, repeat | Creator signs off |

## Overlay style defaults for vertical social

These are starting values for a hook card that has to read at thumbnail size. Adjust per channel style guide.

- All caps, 5 to 7 short lines, broken at phrase boundaries (explicit `\n`)
- Text block about 90% of frame width, centered vertically so it spans roughly the middle half of the frame
- White fill, heavy black outline, hard drop shadow, no background box
- One or two key words in a single accent color (yellow works against sky and foliage)
- Full clip duration unless the brief says otherwise

## Known gotchas

- `line_max_width` did not reliably wrap text. Put explicit newlines in the text string.
- Templates may carry a filled rounded background (`background_style: 1`). Zero it (`background_alpha: 0`, `background_style: 0`) for a plain overlay.
- `text_templates` materials are subtitle templates, not plain text. Copy from a segment whose `material_id` is in `materials.texts`.
- `line_spacing` units are not documented; change in small steps and look at the result.
- Text size in the JSON is not pixels. Calibrate from a screenshot of the first render, then scale.

## Tooling

`scripts/capcut_add_overlay.py` builds the video track and a full-length overlay in an empty project:

```bash
export CAPCUT_TEMPLATE_PROJECT="<name of a project that has a plain text segment>"
python3 scripts/capcut_add_overlay.py "<project-name>" "/path/to/video.mp4" "LINE ONE\nLINE TWO" "KEYWORD,OTHER"
```

It backs up every file it overwrites as `*.pre-overlay`. Run it with CapCut closed.

## References

- `references/project-json-schema.md` - file map, units, and the fields that mattered in practice

## Sibling skills

- **video-discipline** - required; pacing, storyboard, version control, delivery bundle
- **video-remotion**, **video-hyperframes** - generated-video engines; use these when there is no source footage

## License

MIT.
