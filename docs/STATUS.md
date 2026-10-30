# Status

_Last updated: 2026-10-30 (session 3)_

## Summary
The site is built and live: brand, theme, header/footer, 6 posts, all core and legal pages,
Write for Us (guest/sponsored posts), Rank Math SEO/AEO/GEO setup, indexing on. No demo
content remains. Next: the content plan (separate session).

## Needs the owner
1. **Real author.** Send the writer's name, photo and 2–3 line bio; we'll create their user,
   set it as author on posts (stronger E-E-A-T) and show them on About.
2. **Google Search Console:** verify the domain and submit `https://thewowstyle.co.uk/sitemap_index.xml`.
   Optionally connect Rank Math → Analytics.
3. **Contact form:** send one test message (goes to the WordPress admin email).
4. **Social profiles:** if/when they exist, send the URLs (footer, schema `sameAs`).
5. **Newsletter:** Mailchimp isn't connected. Add an API key (MC4WP) if you want sign-ups.
6. **Cloud environment variables:** remove the `< >` around `WP_USER`/`WP_APP_PASSWORD` and
   set `WP_USER` to the login email, so sessions don't need to correct them.
7. Review the legal pages (privacy, terms, affiliate, editorial) and the Write for Us rules.

## How changes are made
- REST API with the application password (`tools/wp.py`).
- Theme options, Rivax templates and Rank Math settings are **not** exposed by the REST API.
  Changing them again needs the setup endpoint: install Code Snippets, add
  `tools/snippets/setup-endpoints.php` as a snippet, do the work, then delete both.
- Permanent site code lives in the mu-plugin (`tools/mu-plugin/wowstyle-site.php`); redeploy
  it through the setup endpoint (`POST /wowstyle/v1/mu-plugin`) or by file manager.

## Access
- WordPress REST API: working as administrator.
- SSH (Hostinger): not reachable from the cloud environment.

## Open questions for the owner
- Audience: assumed UK, mainly women, everyday style, all budgets. Confirm or adjust.
- Monetisation: guest/sponsored posts planned; affiliate programmes? display ads?
