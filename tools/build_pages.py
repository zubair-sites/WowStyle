#!/usr/bin/env python3
"""Build the Elementor layouts for Home, About and Contact in the minimal brand style.

Writes `_elementor_data` through the REST API. Each page is matched by slug and
created if missing. Run again after editing to redeploy.

Usage: python3 tools/build_pages.py [home|about|contact ...]
"""
import json
import os
import secrets
import sys

sys.path.insert(0, os.path.dirname(__file__))
import wp  # noqa: E402

INK, IVORY, STONE, TAUPE, GREY = "#111111", "#F7F4EF", "#E9E3DA", "#8C7A66", "#4A4A4A"
SERIF, SANS = "Bodoni Moda", "Jost"
SITE = "https://thewowstyle.co.uk"


def eid():
    return secrets.token_hex(4)[:7]


def px(top, right=None, bottom=None, left=None):
    right = top if right is None else right
    bottom = top if bottom is None else bottom
    left = right if left is None else left
    return {"unit": "px", "top": str(top), "right": str(right), "bottom": str(bottom), "left": str(left), "isLinked": False}


def size(n, unit="px"):
    return {"unit": unit, "size": n, "sizes": []}


def font(prefix, family, px_size, weight="400", mobile=None, spacing=None, transform=None, line=None):
    s = {
        f"{prefix}_typography": "custom",
        f"{prefix}_font_family": family,
        f"{prefix}_font_size": size(px_size),
        f"{prefix}_font_weight": weight,
    }
    if mobile:
        s[f"{prefix}_font_size_mobile"] = size(mobile)
    if spacing is not None:
        s[f"{prefix}_letter_spacing"] = size(spacing)
    if transform:
        s[f"{prefix}_text_transform"] = transform
    if line:
        s[f"{prefix}_line_height"] = size(line, "em")
    return s


def widget(kind, settings):
    return {"id": eid(), "elType": "widget", "widgetType": kind, "settings": settings, "elements": []}


def column(elements, width=100, **settings):
    return {"id": eid(), "elType": "column", "settings": dict({"_column_size": width, "_inline_size": width, "align": "center"}, **settings), "elements": elements}


def section(columns, bg=None, pad=(90, 20), width=1140, **settings):
    s = {"content_width": size(width), "padding": px(pad[0], pad[1]), "padding_mobile": px(int(pad[0] * 0.6), 20)}
    if bg:
        s.update(background_background="classic", background_color=bg)
    s.update(settings)
    return {"id": eid(), "elType": "section", "settings": s, "elements": columns}


def kicker(text, align="center"):
    return widget("heading", dict(
        {"title": text, "header_size": "p", "align": align, "title_color": TAUPE, "_margin": px(0, 0, 14, 0)},
        **font("typography", SANS, 13, "500", spacing=4, transform="uppercase")))


def heading(text, tag="h2", px_size=40, align="center", mobile=None, color=INK):
    return widget("heading", dict(
        {"title": text, "header_size": tag, "align": align, "title_color": color},
        **font("typography", SERIF, px_size, "500", mobile=mobile or int(px_size * 0.72), line=1.15)))


def text(html, align="center", color=GREY, px_size=18, width=None):
    s = dict({"editor": html, "align": align, "text_color": color}, **font("typography", SANS, px_size, "400", line=1.7))
    if width:
        # Narrow the line length with side padding (as a % of the column) so it stays centred.
        side = str(max(0, round((1140 - width) / 2 / 1140 * 100)))
        s.update(_padding={"unit": "%", "top": "0", "right": side, "bottom": "0", "left": side, "isLinked": False},
                 _padding_tablet=px(0, 40), _padding_mobile=px(0))
    return widget("text-editor", s)


def button(label, url, filled=True, align="center"):
    s = {
        "text": label, "link": {"url": url, "is_external": "", "nofollow": ""}, "align": align,
        "button_text_color": IVORY if filled else INK,
        "background_color": INK if filled else "#FFFFFF00",
        "hover_color": INK if filled else IVORY,
        "button_background_hover_color": IVORY if filled else INK,
        "border_border": "solid", "border_width": px(1), "border_color": INK,
        "border_radius": px(0), "text_padding": px(16, 34), "align_mobile": "center",
    }
    s.update(font("typography", SANS, 13, "500", spacing=2.5, transform="uppercase"))
    return widget("button", s)


def spacer(h):
    return widget("spacer", {"space": size(h)})


def post_grid(count=6, columns="3", category_ids=None, paginate=False):
    """Theme post grid restyled to the minimal palette (no borders, ink text)."""
    s = {
        "posts_per_page": count, "columns": columns, "columns_tablet": "2", "columns_mobile": "1",
        "row_gap": size(50), "column_gap": size(30),
        "thumbnail_size": "rivax-medium", "title_tag": "h3",
        "terms_taxonomy": "category", "terms_position": "outside",
        "show_excerpt": "yes", "excerpt_length": 110,
        "read_more_text": "Read more", "pagination_type": "none",
        "image_overlay_color_color": "#02010100", "image_border_radius": px(0), "image_link": "yes",
        "title_color": INK, "title_hover_style": "none",
        "title_margin": px(8, 0, 10, 0),
        "term_color": TAUPE, "term_background_color": "#FFFFFF00",
        "excerpt_color": GREY,
        "meta_color": "#8A8A8A",
    }
    s.update(font("title_typography", SERIF, 24, "500", mobile=21, line=1.3))
    s.update(font("term_typography", SANS, 12, "500", spacing=2.5, transform="uppercase"))
    s.update(font("excerpt_typography", SANS, 16, "400", line=1.6))
    if paginate:
        s.update(pagination_type="numbers", pagination_color=INK, pagination_color_hover=IVORY,
                 pagination_link_bg_color_hover=INK, pagination_link_bg_color_active=INK,
                 pagination_color_active=IVORY, pagination_margin_top=size(60))
    if category_ids:
        s.update(posts_include_by=["taxonomy"], posts_include_taxonomy_ids=[str(c) for c in category_ids])
    return widget("rivax-post-modern", s)


def category_tile(name, blurb, slug):
    return column([
        widget("heading", dict({"title": name, "header_size": "h3", "align": "left", "title_color": INK,
                                "link": {"url": f"{SITE}/category/{slug}/"}}, **font("typography", SERIF, 24, "500"))),
        text(f"<p>{blurb}</p>", align="left", px_size=15),
        widget("heading", dict({"title": "Explore →", "header_size": "p", "align": "left", "title_color": INK,
                                "link": {"url": f"{SITE}/category/{slug}/"}},
                               **font("typography", SANS, 12, "500", spacing=2.5, transform="uppercase"))),
    ], 25, padding=px(30, 26), border_border="solid", border_width=px(1), border_color="#D9D1C6",
        margin=px(0, 8), background_background="classic", background_color="#FFFFFF")


def home():
    return [
        section([column([
            kicker("Fashion · Style · Wardrobe"),
            heading("Style that works for real life.", "h1", 58, mobile=38),
            spacer(6),
            text("<p>Outfit ideas, wardrobe edits and honest guides to dressing well, without buying more than you need.</p>", width=620),
            spacer(14),
            section_buttons(),
        ])], bg=IVORY, pad=(120, 20)),
        section([column([
            kicker("Latest stories"),
            heading("Fresh on the journal", "h2", 40),
            spacer(30),
            post_grid(6),
            spacer(20),
            button("View all stories", f"{SITE}/blog/", filled=False),
        ])], pad=(90, 20)),
        section([column([kicker("Find your way around"), heading("Browse by topic", "h2", 40)])], bg=STONE, pad=(80, 20)),
        section([
            category_tile("Outfit Ideas", "Real-life outfit formulas for work, weekends and in between.", "outfit-ideas"),
            category_tile("Wardrobe Essentials", "The pieces worth owning, and how to make them last.", "wardrobe-essentials"),
            category_tile("Accessories", "Bags, shoes, sunglasses and jewellery, chosen well.", "accessories"),
            category_tile("Style Guides", "Fit, proportion and colour, explained simply.", "style-guides"),
        ], bg=STONE, pad=(0, 20)),
        section([column([spacer(60)])], bg=STONE, pad=(0, 0)),
        section([column([
            kicker("Start here"),
            heading("The Capsule Wardrobe Checklist", "h2", 40),
            spacer(4),
            text("<p>Thirty pieces that work together, season after season. See what you already own, what's missing and what you can let go.</p>", width=640),
            spacer(14),
            button("Read the checklist", f"{SITE}/capsule-wardrobe-checklist/"),
        ])], pad=(100, 20)),
        section([column([
            widget("image", {"image": {"id": 3632, "url": f"{SITE}/wp-content/uploads/2026/10/the-wow-style-logo-stacked.png"},
                             "image_size": "full", "width": size(240), "align": "center",
                             "_margin": px(0, 0, 10, 0)}),
            text("<p>The Wow Style is a UK fashion journal about getting dressed with confidence: simple ideas, honest advice and pieces worth keeping.</p>", width=600, px_size=17),
            spacer(6),
            button("About us", f"{SITE}/about/", filled=False),
        ])], bg=IVORY, pad=(90, 20)),
    ]


def section_buttons():
    """Two hero buttons side by side (inner section)."""
    return {"id": eid(), "elType": "section", "isInner": True,
            "settings": {"content_width": size(520), "gap": "narrow", "structure": "20"},
            "elements": [
                column([button("Read the latest", f"{SITE}/blog/", align="right")], 50, align_mobile="center"),
                column([button("Capsule checklist", f"{SITE}/capsule-wardrobe-checklist/", filled=False, align="left")], 50),
            ]}


def about():
    return [
        section([column([
            kicker("About"),
            heading("Getting dressed should feel good.", "h1", 52, mobile=36),
            spacer(6),
            text("<p>The Wow Style is a UK fashion and style journal for people who want to look put together without chasing every trend.</p>", width=680, px_size=19),
        ])], bg=IVORY, pad=(110, 20)),
        section([
            column([widget("image", {"image": {"id": 81, "url": f"{SITE}/wp-content/uploads/2021/11/jeferson-gomes-CO5DDUO8BWY-unsplash.jpg"},
                             "image_size": "large", "align": "center", "width": size(100, "%")})], 45),
            column([
                heading("What we write about", "h2", 34, align="left"),
                text("<p>We publish outfit ideas, wardrobe guides and practical advice on choosing clothes and accessories that suit you and last. Everything is written for real life: British weather, busy mornings and budgets of every size.</p>"
                     "<p>We believe in buying less and wearing more. A small wardrobe of pieces you love, that all work together, will always beat a full one with nothing to wear.</p>", align="left"),
                spacer(10),
                heading("How we work", "h2", 34, align="left"),
                text("<p>Our guides are independent. Brands can't pay to change what we say. Some articles may include affiliate links, which means we may earn a small commission if you buy through them, at no extra cost to you. We'll always say when a link is affiliate or a post is sponsored. Read our <a href=\"/affiliate-disclosure/\">affiliate disclosure</a> for details.</p>", align="left"),
            ], 55, padding=px(10, 10, 10, 50), padding_mobile=px(30, 0, 0, 0)),
        ], pad=(90, 20)),
        section([column([
            heading("Say hello", "h2", 34),
            text("<p>Questions, ideas or collaboration requests? We'd love to hear from you.</p>"),
            spacer(10),
            button("Contact us", f"{SITE}/contact/"),
        ])], bg=STONE, pad=(80, 20)),
    ]


CONTACT_FORM_CSS = f"""<style>
.rivax-contact-form input, .rivax-contact-form textarea {{
  background: #fff; border: 1px solid #D9D1C6; border-radius: 0; font-family: {SANS}, sans-serif; }}
.rivax-contact-form input:focus, .rivax-contact-form textarea:focus {{ border-color: {INK}; outline: none; }}
.rivax-contact-form label {{ font-family: {SANS}, sans-serif; letter-spacing: .08em; text-transform: uppercase; font-size: 12px; }}
.rivax-contact-form button, .rivax-contact-form [type=submit] {{
  background: {INK}; color: {IVORY}; border: 1px solid {INK}; border-radius: 0; padding: 16px 34px;
  font-family: {SANS}, sans-serif; font-size: 13px; letter-spacing: .2em; text-transform: uppercase; }}
.rivax-contact-form button:hover, .rivax-contact-form [type=submit]:hover {{ background: {IVORY}; color: {INK}; }}
</style>"""


def contact(old):
    def find(els):
        for e in els:
            if e.get("widgetType") == "rivax-contact-form":
                return e
            hit = find(e.get("elements", []))
            if hit:
                return hit

    form = find(old)
    form = dict(form, id=eid(), settings=dict(form["settings"], button_label="Send message",
                                              success_msg="Thank you. We'll get back to you soon."))
    return [
        section([column([
            kicker("Contact"),
            heading("Get in touch", "h1", 52, mobile=36),
            spacer(6),
            text("<p>For questions, feedback or collaborations, send us a message below. We reply within a few working days.</p>", width=620),
        ])], bg=IVORY, pad=(110, 20)),
        section([column([form, widget("html", {"html": CONTACT_FORM_CSS})])], pad=(70, 20), width=760),
    ]


def journal():
    return [
        section([column([
            kicker("The Journal"),
            heading("All stories", "h1", 52, mobile=36),
            spacer(6),
            text("<p>Outfit ideas, wardrobe essentials and simple style guides. New stories every week.</p>", width=620),
        ])], bg=IVORY, pad=(110, 20)),
        section([column([post_grid(9, paginate=True)])], pad=(80, 20)),
    ]


PAGES = {
    "journal": ("Journal", "blog", journal),
    "home": ("Home", "home", home),
    "about": ("About", "about", about),
    "contact": ("Contact", "contact", contact),
}


def deploy(key):
    title, slug, build = PAGES[key]
    found, _ = wp.request("GET", "/wp/v2/pages", {"slug": slug, "status": "publish,draft", "context": "edit"})
    old = json.loads(found[0]["meta"]["_elementor_data"] or "[]") if found else []
    data = build(old) if key == "contact" else build()
    body = {
        "title": title, "slug": slug, "status": "publish", "template": "elementor_header_footer",
        "meta": {"_elementor_edit_mode": "builder", "_elementor_template_type": "wp-page",
                 "_elementor_data": json.dumps(data)},
    }
    path = f"/wp/v2/pages/{found[0]['id']}" if found else "/wp/v2/pages"
    page, _ = wp.request("POST", path, body=body)
    wp.request("DELETE", "/elementor/v1/cache")
    print(f"{key}: {page['id']} {page['link']}")
    return page


if __name__ == "__main__":
    for k in sys.argv[1:] or list(PAGES):
        deploy(k)
