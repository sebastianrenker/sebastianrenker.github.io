# sebastianrenker.github.io

![License](https://img.shields.io/badge/license-private%20%2F%20non--commercial-lightgrey)
![Stack](https://img.shields.io/badge/stack-static%20HTML%2FCSS-orange)
![Hosting](https://img.shields.io/badge/hosting-GitHub%20Pages-brightgreen)

> Static landing page for the RENKER platform — privacy-first, no build step, no trackers.

## Overview

The public landing page for the RENKER platform, live at
<https://sebastianrenker.github.io/>. It introduces the platform and links to the
individual project repositories, each under its own license.

## Features

- **No build step** — plain HTML/CSS, served as-is.
- **No cookies, no analytics, no third-party requests** at runtime.
- **Self-hosted fonts** in `fonts/` (Archivo + IBM Plex Mono, SIL OFL 1.1) — no
  Google Fonts CDN, so no visitor IP leaks to a font provider.
- **Reality-checked content** — claims are verified against `reality-check.md`.

## Architecture

Two static pages, no framework, no server logic:

| Path | Purpose |
|---|---|
| `index.html` | Landing page |
| `privacy.html` | Privacy notice |
| `fonts/` | Self-hosted webfonts (SIL OFL 1.1) |
| `reality-check.md` | Fact-check reference for the page content |

## Quickstart

Open `index.html` directly in a browser, or serve the folder statically:

```bash
python -m http.server 8000   # -> http://127.0.0.1:8000
```

GitHub Pages serves the repository root automatically at the URL above.

## Tests

No build and no automated tests (static site). Content is manually verified
against `reality-check.md` before publishing.

## License

Private, non-commercial open-source project. © 2026 Sebastian Renker (RENKER).
Linked source repositories are under their own licenses.
