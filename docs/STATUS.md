# Status

_Last updated: 2026-10-30_

## Summary
The site is a fresh install of the Kayleen theme (Elementor) with **no published
content**. It is effectively a build from scratch. See `AUDIT.md` for findings.

## Access
- Network access to thewowstyle.co.uk: working.
- WordPress Application Password: owner says it's added, but the variables were not
  present in the 2026-10-30 session. Environment changes apply to new sessions, so
  check `tools/wp.py check` at the start of the next session.

- SSH (Hostinger, 156.67.72.11:65002): enabled by owner, but **not reachable from
  the cloud environment** — direct TCP times out and tunnelling through the egress
  proxy is not permitted. Don't rely on SSH; use the REST API (+ Elementor MCP endpoint)
  and give the owner click-by-click steps for anything else.

## Open questions for the owner
- Niche and audience (fashion? lifestyle? home & interiors?).
- Monetisation plan: ads, affiliate links, sponsored posts, products?
- Who is the author/brand shown on the About page?
- Are there drafts or old posts we should keep?
- Did the owner run the demo import this morning, or someone else?

## Next step
Security quick fixes (owner, in WP admin), then build: structure, core pages, SEO
plugin, first batch of posts.
