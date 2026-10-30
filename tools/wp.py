#!/usr/bin/env python3
"""Small WordPress REST API helper for thewowstyle.co.uk (stdlib only).

Credentials come from the environment: WP_URL, WP_USER, WP_APP_PASSWORD.

Commands:
  check                     confirm the site and credentials work
  inventory                 dump posts, pages, categories, tags, media as JSON
  get <type> <id>           fetch one item (type: posts, pages, media, ...)
  update <type> <id> <json> update fields on one item, e.g. '{"title": "New"}'

Writes are explicit: only `update` changes anything on the live site.
"""
import base64
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


def env(name, required=True):
    value = os.environ.get(name, "").strip()
    if required and not value:
        sys.exit(f"Missing environment variable {name}")
    return value


BASE = env("WP_URL").rstrip("/") + "/wp-json"


def headers():
    user, pw = env("WP_USER", False), env("WP_APP_PASSWORD", False)
    h = {"Accept": "application/json", "User-Agent": "wowstyle-manager"}
    if user and pw:
        token = base64.b64encode(f"{user}:{pw}".encode()).decode()
        h["Authorization"] = f"Basic {token}"
    return h


def request(method, path, params=None, body=None):
    url = BASE + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    data = None
    h = headers()
    if body is not None:
        data = json.dumps(body).encode()
        h["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.load(resp), resp.headers
    except urllib.error.HTTPError as e:
        sys.exit(f"{method} {url} -> {e.code}: {e.read().decode(errors='replace')[:500]}")


def get_all(path, params=None):
    """Fetch every page of a collection endpoint."""
    params = dict(params or {}, per_page=100, page=1)
    items = []
    while True:
        batch, h = request("GET", path, params)
        items.extend(batch)
        if params["page"] >= int(h.get("X-WP-TotalPages", 1)):
            return items
        params["page"] += 1


def check():
    site, _ = request("GET", "/")
    print(f"Site: {site.get('name')} — {site.get('description')}")
    print(f"URL:  {site.get('url')}")
    print(f"Namespaces: {', '.join(site.get('namespaces', []))}")
    if "Authorization" in headers():
        me, _ = request("GET", "/wp/v2/users/me", {"context": "edit"})
        print(f"Logged in as: {me.get('name')} (roles: {', '.join(me.get('roles', []))})")
    else:
        print("No credentials set: read-only public access.")


def inventory():
    status = "publish,draft,pending,private,future" if "Authorization" in headers() else "publish"
    ctx = {"context": "edit"} if "Authorization" in headers() else {}
    out = {
        "posts": get_all("/wp/v2/posts", dict(ctx, status=status)),
        "pages": get_all("/wp/v2/pages", dict(ctx, status=status)),
        "categories": get_all("/wp/v2/categories"),
        "tags": get_all("/wp/v2/tags"),
        "media": get_all("/wp/v2/media"),
    }
    json.dump(out, sys.stdout, indent=1)
    print(file=sys.stderr)
    for k, v in out.items():
        print(f"{k}: {len(v)}", file=sys.stderr)


def main(argv):
    if not argv:
        sys.exit(__doc__)
    cmd, args = argv[0], argv[1:]
    if cmd == "check":
        check()
    elif cmd == "inventory":
        inventory()
    elif cmd == "get" and len(args) == 2:
        item, _ = request("GET", f"/wp/v2/{args[0]}/{args[1]}", {"context": "edit"})
        json.dump(item, sys.stdout, indent=1)
    elif cmd == "update" and len(args) == 3:
        item, _ = request("POST", f"/wp/v2/{args[0]}/{args[1]}", body=json.loads(args[2]))
        print(f"Updated {args[0]}/{item['id']}: {item.get('link')}")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
