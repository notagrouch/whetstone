# whetstone

Cross-platform agent skills, MCP servers, and tooling. General-purpose, standards-based — designed to work with Claude Code, GitHub Copilot CLI, Gemini CLI, and any MCP-aware agent client.

## What's here

- `plugins/` — Agent skills bundled as plugins (SKILL.md format, Anthropic Agent Skills spec)
- `mcp-servers/` — Model Context Protocol servers (cross-vendor tool integration)
- `scripts/` — Standalone CLI utilities usable from any agent or shell
- `configs/` — Shareable configuration templates
- `design/` — Design tokens, templates, theme presets
- `docs/` — Cross-cutting documentation

## Status

Early stage. First plugin set landed: the **video skills stack** (three skills for short-form educational video production).

## Video skills — three-skill stack

The headline package is a three-skill video-production stack covering the same craft from three angles. Use them together: the engine-agnostic discipline skill is the prerequisite; one of the two engine-specific siblings handles render-stage details.

| Skill | Use for | Engine |
|---|---|---|
| [`plugins/video-discipline/`](plugins/video-discipline/) | The 12 disciplines, 5-stage pipeline (FACTS→MANUSCRIPT→SCENE→STORYBOARD→BUILD), failure-mode catalog, humanizer-grep gate. Engine-agnostic. | None — applies to any |
| [`plugins/video-remotion/`](plugins/video-remotion/) | Remotion-specific receipts (concurrency=2, text safe-area at 1080×1920, atempo lock, ChapterReel-style monolith conventions). | [Remotion](https://www.remotion.dev/) |
| [`plugins/video-hyperframes/`](plugins/video-hyperframes/) | Thin lens over HeyGen's HyperFrames (HTML+GSAP video engine). Adds the FACTS→MANUSCRIPT stage + humanizer-grep + version-control discipline that HyperFrames doesn't ship. | [HyperFrames](https://github.com/heygen-com/hyperframes) (pinned dependency) |

**Engine-selection rule (hard, not a suggestion):**
- Multi-chapter series with continuity, custom primitive library → **Remotion** (`video-remotion`)
- Single-shot short-form content under 90s, want HyperFrames' catalog blocks → **HyperFrames** (`video-hyperframes`)
- Active series mid-flight → finish on whatever engine you started on; never auto-migrate

See each skill's `SKILL.md` for the full instructions and `references/` for routing guides and failure-mode catalogs.

## Contributing

After cloning, enable the local pre-commit hook:

```bash
git config core.hooksPath .githooks
```

The hook runs `gitleaks` for secret scanning. Install via `brew install gitleaks` (macOS) or see [github.com/gitleaks/gitleaks](https://github.com/gitleaks/gitleaks).

## License

MIT.
