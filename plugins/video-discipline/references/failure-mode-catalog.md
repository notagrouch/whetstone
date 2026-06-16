# Failure-mode catalog

Every render thrown away during the source 8-chapter series production. Each row maps to a discipline in the parent `SKILL.md` that prevents the recurrence.

## Canonical failure modes

| Category | Symptom | Root cause | Discipline that prevents |
|---|---|---|---|
| **Safe-area clip** | Text clipped on cover or final slide | Display font + shadow exceeds output frame dimensions | Engine-specific (`video-remotion` discipline #6) |
| **Tee-masked render crash** | Exit code 0 but video truncated mid-chapter | Pipe through `tee` swallowed exit code | Engine-specific (`video-remotion` discipline #7) |
| **Audio post-process violation** | Chipmunk voice on v03 attempt | Reached for `atempo` to "fix pace" | #2 (voice + TTS lock) |
| **Manuscript content trim** | Teaching device removed to fit time budget | Confused "feels rushed" with "needs trim" | #4 (pace adjustment hierarchy) |
| **Density-floor miss** | Beat 3 reads as dead air | No animation layer for 5s static slide | #3 (animation density floor) |
| **Stale-version overwrite** | Lost a v02-shape decision | Overwrote v02 with v03 in place | #6 (version control: `vNN` never overwrite) |
| **Slogan-anchor** | Anchor has no visual to attach to | Chose anchor at storyboard stage, not scene-breakdown | #5 (storyboard structure — anchors are teaching devices) |

## Adding new failure modes

When a new failure type appears in production, add a row here AND add the prevention rule to the matching discipline in the parent SKILL.md. The catalog is a forcing function: if a failure can't be prevented by any existing discipline, the discipline list itself needs a new entry.

## Pattern: the negative corpus is half the lesson

Each row above isn't just a war story. It's an active reminder that:

1. **Every failure mode maps to a discipline.** If a future failure doesn't map cleanly, the discipline list is incomplete.
2. **The version number (`vNN`) is the receipt trail.** Reading a render-history directory listing should tell you which failures happened when.
3. **Catching a failure at storyboard time is 10x cheaper than catching it at render time.** Most rows above were caught LATE — at v04, v05, v08 — because the storyboard discipline wasn't yet sharp enough to surface the defect upstream.

## Cross-engine notes

| Failure | Remotion-specific? | HyperFrames-specific? |
|---|---|---|
| Safe-area clip | Yes — Remotion's React preview hides this; production phone render reveals it | Likely similar — HyperFrames uses headless Chrome; same root cause |
| Tee-masked render crash | Yes — specific to `npx remotion render` CLI exit-code handling | HyperFrames may have analogous `npx hyperframes render` exit-code traps; verify before reuse |
| Audio post-process | Engine-agnostic — applies to any TTS pipeline | Same |
| Manuscript trim | Engine-agnostic — applies to any narration-driven production | Same |
| Density-floor miss | Engine-agnostic — applies to any IG-Reels-shaped output | Same |
| Stale-version overwrite | Engine-agnostic — applies to any file-output pipeline | Same |
| Slogan-anchor | Engine-agnostic — applies to any storyboard/scene-breakdown workflow | Same |

Engine-specific failures stay in the engine-specific sibling skill's catalog. The catalog here covers the 5 engine-agnostic ones; the engine-specific siblings extend it with their renderer's quirks.
