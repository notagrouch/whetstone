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

Early stage. Skeleton in place; first plugins under design.

## Contributing

After cloning, enable the local pre-commit hook:

```bash
git config core.hooksPath .githooks
```

The hook runs `gitleaks` for secret scanning. Install via `brew install gitleaks` (macOS) or see [github.com/gitleaks/gitleaks](https://github.com/gitleaks/gitleaks).

## License

MIT. Assisted with Claude.
