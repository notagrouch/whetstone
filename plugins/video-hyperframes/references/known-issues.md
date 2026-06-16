# HyperFrames known issues

Local catalog of friction we've hit running HyperFrames. Update as new issues surface.

## Active issues

### ~~1. Node engine mismatch (HyperFrames requires Node >=22; macOS often runs older)~~ — RESOLVED 2026-06-16 (see Resolved issues)

**Symptom on Node v20.19.0:**

```
npm warn EBADENGINE Unsupported engine {
  package: 'hyperframes@0.6.104',
  required: { node: '>=22' },
  current: { node: 'v20.19.0' }
}
```

`lint` still passes (it's pure markdown/HTML parsing). `validate` and `render` may fail downstream when the headless Chrome integration depends on Node 22 APIs.

**Workaround:**

```bash
# If you have nvm or n installed:
n 22                            # installs + switches to Node 22
# OR
nvm install 22 && nvm use 22

# Verify
node --version
```

After Node 22 is active, re-run from a fresh shell. The npm warning disappears and validate/render should complete.

**Captured:** 2026-06-16 during plugins/video-hyperframes smoke test (whetstone repo). Lint passed; validate failed downstream with the headless Chrome WebSocket symptom below.

### 2. `validate` / `inspect` timeout: "Timed out after 30000 ms while waiting for the WS endpoint URL to appear in stdout"

**Symptom:**

```
◆  Validating test-short in headless Chrome
✗ Timed out after 30000 ms while waiting for the WS endpoint URL to appear in stdout!
```

This is the puppeteer/playwright launch timeout. The headless Chrome subprocess started but never printed its WebSocket debug URL within 30s.

**Possible causes (in rough order of likelihood on macOS):**

1. **Node engine mismatch** (see issue 1 above) — Node 20 may not provide the runtime Chrome needs. Try Node 22 first.
2. **macOS security blocking puppeteer** — first launch sometimes requires accepting a Gatekeeper prompt. Run `npm run check` once interactively; subsequent runs are clean.
3. **No Chromium downloaded** — puppeteer fetches Chrome on first run; if the fetch silently failed, the spawn returns immediately. Check `~/.cache/puppeteer/` exists and has chrome bundles.
4. **Network blocking the Chrome download** — corporate proxy / Tailscale exit node. Try on a clean network.

**Workaround:** confirm Node 22 first (likely fixes both this AND issue 1). If still failing on Node 22, run `npx puppeteer browsers install chrome` to force the Chromium fetch.

**Captured:** 2026-06-16, whetstone smoke test, Node v20.19.0.

## Resolved issues

### 1. Node engine mismatch — RESOLVED 2026-06-16 (lifedash#654)

**Was:** HyperFrames requires Node >=22. Smoke test on workstation42 (Node v20.19.0) emitted `EBADENGINE` warning; lint passed but `validate` / `inspect` timed out at 30s on the headless Chrome WebSocket endpoint.

**Resolution:** Upgraded workstation42 to Node 22.22.3 via `sudo n 22`. Required two follow-ups:
1. `corepack enable` (lost during major-version bump)
2. `rm -rf ~/.npm/_npx` to force native-binding packages (specifically `sharp`) to rebuild against Node 22 — first `npx hyperframes init` after the upgrade failed with a `sharp` loader error until the cache was cleared

**Verification (Node 22.22.3):**
- `npm run check` (lint + validate + inspect): all green, no timeout
- `npm run render`: 10s test mp4 produced cleanly in ~31s wall time
- `ffprobe` reads duration: 10.000000 seconds
- remotion-studio reinstalls cleanly on Node 22

**Workaround for older Node (if a fresh box needs to run HF):** see the pre-upgrade workaround at the bottom of this file — `n 22` or `nvm install 22 && nvm use 22`, then clear `~/.npm/_npx` before first `npx hyperframes` invocation.

### 2. validate / inspect 30s timeout — RESOLVED 2026-06-16 (was downstream of issue 1)

**Was:** `Timed out after 30000 ms while waiting for the WS endpoint URL to appear in stdout` on `npm run check`.

**Resolution:** Was a symptom of issue 1 (Node 20 didn't satisfy headless Chrome's runtime needs cleanly). On Node 22 the WebSocket endpoint comes up within ~2 seconds and inspect completes normally.

## How to file a new issue

For each new friction:

1. Reproduce twice to confirm it's not transient
2. Capture the exact error message
3. Document the workaround (or "no workaround yet — escalated to HyperFrames Discord")
4. Add a row above with symptom + cause hypothesis + workaround + capture date

If the issue affects multiple users (not just our setup), open an issue on HeyGen's repo: `https://github.com/heygen-com/hyperframes/issues/new`
