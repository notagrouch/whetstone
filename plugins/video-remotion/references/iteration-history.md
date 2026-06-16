# Iteration history — 8-chapter educational series

Per-chapter render-version count, narration word count, locked render duration, and wpm. Source data is the educational series this skill was extracted from; content topics are abstracted.

## Iteration table

| Chapter | Render versions | Locked | Words | Duration (s) | WPM | Notes |
|---|---|---|---|---|---|---|
| 1 | v02-v08 (7 versions) | v08 | 273 | 93.1 | 176.0 | Foundational chapter; took 8 iterations to lock pacing + humanizer + safe-area + primitive-library |
| 2 | v01-v05 (5 versions) | v05 | 230 | 81.0 | 170.3 | Second chapter; storyboard markdown still authored; narration stabilized at v04 |
| 3 | v01-v05 (5 versions) | v05 | 224 | 84.7 | 158.7 | Voice-lock rule taught itself here (atempo violation, manuscript trim violation — both reverted) |
| 4 | v01-v05 (5 versions) | v05 | 259 | 96.7 | 160.6 | Narration locked at v01; v01-v05 were VISUAL iteration (anchor flags, slide layout) only |
| 5 | v01 (1 version) | v01 | 247 | 94.7 | 156.5 | Shipped on v01 — first single-iteration chapter |
| 6 | v01 (1 version) | v01 | 307 | 131.4 | 140.2 | Heaviest content of the series; shipped on v01 on PURE compositional reuse |
| 7 | v01 (1 version) | v01 | 228 | 81.6 | 167.7 | Shipped on v01 |
| 8 | v01 (1 version) | v01 | 217 | 82.0 | 158.7 | Shipped on v01 |

## Pace summary

- **WPM range across locked chapters:** 140.2 - 176.0
- **WPM mean:** 161.1
- **Outliers:**
  - Chapter 1 at 176 wpm (highest; densest delivery)
  - Chapter 6 at 140 wpm (lowest; longest duration 131s; heaviest content)
- **Verdict:** the cohort clusters around 161 wpm, not the 178 originally targeted from Chapter 1's first humanizer pass. Pace softened naturally across the series as humanizer trims removed compression density.

## Iteration compression — real or simpler-chapter effect?

**Real.** Three pieces of evidence:

1. Chapter 6 has the LONGEST manuscript (~2400 words) and LONGEST narration (307 words) of all 8 chapters, yet shipped on pure reuse of primitives built in Chapters 1-4. Heaviest content shipped on lightest new-code budget.

2. Chapters 1-2 added 6 chapter-specific animation primitives that have ZERO reuse. Chapters 3-4 added 4 primitives that became the workhorse vocabulary (each reused 3-4 times in Chapters 5-8). After Chapter 4, no new primitives were added.

3. Chapters 3-8 skipped formal storyboard markdown entirely — the structural decisions migrated into `chapters.ts` inline comments + beat consts. Storyboard layer collapsed.

**Counter-evidence:** Chapters 4, 5, 7 manuscripts ARE shorter (~1500w) than Chapters 1-3. Some "getting easier" was lighter source material. But the dominant effect was compositional, not topical.

## Humanizer recurring changes (Chapters 1-3, where versioned narrations exist)

Across the three chapters that went through multiple narration revisions (Chapter 1 v04 → v05 → v06 → locked, Chapter 2 v01 → v04 → locked, Chapter 3 v01 → v02 → locked), the recurring delta categories were:

| Category | Pattern | Frequency |
|---|---|---|
| Em-dash strip | em-dash → period or comma | All 3 chapters |
| Rule-of-three break | "Same trick. Same mechanism. Same answer." → trimmed | 2 of 3 |
| Status-flattery close cut | "which already puts you ahead of most people..." → cut | Chapter 1 only |
| AI-vocab swap | "beautiful, confident" → "confident, fluent" | Chapter 1 |
| Thesis-restatement outro | "Fluency in one beats..." → "Start with X this week" (concrete action) | Chapter 2 |
| Verbose intro trim | preamble taglines cut to lead with the example | Chapter 1 |

## Failure-mode catalog (renders thrown away)

Six known failure-mode events from production:

1. **Cover-text safe-area clip** — large display font on title slide pushed text past the 1080×1920 edge. Caught on phone preview, not in Remotion preview. Fixed in subsequent version via the 10px gutter rule.

2. **Tee-masked render crash** — a batch render reported exit code 0 but the actual `npx remotion render` command had crashed at frame 96/450. Root cause: pipe through `tee` swallowed the render command's exit code. Fixed by removing tee from render chains and capturing `EXIT=$?` immediately.

3. **Atempo voice-lock violation (Chapter 3 attempt)** — attempted to slow down the chapter narration using `ffmpeg atempo=0.85`. Sounded chipmunky AND violated the natural-voice series lock. Reverted to natural TTS, extended the timeline instead.

4. **Manuscript content trim violation (Chapter 3 attempt)** — attempted to trim 2 of the 5 pieces of the teaching device list to fit the time budget. The 5-piece list WAS the prize of the chapter. Reverted to the full 5 pieces and extended the timeline.

5. **Density-floor miss (Chapter 4 v01-v04)** — anchor-2 had a 5s static slide with VO only. Read as dead air. Added animation primitive (numbered checklist with type-on); shipped at v05.

6. **Stale-version overwrite (early Chapter 1 attempt)** — overwrote v02 with v03 in place to "keep the directory tidy". Lost the v02-shape decision that turned out to be the right one. Recovered from screen recording. Established the never-overwrite rule.

Every failure mode maps to one of the 12 disciplines in the parent SKILL.md.
