# The Wow Style — site management

Working repo for managing https://thewowstyle.co.uk (WordPress).
WordPress stays the live site; this repo holds the plan, the record of
changes, and any tooling or custom code, so each session can pick up where
the last one stopped.

| File | Purpose |
| --- | --- |
| `docs/STATUS.md` | Current state, blockers, what's next. Read this first. |
| `docs/TASKS.md` | Prioritised task list. |
| `docs/CHANGELOG.md` | Every change made to the live site, newest first. |
| `docs/AUDIT.md` | Audit checklist and findings. |
| `tools/wp.py` | WordPress REST API helper (stdlib only). |
| `tools/build_pages.py` | Elementor layouts for Home, Journal, About, Contact. |
| `tools/publish_posts.py` | Publish `content/posts` and `content/pages` Markdown. |
| `tools/render_brand.js` | Render `brand/assets.html` to `brand/png/`. |
| `brand/` | Logo, icon and graphic sources and PNGs. Palette: ink `#111111`, ivory `#F7F4EF`, stone `#E9E3DA`, taupe `#8C7A66`; fonts Bodoni Moda + Jost. |
| `content/` | Post and page copy, as published. |

## Access needed

Set as environment variables in the cloud environment (never commit them):

- `WP_URL` — `https://thewowstyle.co.uk`
- `WP_USER` — WordPress username
- `WP_APP_PASSWORD` — from Users → Profile → Application Passwords

The environment's network access must also allow `thewowstyle.co.uk`.

## Quick start

```bash
python3 tools/wp.py check
```

```bash
python3 tools/wp.py inventory > docs/inventory.json
```
