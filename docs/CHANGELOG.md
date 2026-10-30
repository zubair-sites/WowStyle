# Changelog

Changes made to the live site, newest first. Include date, what changed,
where (URL / post ID), and how to undo it.

## 2026-10-30 (session 2): brand, homepage, content
Undo notes in brackets.
- **Brand assets** uploaded to Media (source: `brand/assets.html`, PNGs in `brand/png/`):
  logo dark 3630, logo light 3631, stacked 3632, site icon 3633, OG image 3634, newsletter 3635.
- **Settings:** tagline "Everyday fashion, outfit ideas and wardrobe edits"; site icon 3633;
  site logo 3630; timezone Europe/London; date format `j F Y`. [Settings → General]
- **Security:** deleted public demo-import log (media 16); user 1 display name "The Wow Style",
  slug `the-wow-style` (was the email); deactivated WP Reset and One Click Demo Import.
  [Plugins → activate]
- **Categories:** renamed Uncategorized → Style Guides (id 1); added Outfit Ideas 59,
  Wardrobe Essentials 60, Accessories 61.
- **Posts published** (source `content/posts/`, script `tools/publish_posts.py`): 3637–3642.
- **Pages:** new Home 3643 set as front page; old demo home 3115 → draft `home-old-demo`
  [Settings → Reading → front page 3115, republish]. About 1067, Contact 1081 and Blog 966
  (now titled Journal) rebuilt with `tools/build_pages.py`. New Privacy & Cookie Policy 3649,
  Affiliate Disclosure 3648 (source `content/pages/`).
- **Menu 57** assigned to primary + mobile: Home (→3643), Outfit Ideas, Wardrobe Essentials,
  Accessories, Journal, About, Contact.
- **Not changed (needs WP admin):** header/footer logo, theme accent colour, footer links.
  Site still set to "Discourage search engines".

## 2026-10-30
- Set up this management repo. No changes made to the live site.
