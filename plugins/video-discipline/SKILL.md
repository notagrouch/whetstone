---
name: video-discipline
description: Engine-agnostic production discipline for short-form educational videos (60-130s, IG-Reels-shape) with TTS narration. Covers pacing measurement, voice lock, density floor, pace adjustment, storyboard structure, version control, iteration compression, humanizer-grep gate, and failure-mode catalog. Use as the shared core for any rendering engine (Remotion, HyperFrames, others). Pair with an engine-specific sibling skill (video-remotion or video-hyperframes) for build-stage details.
license: MIT
prerequisites: []
provides: video-discipline-vocabulary
---

# video-discipline

Hard-won, engine-agnostic production discipline for short-form educational videos (60-130s, IG-Reels-shape) with TTS narration. Extracted from production of an 8-chapter educational series (26 distinct renders, foundational chapter took 8 iterations to lock; later chapters shipped on v01 by encoding these disciplines upfront).

This skill is the **shared core**. Engine-specific details (Remotion's `--concurrency=2`, HyperFrames' `data-*` attribute model, render-CLI quirks) live in sibling skills:

- **video-remotion** — Remotion-specific receipts (concurrency, ChapterReel-style monolith, text safe-area at 1080×1920)
- **video-hyperframes** — Thin lens over HeyGen's HyperFrames for short-form work

This skill is **opinionated**. The opinions are receipts of what cost us iteration tax. Follow them or pay the tax yourself.

## When to use

- Planning a multi-chapter educational video series (any topic) for IG Reels / TikTok / YouTube Shorts
- Adding a new chapter to an existing series and want to avoid re-paying the iteration tax
- Diagnosing why a chapter "feels off" - is it pace, density, or voice?
- Picking between two rendering engines (consult this skill's engine-selection guidance below)
- Shipping the first chapter of a new series and wondering what to lock vs. leave flexible

## When NOT to use

- Long-form video (>3 min) - pacing math and density floor differ
- Live-action / camera-based video - this skill is illustrated/animated + TTS narration only
- One-off explainer with no series continuity - the lock/reuse mechanics don't apply

## Engine selection (hard rule, not a suggestion)

| Use case | Engine | Sibling skill |
|---|---|---|
| Series with >3 chapters, custom primitive library, React/TSX team | Remotion | `video-remotion` |
| Single-shot short-form (<90s), social/explainer content, leverage prebuilt blocks | HyperFrames | `video-hyperframes` |
| Active series mid-flight | Stay on the engine you started — never auto-migrate | Whichever sibling you're already using |

**Reason:** the 12 disciplines below apply to any HTML-or-React-based renderer that uses headless Chrome + FFmpeg under the hood. But series work amortizes a custom primitive library; one-shot work benefits from prebuilt catalogs. Choose by use case, not preference.

## The pipeline (5 stages, mandatory order)

```
FACTS → MANUSCRIPT → SCENE BREAKDOWN → STORYBOARD → BUILD
```

Each arrow is a stage gate. Skipping a stage forces a rebuild at a later stage. Words drive timing drives beats drives scenes — never reorder.

| Stage | Input | Output | Lock criterion |
|---|---|---|---|
| FACTS | Topic brief | `facts/<chapter>-facts.md` — concrete teaching devices (analogies, mechanisms, contrasts) | Every device is concrete, not a slogan |
| MANUSCRIPT | Facts doc | Long-form chapter content (~1500-2400 words) | Teaching shape locked: hook, 3 anchors, close |
| SCENE BREAKDOWN | Manuscript | Beat-by-beat decomposition: ~5-6 beats × 2.5-3.5s each | Every static beat >3-4s has an animation plan |
| STORYBOARD | Scene breakdown | Markdown storyboard (or inline schema entry once schema stabilizes) | Anchor flags assigned; beat timings sum to target |
| BUILD | Storyboard | Rendered video (1080×1920 + 2x + cover.png + caption) | Render verified via ffprobe + visual safe-area check |

**After the first 2-3 chapters, the storyboard markdown can collapse into an inline code-config schema entry** — once the 5-beat structure and anchor vocabulary stabilize, the structural decisions migrate into code comments + beat consts. This is iteration compression at the storyboard layer.

## The 10 engine-agnostic disciplines

(Two more disciplines — text safe-area enforcement and render-CLI configuration — are engine-specific. See `video-remotion` or `video-hyperframes`.)

### 1. Pacing target — lock the first chapter's wpm as the series anchor

Measure the locked first chapter's words-per-minute and use it as the **measurement instrument** for every subsequent chapter, not as a hard target every chapter must hit.

```bash
WORDS=$(wc -w < narrations/chapter-1.txt)
DURATION=$(ffprobe -v error -show_entries format=duration -of csv=p=0 renders/chapter-1-v-locked/chapter-1-locked-1080.mp4)
WPM=$(python3 -c "print(round($WORDS / ($DURATION / 60), 1))")
echo "Series anchor wpm: $WPM"
```

**Why locked wpm matters:** chapter-to-chapter pace drift is barely perceptible (~10 wpm at the chapter level). Reaching for a pacing fix on a 10-wpm gap is over-correction. The locked wpm is the diagnostic tool that tells you when a difference is real vs. noise.

**Expected variance:** target wpm minus 20 to plus 5 is the normal corridor. Outliers indicate dense content (extend timeline) or thin content (let it breathe — don't pad).

### 2. Voice + TTS — once locked, never post-process

Once a natural-voice TTS baseline is locked for a series, **never apply downstream audio time-stretch** — no ffmpeg `atempo`, no rubberband, no SoX, no DAW timestretch. The lock is a series-level invariant.

**Escape valves when a chapter feels rushed:**
1. Extend the timeline (preferred; see discipline #4)
2. Rewrite the manuscript section and re-render TTS (correct upstream)
3. Accept the variation (a 10-wpm spread across chapters is fine)

**Anti-pattern detected in production:** "atempo=0.85 to slow it down" — sounds chipmunky AND violates the voice lock. Never reach for this.

### 3. Animation density floor — every static beat >3-4s gets a layer

At IG-scroll cadence, a static slide held for more than 3-4 seconds with only VO reads as dead time. **HOOK and ENDCARD beats tighten the floor to ~2s** because they bookend attention.

Build a reusable animation primitive library (carousel, reveal, counter, type-on, gradient sweep, comparison-cards, numbered-checklist, contrast-list, pushback-quotes). Compose later chapters from primitives instead of hand-crafting each beat.

**Diagnostic question for "this beat feels flat":** is there visual change happening between frame 1 and frame N? If no, you have a density-floor violation, not a pacing problem.

### 4. Pace adjustment — extend the timeline, never trim the manuscript

When a chapter feels rushed, the hierarchy is:

1. **Extend** the timeline so beats breathe
2. **Adjust beat boundaries** so dense sections get more frame budget
3. **Add visual breathing room** (silence + held-frame animation)
4. **Re-prompt TTS** for the dense section with explicit pacing markers
5. **Content cuts** — ONLY with explicit author sign-off

The manuscript content is load-bearing teaching material. Trimming it to fix pacing destroys the chapter's value. **Cost of an over-long video: small. Cost of a content cut: large.**

The 5-piece teaching device is the prize of the chapter — never trim it to fit the time budget. Extend the time budget instead.

### 5. Storyboard structure — 5 beats, anchors selected at scene-breakdown time

The 5-beat structure for a 60-130s chapter:

```
intro (3-4s)  →  anchor-1 (20-25s)  →  anchor-2 (25-30s heaviest)  →  anchor-3 (20-25s)  →  close (5s)
                                                                                            (+ qrCard 5s, optional)
```

**Anchor selection rule:** each anchor maps to a **teaching device from the manuscript** (concrete analogy / mechanism / contrast), NOT a summary slogan. Slogan-anchors fail at the scene-breakdown stage because they have no visual to attach to.

**Anchor-2 is the heaviest beat.** Put the chapter's load-bearing concept there. Anchor-1 sets up; anchor-3 reinforces; anchor-2 teaches.

### 6. Version control — `vNN` from the FIRST render, never overwrite

Write to versioned filenames from the very first render. Never overwrite to "save space" or "keep the directory tidy."

```
renders/
  chapter-1-v01/
    chapter-1-v01-1080.mp4
    chapter-1-v01-2x.mp4
    chapter-1-v01-cover.png
    chapter-1-v01-slide-N.png
  chapter-1-v02/
    ...
```

**Why:** earlier versions are NOT recoverable from source code alone — re-rendering takes minutes and outputs differ subtly (font availability, randomness in animations, ffmpeg version). The rendered file is the only faithful snapshot of that moment.

**The version number is also the lock receipt.** When you revert from v04 back to a v02-shape decision, you spawn `v05` capturing the revert — you don't overwrite v02.

### 7. Cover image generation — render alongside, not after

The cover is the thumbnail viewers see in their feed before they tap. It deserves the same animation-pipeline treatment as the chapter itself.

**Pattern:** add a `chapter-N-vN-cover.png` render output in the same composition config. Use the chapter's hero anchor (anchor-2's visual at the frame where it's most legible) as the cover frame, not the title slide.

**Anti-pattern:** generating covers in Photoshop or Figma after the fact. Drift inevitable; brand becomes inconsistent; iteration loop adds a manual step.

### 8. Iteration compression — encode Chapter 1's lessons at the top of the skill

Chapter 1 of a new series will take many iterations (8 was real). Chapters 2-3 will take 3-5 iterations. By Chapter 4-5, single-iteration shipping becomes possible IF the lessons from Chapter 1's iteration have been:

1. **Codified** — written into the skill (this doc)
2. **Tooled** — animation primitives library expanded once, reused thereafter
3. **Templated** — code-config schema embeds the 5-beat structure so chapter authors can't accidentally skip beats

**Diagnostic:** if you're iterating each new chapter the same number of times, the lessons aren't sticky. Audit what's NOT being reused and either reuse it or kill it.

**Compositional reuse beats simpler chapters.** The heaviest manuscript in a series can ship on the lightest new-code budget IF the primitive library is complete by Chapter 4. Do not confuse "Chapter 6 was easier" with "Chapter 6 was structurally simpler" — measure manuscript word count + concept count to verify.

### 9. Humanizer-grep gate — empty grep is necessary, not sufficient

Before declaring narration done, run the AI-tell grep:

```bash
grep -iE "delve|leverage|robust|vibrant|tapestry|comprehensive|seamless|in the realm of|landscape|when it comes to|it's important to note|i hope this helps|ultimately,|in conclusion|moreover,|furthermore,|additionally," narrations/chapter-N.txt
```

Empty result passes. Any hit forces rewrite.

**Caught by this grep:** the worst AI-tell vocabulary.

**NOT caught by this grep — needs a separate human pass:**
- Em-dash overuse (em-dashes are the single most reliable AI-slop tell)
- Rule-of-three padding ("Same trick. Same mechanism. Same answer.")
- "It's not just X — it's Y" construction
- Status-flattery closes ("which already puts you ahead of most people...")
- Writerly preamble taglines ("Three things you actually need to know...")

Run the grep AND a separate human read for these. Both gates must pass.

See `references/humanizer-banned-tokens.md` for the full pattern and the rationale per token.

### 10. Failure-mode catalog — the negative corpus IS half the lesson

Every render thrown away taught something. Catalog them. The catalog itself is part of the skill.

See `references/failure-mode-catalog.md` for the working catalog with seven canonical failure modes.

**Pattern:** every failure mode maps to a discipline above. When a new failure type appears, add a row to the catalog AND add the prevention to the matching discipline.

## Anti-patterns (do-NOT shortcuts)

- **Atempo / rubberband / SoX to "fix pace"** — voice lock violation; see #2
- **Trimming manuscript to fit time budget** — content cuts are an author decision, not a build-time fix; see #4
- **Skipping storyboard for "simple chapters"** — when storyboard skips, ad-hoc scene decisions made at build time always cost more iterations; see #5
- **Photoshop cover after render** — drift; see #7
- **Overwriting render output** — loses the snapshot; see #6
- **Em-dashes in TTS narration** — pause longer than commas, sound stagey, are AI-slop signature; see #9

## Worked examples

The three worked examples below show the pipeline applied to three different chapter shapes. The teaching content is abstracted to teaching-shape; the pipeline mechanics are real production records.

### Example A — first chapter of a new series (foundational + heavily iterated)
<!-- abstracted-from: jc-ch1-mental-model -->

A series-opening chapter teaching three concepts about a technical topic. ~280 words of narration, target ~95 seconds, locked at v08 after 8 iterations.

**Stage 1 (FACTS):** three concrete teaching devices identified — a smartphone autocomplete analogy, a distribution curve illustrating the difference between predicting and reasoning, and an oracle-vs-assistant framing for the mindset shift.

**Stage 2 (MANUSCRIPT):** ~1900 word long-form chapter. Six H2 sections (intro / device 1 / device 2 / device 3 / synthesis / close).

**Stage 3 (SCENE BREAKDOWN):** 5 beats: intro (3.5s) / anchor-1 autocomplete (22s) / anchor-2 distribution curve heaviest (28s) / anchor-3 framing shift (24s) / close (7s). Total target: 84.5s. Actual locked: 94.5s — extended at anchor-2 + close per discipline #4.

**Stage 4 (STORYBOARD):** full markdown storyboard (~600 lines) — the heaviest storyboard of the series because primitives didn't exist yet. Three chapter-specific animation primitives identified for build.

**Stage 5 (BUILD):** v01 → v08 iteration trail:
- v01-v03: animation primitives built and refined
- v04: narration humanizer pass — em-dash strip, AI-vocab swap, status-flattery close cut
- v05: pace adjustment — anchor-2 extended by 6s
- v06: cover image swapped from title-frame to mid-anchor-2 hero frame
- v07: safe-area fix on close beat
- v08: locked — final ffprobe verification

**What this chapter taught the series:** the entire discipline catalog. Every later chapter shipped faster because v01-v08 of this one paid the tuition.

### Example B — middle chapter (compositional reuse, single-iteration ship)
<!-- abstracted-from: jc-ch6-the-traps -->

A middle chapter teaching one concept on top of the foundational mental model from Example A. ~310 words narration, target ~130 seconds, shipped on v01.

**Stage 1 (FACTS):** one core concept with three concrete examples of common mistakes (the "traps"). The teaching device is the contrast between expectations and reality.

**Stage 2 (MANUSCRIPT):** ~2400 word long-form chapter — actually the LONGEST manuscript in the series. Eight H2/H3 sections covering the trap categories.

**Stage 3 (SCENE BREAKDOWN):** 5 beats + qrCard. Anchor-2 is the trap-comparison sequence (heaviest).

**Stage 4 (STORYBOARD):** **inline in the code-config schema** — no separate markdown storyboard. By this point in the series, the 5-beat structure and anchor-flag schema were stable enough that the structural decisions migrated to code comments + beat consts. This is iteration compression at the storyboard layer.

**Stage 5 (BUILD):** v01 = locked. Three reused primitives from earlier chapters: contrast-list, pushback-quotes, example-carousel. Zero new animation primitives.

**What this chapter demonstrates:** the heaviest content can ship on the lightest new-code budget if the primitive library is complete. Compositional reuse > simpler chapters.

### Example C — chapter that taught the voice-lock rule (iteration cost from a violated rule)
<!-- abstracted-from: jc-ch3-prompting -->

A chapter where natural-voice TTS produced output that felt slightly faster than the series baseline. An early iteration attempted to fix this with `ffmpeg atempo=0.85` downstream of TTS, plus manuscript trim of a 5-piece teaching device.

**Both fixes were wrong.** The chapter author caught it:

> "I want the voice to be natural. did we not lock that in? why would it sound chipmunkish?"

And separately:

> "if you need to pace it, you extend the video. the length can be variable, the voice must be consistent."

**Resolution:** reverted to natural Kore TTS, restored the 5-piece teaching device, extended the timeline by ~10s, locked as v05.

**Lessons this chapter generated:**
- Discipline #2 (voice lock invariant; never atempo)
- Discipline #4 (extend the timeline, never trim the content)
- The 5-piece teaching device was the prize of the chapter — trimming it would have destroyed the chapter's value

This chapter's failure became two of the disciplines above.

## References

- `references/humanizer-banned-tokens.md` — full grep pattern + per-token rationale + what the grep does NOT catch
- `references/failure-mode-catalog.md` — seven canonical failure modes with prevention mapping
- `case-studies/` (optional) — authorized real-content extensions per source. New skills start empty; add files only when the source is approved for public disclosure.

## Sibling skills

- **video-remotion** — Remotion-specific receipts (concurrency=2, ChapterReel-style monolith, 10px text safe-area, atempo-violation case study). Required when using Remotion as the renderer.
- **video-hyperframes** — Thin lens over HeyGen's HyperFrames for short-form work. Required when using HyperFrames.

## Compatibility

- Claude Code (Anthropic Agent Skills spec)
- GitHub Copilot CLI
- Cursor
- Gemini CLI
- Any MCP-aware agent client

## License

MIT.
