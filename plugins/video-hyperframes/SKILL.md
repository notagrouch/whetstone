---
name: video-hyperframes
description: Thin lens over HeyGen's HyperFrames (HTML + GSAP video engine) for short-form (<90s) video production. Adds the production-discipline + facts-to-manuscript + humanizer-grep layer that HyperFrames doesn't ship out of the box. Use ONLY for single-shot social/explainer content under 90s. For multi-chapter series with continuity, use video-remotion instead.
license: MIT
prerequisites: [video-discipline]
dependencies:
  external:
    - name: hyperframes
      source: https://github.com/heygen-com/hyperframes
      pinned_sha: 479184ecf0bc5d9c02e621ea6019fa7d2c417ab8
      install: npx skills add heygen-com/hyperframes
      required_for: rendering only - discipline layer applies without it
      review_cadence: quarterly
---

# video-hyperframes

Thin lens over [HeyGen's HyperFrames](https://github.com/heygen-com/hyperframes) for short-form (<90s) video production. HyperFrames is an Apache 2.0 HTML-native video engine that ships a comprehensive catalog of installable blocks, first-party agent skills, and a CLI-driven dev loop.

**This skill does NOT duplicate HyperFrames' documentation.** It adds the production layer that HyperFrames intentionally leaves to the operator: the facts-to-manuscript stage, the humanizer-grep gate, the version-control discipline, and the engine-selection criteria that tell you when HyperFrames is the right choice.

The engine-agnostic disciplines (pacing, voice lock, density floor, pace adjustment, etc.) live in the sibling **video-discipline** skill — required prerequisite.

## When to use

**Use video-hyperframes for:**
- Single-shot social content under 90s (Reels, Shorts, TikTok, IG)
- One-off explainers / case-study shorts / horror-story videos / promo clips
- Content where HyperFrames' catalog blocks (`instagram-follow`, `flash-through-white`, `data-chart`) save days of bespoke build time
- Work where the rendering engine is allowed to be a black box (HTML in, MP4 out)

**Do NOT use video-hyperframes for:**
- Multi-chapter series with continuity (use `video-remotion` — protects custom primitive library investment)
- Active series mid-flight (never auto-migrate; finish the series on its current engine)
- Content requiring custom React composition primitives (HTML+GSAP source is structurally weaker for complex composition; use Remotion)
- Long-form video >3 min (different pacing math; out of scope for both this skill and video-discipline)

## Dependency: HyperFrames upstream

HyperFrames is pinned at SHA `479184ecf0bc5d9c02e621ea6019fa7d2c417ab8` (captured 2026-06-16).

**Install path (NOT into `~/.claude/`):**

```bash
# Scratch eval / project init
mkdir -p /tmp/hyperframes-eval && cd /tmp/hyperframes-eval
npx hyperframes init my-short

# Skills install — pin to a specific HyperFrames SHA, never `latest`
cd my-short
npx skills add heygen-com/hyperframes@479184ecf0bc5d9c02e621ea6019fa7d2c417ab8
```

**Why pin a SHA, not `main`:** HeyGen is a commercial company shipping rapidly. `npx skills add heygen-com/hyperframes` (no SHA) fetches whatever is on main — which can change between sessions. Pinning gives you a stable baseline that you bump deliberately.

**Quarterly review cadence:** every ~90 days, check HyperFrames' releases for breaking changes since the pinned SHA. If clean, bump to the latest stable; if breaking, schedule a migration session before the bump.

See `references/upstream-skill-map.md` for which of HyperFrames' 16 skills to consult for which video shape.

## The value-add layer (what HyperFrames doesn't ship)

HyperFrames covers the rendering and authoring contract (compositions, animations, captions, TTS, audio). It does NOT cover:

### 1. The facts-to-manuscript stage

Before you author an HTML composition, you need a long-form manuscript distilled from primary-source facts. HyperFrames' `general-video` skill jumps straight to scene-breakdown; for educational content, that's premature.

**Pipeline (from video-discipline):**

```
FACTS → MANUSCRIPT → SCENE BREAKDOWN → STORYBOARD → BUILD
```

Stages 1-2 (FACTS, MANUSCRIPT) happen BEFORE you touch HyperFrames. Stage 3-5 (SCENE BREAKDOWN, STORYBOARD, BUILD) are where HyperFrames' workflow kicks in. Skipping the upstream stages is the most common failure mode in single-shot explainer production.

### 2. The humanizer-grep gate

HyperFrames' `hyperframes-creative` skill covers narration register and palette decisions. It does NOT enforce an AI-slop scrub of the narration before TTS.

**Run before any TTS call:**

```bash
grep -iE "delve|leverage|robust|vibrant|tapestry|comprehensive|seamless|in the realm of|landscape|when it comes to|it's important to note|i hope this helps|ultimately,|in conclusion|moreover,|furthermore,|additionally," narration.txt
```

Empty result passes. Any hit forces rewrite. See `video-discipline/references/humanizer-banned-tokens.md` for the full pattern + per-token rationale + the patterns the grep does NOT catch (em-dash overuse, rule-of-three padding, status-flattery).

### 3. Version control discipline

HyperFrames' default render output overwrites the previous render. For one-shot social content this is fine. For iteration-heavy work (when you're A/B-testing variants), apply the `vNN` discipline from video-discipline:

```bash
# After each render, rename to versioned output
mv out/composition-main.mp4 out/composition-v01-1080.mp4
```

Lighter weight than the Remotion render workflow, but the principle (never overwrite a successful render) still applies.

### 4. Catalog-block selection guidance

HyperFrames ships a Catalog (`npx hyperframes add <block>`). For our typical short-form work, the high-value blocks are:

| Block | Use case | Install |
|---|---|---|
| `instagram-follow` | Social CTA overlay on shorts | `npx hyperframes add instagram-follow` |
| `flash-through-white` | Scene transition (high-energy hooks) | `npx hyperframes add flash-through-white` |
| `data-chart` | Animated stat / chart for case-study shorts | `npx hyperframes add data-chart` |
| `embedded-captions` (skill, not block) | Auto-burned captions from TTS | See `hyperframes-media` skill |

Before building a primitive from scratch, search the Catalog first: `npx hyperframes search <topic>`.

## Workflow

### Step 1 — Apply video-discipline stages 1-2 (FACTS + MANUSCRIPT)

Write `facts/<short-name>-facts.md` with the concrete teaching devices. Write the long-form manuscript (`~1500-2000 words`). These are upstream of HyperFrames — pure markdown work.

### Step 2 — Init HyperFrames project

```bash
mkdir -p /tmp/<short-name> && cd /tmp/<short-name>
npx hyperframes init .
```

Read the generated `index.html` and `composition.html` to understand the schema before authoring.

### Step 3 — Scene breakdown + storyboard inline in HTML

Per video-discipline #5, break the manuscript into 5 beats (intro / anchor-1 / anchor-2 heaviest / anchor-3 / close). Author directly as HTML with `data-start` / `data-duration` / `data-track-index` attributes. No separate markdown storyboard needed for single-shot work.

Reference upstream `hyperframes-core/references/data-attributes.md` for the schema.

### Step 4 — Add catalog blocks

`npx hyperframes search <topic>` for blocks that fit the storyboard. Install via `npx hyperframes add`. Compose blocks into the 5-beat structure.

### Step 5 — TTS narration (engine-agnostic discipline)

Run humanizer-grep gate FIRST. Then use HyperFrames' `hyperframes-media` skill for TTS or pipe your own pre-generated narration audio.

### Step 6 — Preview + render

```bash
npx hyperframes preview          # local preview with live reload
npx hyperframes render           # produce MP4
```

Verify the output via `ffprobe -v error -show_entries format=duration out/<file>.mp4`.

### Step 7 — Version the output

```bash
mv out/composition.mp4 out/<short-name>-v01-1080.mp4
```

Never overwrite. Per video-discipline #6.

## When to escalate

If a HyperFrames render fails repeatedly, the lint refuses, or a catalog block doesn't behave as documented:

1. Check `references/known-issues.md` (this skill's local catalog)
2. Read upstream `hyperframes-cli/references/troubleshooting.md`
3. Check HyperFrames' Discord (linked in their README)
4. File a follow-up note in `references/known-issues.md` with the workaround

Do NOT modify HyperFrames source code — the pinned SHA is the contract.

## Sibling skills

- **video-discipline** (REQUIRED prerequisite) — engine-agnostic 12 disciplines + 5-stage pipeline + worked examples
- **video-remotion** — Remotion-specific skill for multi-chapter series work; do NOT use for HyperFrames work

## References

- `references/upstream-skill-map.md` — which of HyperFrames' 16 skills covers what; routing guide
- `references/known-issues.md` (created on first failure) — local catalog of HyperFrames quirks we've hit

## Compatibility

- Claude Code (Anthropic Agent Skills spec)
- GitHub Copilot CLI
- Cursor
- Gemini CLI
- Any MCP-aware agent client that supports `npx skills add`

## License

MIT. Depends on HyperFrames (Apache 2.0). Compatible licensing.
