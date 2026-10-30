# Status

_Last updated: 2026-10-30_

## Summary
Brand, homepage, core pages and 6 starter posts are live (see CHANGELOG 2026-10-30
session 2). Waiting on the owner's review and the WP-admin steps below.

## Needs the owner (in WP admin)
These live in the theme options / Rivax header-footer templates, which the REST API
can't reach (installing a code-snippets plugin to do it was blocked by the session's
safety rules; the owner can allow it instead).
1. Theme options: logo → `the-wow-style-logo-dark.png` (light version for dark headers);
   accent colour `#ff2c54` → `#111111`.
2. Rivax "Default Footer" (1213): Category list (Health/Typography/Music/Travel are demo
   text), add Privacy Policy + Affiliate Disclosure links, social links, newsletter block
   (needs Mailchimp API key, or remove it).
3. Rank Math setup wizard (no meta descriptions/OG/sitemap output yet).
4. Settings → Reading: untick "Discourage search engines" once happy.
5. Send a test message through the Contact form.
6. Delete the WP Reset plugin; real author name/photo/bio (see open questions).

## Access
- WordPress REST API: **working as administrator** (checked 2026-10-30), but only
  after correcting the stored values in-session. Owner to fix the environment:
  - `WP_USER` must be the login email (`kamilshykh7@gmail.com`); the stored value is
    wrapped in `< >` and contains a space, so it's rejected.
  - `WP_APP_PASSWORD` is wrapped in `< >`; remove the brackets (keep the spaces).

- SSH (Hostinger, 156.67.72.11:65002): enabled by owner, but **not reachable from
  the cloud environment** — direct TCP times out and tunnelling through the egress
  proxy is not permitted. Don't rely on SSH; use the REST API (+ Elementor MCP endpoint)
  and give the owner click-by-click steps for anything else.

## Open questions for the owner
- Niche: fashion blog (confirmed). Audience still to confirm (assumed UK women, everyday style).
- Monetisation plan: ads, affiliate links, sponsored posts, products?
- Real author: name, photo and short bio of the person writing (not invented).
- Are there drafts or old posts we should keep?
- Did the owner run the demo import this morning, or someone else?

## Next step
Owner reviews the site and does the WP-admin steps above; then Rank Math meta per post,
content plan and steady publishing.
