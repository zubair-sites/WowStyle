# Status

_Last updated: 2026-10-30_

## Known so far
- Platform: WordPress.
- Business: not confirmed. A third-party listing for thewowstyle.com describes a
  lifestyle blog (home decor, interiors, travel, fashion, home improvement).
  Need to confirm whether the .co.uk site is the same.

## Blockers
1. `thewowstyle.co.uk` is not in the cloud environment's allowed network domains,
   so the site cannot be loaded or audited.
2. No WordPress Application Password set (`WP_URL`, `WP_USER`, `WP_APP_PASSWORD`).

## Open questions for the owner
- What is the business, and who is the audience?
- Main goal: traffic, sales/enquiries, redesign, or fixing problems?
- Plugins in use: WooCommerce? Elementor/Divi? Yoast/RankMath?
- Monetisation: ads, affiliate links, sponsored posts?

## Next step
Once access is in place: run `tools/wp.py check`, then the audit in `docs/AUDIT.md`.
