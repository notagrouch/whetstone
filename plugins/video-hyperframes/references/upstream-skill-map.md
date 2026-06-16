# Upstream HyperFrames skill map

Routing guide: which of HyperFrames' 16 skills covers what, and when our video-hyperframes lens should defer vs. override.

**Pinned SHA:** `479184ecf0bc5d9c02e621ea6019fa7d2c417ab8` (verify before deep-linking specific lines: `https://github.com/heygen-com/hyperframes/tree/479184ecf0bc/skills/<skill>/`)

## Skill inventory (16 total)

### Core technical contract

| Upstream skill | Covers | Our lens |
|---|---|---|
| `hyperframes` | Entry-point router skill — directs to other skills based on intent | Defer — use upstream router |
| `hyperframes-core` | HTML composition contract: `data-*` attributes, clips, tracks, sub-comps, determinism rules | Defer — this is the technical spec |
| `hyperframes-cli` | Dev loop: lint, validate, preview, render | Defer for CLI; reference our discipline #6 for versioned output naming |
| `hyperframes-animation` | Motion adapters: GSAP, Lottie, Three, Anime.js, CSS, WAAPI | Defer — animation runtime details |
| `hyperframes-creative` | Palettes, typography, narration register, beat planning, audio-reactive | **Partial defer** — use for palette/typography; OVERRIDE narration register with our humanizer-grep gate |
| `hyperframes-media` | TTS, Whisper transcribe, background removal, captions | **Partial defer** — use for TTS infrastructure; pipe your narration through our humanizer-grep gate BEFORE calling their TTS |
| `hyperframes-registry` | Install blocks and components (`hyperframes add`) | Defer — catalog discovery |

### Production-shape skills (use these as templates for our work)

| Upstream skill | Best for | Our lens |
|---|---|---|
| `general-video` | Authoring a fresh HyperFrames composition from intent | **OVERRIDE** — apply our video-discipline stages 1-2 (FACTS + MANUSCRIPT) BEFORE invoking general-video; their workflow assumes manuscript already done |
| `faceless-explainer` | Talking-head-less educational content | Strong match for our trendy-shorts work (#634-#638); apply our discipline layer on top |
| `motion-graphics` | Animated infographics, kinetic typography | Match for the McKinsey 92/1 stat-short or AI Fluency 5-skills explainer |
| `product-launch-video` | Product/feature announcement videos | Lower match — different brand register than educational |
| `pr-to-video` | Press-release-to-video automation | Niche; useful if we ever automate news-cycle content |
| `website-to-video` | Capture website → produce video walkthrough | Niche; useful for case-study shorts featuring real products |
| `embedded-captions` | Burn-in captions on existing renders | Defer — caption infrastructure |
| `graphic-overlays` | Lower-thirds, callouts, watermarks | Defer — overlay component library |

### Migration skill

| Upstream skill | When to use | Our position |
|---|---|---|
| `remotion-to-hyperframes` | Explicitly porting an existing Remotion composition | **DO NOT INVOKE on ChapterReel.tsx without explicit author go.** This skill is non-destructive (reads source, emits new HTML, originals preserved) but the SSIM-validated translation requires careful evaluation. For new series, author natively rather than migrating. |

## Routing decisions for our typical work

| Our task | Upstream entry point | Our discipline layer adds |
|---|---|---|
| 60s case-study short (e.g. lifedash#638 Mac Minis lawyer) | `faceless-explainer` | FACTS doc, humanizer-grep, version output |
| Stat-short (e.g. lifedash#635 AI Fluency 5 skills) | `motion-graphics` | FACTS doc, humanizer-grep, version output |
| Horror-story short (e.g. lifedash#637 €0.01 banking attack) | `faceless-explainer` + custom blocks | FACTS doc, humanizer-grep, version output, primary-source citation discipline |
| Evergreen prompt-instruction video (e.g. lifedash#634 "I don't know") | `general-video` | FACTS doc, humanizer-grep, version output |
| Migrating ChapterReel to HyperFrames | `remotion-to-hyperframes` | **Halt — get explicit go from author first.** ChapterReel is the in-flight asset to protect. |

## What HyperFrames intentionally does not cover (and we own)

1. **The FACTS stage** — distilling primary-source facts into a teachable structure before manuscript work
2. **The humanizer-grep gate** — AI-slop scrub on narration before TTS
3. **Engine-selection criteria** — when to use HyperFrames vs. Remotion vs. neither
4. **Series-continuity rules** — how to keep a multi-chapter series visually + tonally consistent (we use `video-remotion` for series; HyperFrames is single-shot territory)
5. **Version-output discipline** (the vNN never-overwrite rule) — applies regardless of engine

These are documented in `video-discipline/SKILL.md` (engine-agnostic) and `video-hyperframes/SKILL.md` (HyperFrames-specific application).

## How to update this map

When HyperFrames ships a new skill (visible at `https://github.com/heygen-com/hyperframes/tree/<SHA>/skills/`), add a row above. When our work surfaces a new routing decision, add it to the "Routing decisions" table. When we hit a HyperFrames quirk that needs documenting, add to `known-issues.md` (created on first failure).

Quarterly review cadence: check the upstream skill list for additions/removals when bumping the pinned SHA.
