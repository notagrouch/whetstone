# CapCut project JSON: working notes

Observed on CapCut desktop 8.9.1 (macOS). Not an official spec; verify against a project the app wrote itself.

## File map

Project root: `~/Movies/CapCut/User Data/Projects/com.lveditor.draft/<project>/`

| File | Role |
|---|---|
| `draft_info.json` | Timeline content (tracks, segments, materials) |
| `Timelines/<id>/draft_info.json` | Same timeline, per-timeline copy. Keep identical to the root copy |
| `Timelines/project.json` | Timeline index; `main_timeline_id` gives `<id>` |
| `draft_meta_info.json` | Project metadata: `tm_duration`, `draft_materials` (imported media list) |
| `*.bak`, `template-2.tmp` | App-managed backups; leave alone |

## Units and layout

- Times are microseconds. 8.04 s is `8041367`.
- `canvas_config` carries `width`, `height`; set it from the source (1080x1920 for vertical).
- `tracks[]` each have `type` (`video`, `text`, `audio`...) and `segments[]`. A segment has `target_timerange {start,duration}`, `source_timerange` (null for text), `clip` (scale, transform, rotation, alpha), `material_id`, and `extra_material_refs`.
- `clip.transform` x and y are normalized to the canvas, 0,0 is center.
- Every id referenced by a segment must exist in `materials.<kind>[]`. Regenerate uuids when copying.

## Text materials

- `materials.texts[]` entries hold `content`, a JSON **string**: `{"styles":[...],"text":"..."}`.
- Each style has a `range` [start,end) in characters of `text`, a `fill` color (0 to 1 floats), `size`, optional `strokes` and `shadows`.
- Newlines in `text` are honored; automatic wrap via `line_max_width` was unreliable.
- Background box fields: `background_style`, `background_color`, `background_alpha`.

## Video materials

- `materials.videos[]`: `path`, `duration`, `width`, `height`, `has_audio`, `material_name`, `local_material_id`.
- The video segment also references helper materials (speeds, canvases, sound channel mappings, and so on) through `extra_material_refs`. Copy them with the segment.

## Safety checklist

1. App closed
2. Backups written
3. Both timeline copies written and parse as JSON
4. Media path exists on disk
5. Opened in the app by the creator before calling it done
