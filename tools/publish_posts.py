#!/usr/bin/env python3
"""Publish content/posts/*.md (and content/pages/*.md) to WordPress as block-editor content.

Each file has a small front matter block (title, slug, excerpt, and for posts
category and image). Files with `type: page` are published as pages.
Items are matched by slug: existing ones are updated, new ones created.

Optional front matter:
  quick        "Quick answer" summary shown first (answer-first, for AEO/GEO)
  seo_title    Rank Math SEO title
  description  Rank Math meta description
  keyword      Rank Math focus keyword(s), comma separated
A "## Frequently asked questions" section with "### Question" headings becomes a
Rank Math FAQ block, which outputs FAQPage schema.

SEO meta is written through the setup endpoint (/wowstyle/v1/meta) when it's active.

Usage: python3 tools/publish_posts.py [--status draft|publish] [file ...]
"""
import html
import json
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
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    s = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)


def block_json(data):
    """JSON for a block comment, escaped the way WordPress serialises it."""
    out = json.dumps(data, ensure_ascii=False)
    for ch, esc in (("--", "\\u002d\\u002d"), ("<", "\\u003c"), (">", "\\u003e"), ("&", "\\u0026")):
        out = out.replace(ch, esc)
    return out


def quick_answer(text):
    return ('<!-- wp:group {"className":"wow-quick-answer"} --><div class="wp-block-group wow-quick-answer">'
            f'<!-- wp:paragraph --><p><strong>Quick answer</strong> {inline(text)}</p><!-- /wp:paragraph -->'
            '</div><!-- /wp:group -->')


def faq_block(md):
    questions = []
    for chunk in re.split(r"^### ", md, flags=re.M)[1:]:
        q, _, a = chunk.partition("\n")
        answer = " ".join(inline(p.strip()) for p in a.strip().split("\n\n") if p.strip())
        questions.append({"id": f"faq-{len(questions) + 1}", "title": inline(q.strip()), "content": answer, "visible": True})
    items = "".join(f'<div id="{q["id"]}" class="rank-math-faq-item"><h3 class="rank-math-question">{q["title"]}</h3>'
                    f'<div class="rank-math-answer">{q["content"]}</div></div>' for q in questions)
    return (f'<!-- wp:heading --><h2 class="wp-block-heading">Frequently asked questions</h2><!-- /wp:heading -->\n\n'
            f'<!-- wp:rank-math/faq-block {block_json({"questions": questions})} -->'
            f'<div class="wp-block-rank-math-faq-block">{items}</div><!-- /wp:rank-math/faq-block -->')


def to_html(meta, body):
    main, _, faq = body.partition("## Frequently asked questions")
    parts = [quick_answer(meta["quick"])] if meta.get("quick") else []
    parts.append(to_blocks(main))
    if faq.strip():
        parts.append(faq_block(faq))
    return "\n\n".join(parts)


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
    seo_enabled = "/wowstyle/v1/meta" in wp.request("GET", "/")[0]["routes"]
    if not seo_enabled:
        print("note: setup endpoint not active, so Rank Math fields are skipped (set them in the editor)")
    for path in files:
        meta, body = parse(path)
        kind = "pages" if meta.get("type") == "page" else "posts"
        data = {
            "title": meta["title"],
            "slug": meta["slug"],
            "status": status,
            "content": to_html(meta, body),
            "excerpt": meta["excerpt"],
        }
        if kind == "posts":
            data.update(categories=[cats[meta["category"]]], featured_media=int(meta["image"]))
        found, _ = wp.request("GET", f"/wp/v2/{kind}", {"slug": meta["slug"], "status": "publish,draft,private"})
        path_ = f"/wp/v2/{kind}/{found[0]['id']}" if found else f"/wp/v2/{kind}"
        post, _ = wp.request("POST", path_, body=data)
        seo = {"rank_math_title": meta.get("seo_title"), "rank_math_description": meta.get("description"),
               "rank_math_focus_keyword": meta.get("keyword")}
        for key, value in seo.items():
            if value and seo_enabled:
                wp.request("POST", "/wowstyle/v1/meta", body={"post": post["id"], "key": key, "value": value})
        print(f"{'updated' if found else 'created'} {post['id']} {post['link']}")


if __name__ == "__main__":
    main(sys.argv[1:])
