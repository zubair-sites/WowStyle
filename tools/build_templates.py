#!/usr/bin/env python3
"""Build the theme's Rivax templates (header, sticky header, mobile menu, footer,
archive, related posts) in the brand style.

Rivax templates don't expose their Elementor data through the core REST API, so this
writes `_elementor_data` through the setup endpoint (`/wowstyle/v1/meta`), which must
be active while it runs.

Usage: python3 tools/build_templates.py [header|sticky|offcanvas|footer|archive|related ...]
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import wp  # noqa: E402
from build_pages import (  # noqa: E402
    GREY, INK, IVORY, SANS, SERIF, SITE, STONE, TAUPE,
    button, column, font, heading, kicker, post_grid, px, section, size, text, widget,
)

UPLOADS = f"{SITE}/wp-content/uploads/2026/10"
LOGO_DARK = {"id": 3630, "url": f"{UPLOADS}/the-wow-style-logo-dark.png", "alt": "The Wow Style", "source": "library"}
LOGO_LIGHT = {"id": 3631, "url": f"{UPLOADS}/the-wow-style-logo-light.png", "alt": "The Wow Style", "source": "library"}
MENU_ID = "57"
HAIRLINE = "#DDD5CA"

EXPLORE = [
    ("Outfit Ideas", "/category/outfit-ideas/"),
    ("Wardrobe Essentials", "/category/wardrobe-essentials/"),
    ("Accessories", "/category/accessories/"),
    ("Style Guides", "/category/style-guides/"),
    ("The Journal", "/blog/"),
]
ABOUT = [
    ("About us", "/about/"),
    ("Contact", "/contact/"),
    ("Write for us", "/write-for-us/"),
    ("Editorial policy", "/editorial-policy/"),
]
LEGAL = [
    ("Privacy & cookies", "/privacy-policy/"),
    ("Affiliate disclosure", "/affiliate-disclosure/"),
    ("Terms of use", "/terms-of-use/"),
]


def logo(image, width, mobile=None, align="center"):
    s = {"image": image, "align": align, "width": size(width), "custom_title": "The Wow Style"}
    if mobile:
        s["width_mobile"] = size(mobile)
    return widget("rivax-site-logo", s)


def links(items, color=INK, hover=TAUPE, px_size=15, gap=10):
    s = {
        "view": "traditional",
        "icon_list": [{"_id": f"l{i}", "text": t, "selected_icon": {"value": "", "library": ""},
                       "link": {"url": SITE + u, "is_external": "", "nofollow": ""}} for i, (t, u) in enumerate(items)],
        "text_color": color, "text_color_hover": hover, "space_between": size(gap),
        "text_indent": size(0),
    }
    s.update(font("icon_typography", SANS, px_size, "400"))
    return widget("icon-list", s)


def label(title, color=TAUPE, align="left"):
    return widget("heading", dict(
        {"title": title, "header_size": "h4", "align": align, "title_color": color, "_margin": px(0, 0, 18, 0)},
        **font("typography", SANS, 12, "500", spacing=3, transform="uppercase")))


def search_button():
    return widget("rivax-search", {
        "text_align": "right", "button_bg": "#FFFFFF00", "button_color": INK,
        "button_padding": px(8), "button_font_size": size(20), "button_border_radius": px(0),
    })


def navigation(align="center"):
    return widget("rivax-navigation", {"menu": MENU_ID, "H_menu_align": align, "h_menu_hover_shape": "hover-style-1"})


def header():
    return [
        section([
            column([widget("rivax-offcanvas", {"icon_text_align": "left", "content_template": "1180"})],
                   20, _inline_size_mobile=20, _inline_size_tablet=20),
            column([logo(LOGO_DARK, 230, 160)], 60, _inline_size_mobile=60, _inline_size_tablet=60),
            column([search_button()], 20, _inline_size_mobile=20, _inline_size_tablet=20),
        ], pad=(22, 20), width=1240, structure="30", content_position="middle",
            padding_mobile=px(14, 12)),
        section([column([navigation()])], pad=(4, 20), width=1240,
                hide_tablet="hidden-tablet", hide_mobile="hidden-mobile",
                border_border="solid", border_width=px(1, 0, 1, 0), border_color=STONE),
    ]


def sticky():
    return [section([
        column([logo(LOGO_DARK, 150, align="left")], 20),
        column([navigation("right")], 80),
    ], pad=(10, 20), width=1240, bg="#FFFFFF", structure="21", content_position="middle",
        hide_tablet="hidden-tablet", hide_mobile="hidden-mobile",
        border_border="solid", border_width=px(0, 0, 1, 0), border_color=STONE)]


def offcanvas():
    menu = [("Home", "/")] + EXPLORE[:4] + [("The Journal", "/blog/"), ("About", "/about/"),
                                            ("Contact", "/contact/"), ("Write for us", "/write-for-us/")]
    return [section([column([
        logo(LOGO_DARK, 180, align="left"),
        text("<p>Everyday fashion, outfit ideas and wardrobe edits.</p>", align="left", px_size=15),
        widget("divider", {"color": STONE, "gap": size(18)}),
        links(menu, px_size=19, gap=14),
        widget("divider", {"color": STONE, "gap": size(18)}),
        label("Latest stories"),
        widget("rivax-post-elastic", {
            "columns": "1", "columns_tablet": "1", "posts_per_page": 3, "thumbnail_size": "thumbnail",
            "show_author": "", "item_image_width": size(70), "item_image_height": size(70),
            "content_padding": px(0, 0, 0, 14), "row_gap": size(16), "title_tag": "h5",
            "title_hover_style": "none", "title_color": INK,
            **font("title_typography", SERIF, 15, "500", line=1.35),
        }),
    ], align="flex-start")], pad=(10, 0), width=400)]


def footer():
    cta = section([
        column([
            kicker("Contribute", align="left"),
            heading("Have a style story to share?", "h2", 34, align="left", color=IVORY),
        ], 66, align="flex-start"),
        column([button_light("Write for us", f"{SITE}/write-for-us/")], 34),
    ], bg=INK, pad=(70, 20), width=1200, structure="21", content_position="middle",
        border_border="solid", border_width=px(0, 0, 1, 0), border_color="#2A2A2A")

    cols = section([
        column([
            logo(LOGO_LIGHT, 200, align="left"),
            text("<p>A UK fashion journal about getting dressed with confidence: outfit ideas, wardrobe "
                 "essentials and simple style guides for real life.</p>", align="left", color="#BDB6AC", px_size=15),
        ], 37, align="flex-start", padding=px(0, 40, 0, 0), padding_mobile=px(0, 0, 30, 0)),
        column([label("Explore"), links(EXPLORE, color=IVORY, hover=TAUPE)], 21, align="flex-start",
               padding_mobile=px(0, 0, 26, 0)),
        column([label("The Wow Style"), links(ABOUT, color=IVORY, hover=TAUPE)], 21, align="flex-start",
               padding_mobile=px(0, 0, 26, 0)),
        column([label("Legal"), links(LEGAL, color=IVORY, hover=TAUPE)], 21, align="flex-start"),
    ], bg=INK, pad=(70, 20), width=1200, structure="40")

    bottom = section([
        column([widget("heading", dict({"title": "© 2026 The Wow Style. All rights reserved.", "header_size": "p",
                                        "align": "left", "align_mobile": "center", "title_color": "#8F887F"},
                                       **font("typography", SANS, 13, "400")))], 50),
        column([widget("heading", dict({"title": "Buy less. Wear more.", "header_size": "p", "align": "right",
                                        "align_mobile": "center", "title_color": "#8F887F"},
                                       **font("typography", SERIF, 15, "400")))], 50),
    ], bg=INK, pad=(26, 20), width=1200, structure="20",
        border_border="solid", border_width=px(1, 0, 0, 0), border_color="#2A2A2A")
    return [cta, cols, bottom]


def button_light(label_text, url):
    b = button(label_text, url, filled=False, align="right")
    b["settings"].update(button_text_color=IVORY, border_color=IVORY, hover_color=INK,
                         button_background_hover_color=IVORY, align_mobile="left")
    return b


def archive(old):
    grid = post_grid(12, paginate=True)
    grid["settings"]["posts_source"] = "current_query"  # show the category/search/author being viewed
    return [section([column([grid])], pad=(40, 20), width=1200)]


def related(old):
    grid = post_grid(3)
    grid["settings"].update(show_excerpt="", posts_per_page=3, posts_source="related")
    return [section([column([
        widget("divider", {"color": STONE, "gap": size(30)}),
        kicker("Keep reading"),
        heading("You might also like", "h2", 32),
        widget("spacer", {"space": size(24)}),
        grid,
    ])], pad=(30, 0), width=1200)]


TEMPLATES = {
    "header": (1176, header),
    "sticky": (1203, sticky),
    "offcanvas": (1180, offcanvas),
    "footer": (1213, footer),
    "archive": (1053, archive),
    "related": (1039, related),
}


def deploy(key):
    tid, build = TEMPLATES[key]
    old = wp.request("GET", "/wowstyle/v1/meta", {"post": tid, "key": "_elementor_data"})[0]["value"]
    old = json.loads(old) if old else []
    data = build(old) if key in ("archive", "related") else build()
    wp.request("POST", "/wowstyle/v1/meta", body={"post": tid, "key": "_elementor_data", "value": json.dumps(data)})
    print(f"{key}: template {tid} updated")


if __name__ == "__main__":
    for k in sys.argv[1:] or list(TEMPLATES):
        deploy(k)
