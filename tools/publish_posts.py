#!/usr/bin/env python3
"""Publish content/posts/*.md (and content/pages/*.md) to WordPress as block-editor content.

Each file has a small front matter block (title, slug, excerpt, and for posts
category and image). Files with `type: page` are published as pages.
Items are matched by slug: existing ones are updated, new ones created.

Usage: python3 tools/publish_posts.py [--status draft|publish] [file ...]
"""
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
import wp  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..", "content", "posts")


def parse(path):
    text = open(path, encoding="utf-8").read()
    _, front, body = text.split("---", 2)
    meta = dict(line.split(": ", 1) for line in front.strip().splitlines())
    return meta, body.strip()


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)


def to_blocks(md):
    out, items, ordered = [], [], False

    def flush():
        nonlocal items
        if items:
            tag = "ol" if ordered else "ul"
            attrs = ' {"ordered":true}' if ordered else ""
            lis = "".join(f"<!-- wp:list-item --><li>{i}</li><!-- /wp:list-item -->" for i in items)
            out.append(f'<!-- wp:list{attrs} --><{tag} class="wp-block-list">{lis}</{tag}><!-- /wp:list -->')
            items = []

    for line in md.splitlines():
        line = line.rstrip()
        m_ul = re.match(r"^- (\[ \] )?(.*)", line)
        m_ol = re.match(r"^\d+\. (.*)", line)
        if m_ul or m_ol:
            if items and ordered != bool(m_ol):
                flush()
            ordered = bool(m_ol)
            items.append(inline(m_ol.group(1) if m_ol else m_ul.group(2)))
            continue
        flush()
        if not line:
            continue
        h = re.match(r"^(#{2,4}) (.*)", line)
        if h:
            lvl = len(h.group(1))
            attrs = f' {{"level":{lvl}}}' if lvl != 2 else ""
            out.append(f'<!-- wp:heading{attrs} --><h{lvl} class="wp-block-heading">{inline(h.group(2))}</h{lvl}><!-- /wp:heading -->')
        else:
            out.append(f"<!-- wp:paragraph --><p>{inline(line)}</p><!-- /wp:paragraph -->")
    flush()
    return "\n\n".join(out)


def main(argv):
    status = "publish"
    if argv[:1] == ["--status"]:
        status, argv = argv[1], argv[2:]
    files = argv or sorted(os.path.join(ROOT, f) for f in os.listdir(ROOT) if f.endswith(".md"))
    cats = {c["slug"]: c["id"] for c in wp.get_all("/wp/v2/categories")}
    for path in files:
        meta, body = parse(path)
        kind = "pages" if meta.get("type") == "page" else "posts"
        data = {
            "title": meta["title"],
            "slug": meta["slug"],
            "status": status,
            "content": to_blocks(body),
            "excerpt": meta["excerpt"],
        }
        if kind == "posts":
            data.update(categories=[cats[meta["category"]]], featured_media=int(meta["image"]))
        found, _ = wp.request("GET", f"/wp/v2/{kind}", {"slug": meta["slug"], "status": "publish,draft,private"})
        path_ = f"/wp/v2/{kind}/{found[0]['id']}" if found else f"/wp/v2/{kind}"
        post, _ = wp.request("POST", path_, body=data)
        print(f"{'updated' if found else 'created'} {post['id']} {post['link']}")


if __name__ == "__main__":
    main(sys.argv[1:])
