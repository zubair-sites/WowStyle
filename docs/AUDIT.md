# Audit

Status: first pass done 2026-10-30 from public access only (no login yet).

## Checklist

### Technical
- [ ] HTTPS everywhere, no mixed content; http and www redirect to one version
- [ ] WordPress, theme and plugin versions current (as far as visible)
- [ ] Page speed / Core Web Vitals, mobile and desktop
- [ ] Image sizes and formats (WebP/AVIF), lazy loading
- [ ] Caching and CDN
- [ ] Broken internal and external links, 404s
- [ ] robots.txt and XML sitemap
- [ ] Exposed user enumeration (`/wp-json/wp/v2/users`), xmlrpc, login hardening

### SEO
- [ ] Titles and meta descriptions: missing, duplicate, too long
- [ ] One H1 per page, sensible heading structure
- [ ] Canonicals, noindex on thin archive/tag pages
- [ ] Structured data (Article, Breadcrumb, Organization)
- [ ] Internal linking, orphan posts
- [ ] Image alt text
- [ ] Thin, outdated or duplicate content; posts to update, merge or remove

### Content and design
- [ ] Clear purpose on the homepage, navigation that matches the content
- [ ] Mobile layout and readability
- [ ] Categories and tags tidy (no near-duplicates, no empty ones)
- [ ] About, Contact, Privacy Policy, Cookie notice (UK GDPR / PECR)
- [ ] Affiliate / sponsored disclosures where needed (ASA / CAP code)

## Findings (2026-10-30, public access)

### What the site is right now
- WordPress 7.1.4 on Hostinger (LiteSpeed, PHP 8.3), theme **Kayleen** (Rivax),
  **Elementor** 4.3.5, Mailchimp for WP, Redux.
- **No published posts.** One category ("Uncategorized", empty), no tags.
- 4 pages: Home, Blog, About, Contact. Home and Blog show "Nothing found!".
  About is theme demo text ("Alice Qelvin", lorem ipsum).
- 120 media files, mostly from 2021–2022, none with alt text. The two logo PNGs
  are about 1.4–1.6 MB each.
- A theme demo import ran today (09:57) and Home/Blog were edited at 10:37,
  so the site appears to be mid-setup.

### Security (fix first)
1. **Public log file** at `/wp-content/uploads/2026/10/log_file_2026-10-30__09-57-26.txt`
   (demo-import log). It shows the server path and hosting account ID. Delete it from Media.
2. **Admin login name is public.** User 1's username/display name is an email address,
   visible at `/wp-json/wp/v2/users` and in the author URL `/author/kamilshykh7gmail-com/`.
   Set a public display name and block user enumeration.
3. `readme.html` is public and the WordPress version is shown in a generator tag (minor).
4. `wp-login.php` is open with no visible login protection. Check for 2FA / limit-login.

### SEO
- No meta description, no Open Graph tags, no H1 on the homepage, empty site tagline.
- `/sitemap.xml` redirects to `/wp-sitemap.xml`, which returns **404**. No sitemap at all.
- No SEO plugin detected (no Yoast/RankMath output).
- Nothing indexable to rank: zero posts.

### Content and compliance
- About page is placeholder text; Contact page form not tested.
- No Privacy Policy page, no cookie notice (needed under UK GDPR/PECR once analytics,
  Mailchimp signup or ads are active).
- No analytics detected.
