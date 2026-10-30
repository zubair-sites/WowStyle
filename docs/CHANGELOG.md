# Changelog

Changes made to the live site, newest first. Include date, what changed,
where (URL / post ID), and how to undo it.

## 2026-10-30 (session 3): full build-out, demo removal, SEO/AEO/GEO
Owner approved installing Code Snippets temporarily; it was used only for an admin-only
setup endpoint (`tools/snippets/setup-endpoints.php`) and has been deleted again.
Backups of everything replaced are in `backups/`.
- **Theme options** (`rivax_kayleen_options`, backup in `backups/`): logo 3630, accent `#111111`,
  second colour `#8C7A66`, link/heading ink, Bodoni Moda headings + Jost body, monochrome
  category badges, share buttons (FB, X, Pinterest, email, WhatsApp, link), no view counts,
  emojis off, smooth scroll off. Elementor kit 8 colours/fonts/buttons set to the same palette.
- **Templates rebuilt** (`tools/build_templates.py`, originals in `backups/templates/`):
  header 1176, sticky 1203, mobile menu 1180 (now has full navigation), footer 1213 (ink,
  Write-for-us CTA, Explore / The Wow Style / Legal links), archive 1053 (current query, no
  demo sidebar), related posts 1039.
- **Mobile:** removed the theme's floating round menu button (menu no longer assigned to
  the "Mobile menu" location); the header icon opens the menu.
- **Must-use plugin** `wp-content/mu-plugins/wowstyle-site.php` (source `tools/mu-plugin/`):
  brand CSS, H1 on standard pages (theme had it commented out), author avatar fallback,
  XML-RPC off, `?author=` enumeration blocked, public users endpoint hidden, generator removed.
  [Undo: delete the file]
- **Removed:** `readme.html`, `wp-config-sample.php`; 119 demo media files (local backup only,
  not in repo); 30 unused demo templates and the old demo home (Trash); WP Reset and One Click
  Demo Import plugins; default widgets moved to Inactive. Demo kit 3371 left (Elementor
  blocks deleting kits; it's inactive).
- **Images:** 8 branded cover images (`brand/covers.html`, media 3654–3661) as featured images.
- **Content:** all 6 posts now have a Quick answer box, internal links and an FAQ block
  (FAQPage schema). New pages: Write for Us 3710, Editorial Policy 3707, Terms of Use 3709.
  About links to editorial policy and Write for us. Elementor pages now have clean
  `post_content` (old demo HTML removed).
- **Rank Math** (backup in `backups/`): modules trimmed (+404 monitor, redirections, image SEO,
  llms.txt), Organization schema with logo, title separator, homepage/page/post/category SEO
  titles, descriptions and focus keywords, default OG image, breadcrumbs (schema), templates
  and Elementor floating buttons noindexed and out of the sitemap, author archive noindex,
  llms.txt with site summary, wizard marked complete.
- **WordPress:** language en_GB, privacy page set, comment moderation on, pingbacks off,
  **search engines allowed** (was "discourage").

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
