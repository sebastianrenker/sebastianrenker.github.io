#!/usr/bin/env python3
"""Cross-post a page of this site as a short teaser with a canonical link.

Stdlib only. Dry-run by default; nothing is sent without --send.
Targets (each only if its credentials are present in the environment):
  devto    DEVTO_API_KEY                      -> draft article (published=false unless --publish)
  bluesky  BSKY_HANDLE + BSKY_APP_PASSWORD    -> one post with a clickable link

Usage: python scripts/crosspost.py <path/to/index.html> [--send] [--publish] [--tags a,b,c]
"""
import argparse, html, json, os, re, sys, urllib.request

SITE = "https://sebastianrenker.github.io"


def meta(t, pat):
    m = re.search(pat, t, re.S)
    return html.unescape(m.group(1)).strip() if m else None


def read_page(path):
    t = open(path, encoding="utf-8").read()
    title = meta(t, r"<title>(.*?)</title>")
    desc = meta(t, r'<meta name="description" content="(.*?)"')
    url = meta(t, r'<link rel="canonical" href="(.*?)"')
    if not (title and desc and url and url.startswith(SITE + "/")):
        sys.exit("page needs <title>, meta description and a canonical URL on " + SITE)
    return title, desc, url


def post_json(url, payload, headers):
    req = urllib.request.Request(url, json.dumps(payload).encode(), {"Content-Type": "application/json", **headers})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode() or "{}")


def devto(title, desc, url, tags, publish, send):
    key = os.environ.get("DEVTO_API_KEY")
    body = f"{desc}\n\n**Read the full post:** {url}\n\n*Originally published at {url}.*"
    art = {"article": {"title": title, "body_markdown": body, "published": publish,
                       "canonical_url": url, "tags": tags[:4]}}
    if not send or not key:
        print("[devto] DRY-RUN" if key or not send else "[devto] skipped: no DEVTO_API_KEY"); print(json.dumps(art, indent=1)[:600]); return
    r = post_json("https://dev.to/api/articles", art, {"api-key": key})
    print("[devto] created", r.get("url"), "published=" + str(r.get("published")))


def bluesky(title, desc, url, send):
    h, pw = os.environ.get("BSKY_HANDLE"), os.environ.get("BSKY_APP_PASSWORD")
    room = 300 - len(url) - 2
    text = f"{title}\n\n{desc}"
    if len(text) > room:
        text = text[: room - 1].rstrip() + "…"
    text = f"{text}\n{url}"
    start = len(text[: text.rindex(url)].encode())
    facets = [{"index": {"byteStart": start, "byteEnd": start + len(url.encode())},
               "features": [{"$type": "app.bsky.richtext.facet#link", "uri": url}]}]
    if not send or not (h and pw):
        print("[bluesky] DRY-RUN" if (h and pw) or not send else "[bluesky] skipped: no credentials"); print(text); return
    s = post_json("https://bsky.social/xrpc/com.atproto.server.createSession", {"identifier": h, "password": pw}, {})
    rec = {"$type": "app.bsky.feed.post", "text": text, "facets": facets, "langs": ["en"],
           "createdAt": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat().replace("+00:00", "Z")}
    r = post_json("https://bsky.social/xrpc/com.atproto.repo.createRecord",
                  {"repo": s["did"], "collection": "app.bsky.feed.post", "record": rec},
                  {"Authorization": "Bearer " + s["accessJwt"]})
    print("[bluesky] posted", r.get("uri"))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("page"); ap.add_argument("--send", action="store_true")
    ap.add_argument("--publish", action="store_true", help="dev.to: publish instead of saving a draft")
    ap.add_argument("--tags", default="ai,security,python")
    a = ap.parse_args()
    title, desc, url = read_page(a.page)
    tags = [x.strip() for x in a.tags.split(",") if x.strip()]
    devto(title, desc, url, tags, a.publish, a.send)
    bluesky(title, desc, url, a.send)
