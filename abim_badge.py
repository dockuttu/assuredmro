# -*- coding: utf-8 -*-
"""abim_badge.py - put Dr. Arora's ABIM board-certification badge in every page footer.

Run near the end of build.sh, after the site has been generated:

    python3 abim_badge.py bundle/site      # or: python3 abim_badge.py site

The badge image is served from the WordPress media library on serenemedspas.com,
the same place these sites already pull the Serene logo from, so no asset needs
to live in this repo. Idempotent - pages that already carry the badge are
skipped, so it is safe to run on every build.
"""
import os
import sys

SITE = sys.argv[1] if len(sys.argv) > 1 else "site"

IMG = ("https://serenemedspas.com/wp-content/uploads/2026/09/"
       "57916afd-d9a0-4cb8-8618-dbcce3f41000.png")
VERIFY = "https://badges.abim.org/5fd362be-e972-4798-ad03-bc41774dc4c6"
MARKER = 'id="abim-cred"'

BLOCK = (
    '<div %s style="max-width:1100px;margin:26px auto 0;padding:0 20px;display:flex;'
    'gap:14px;align-items:center;color:inherit">'
    '<a href="%s" target="_blank" rel="noopener" style="flex:0 0 auto;line-height:0">'
    '<img src="%s" width="60" height="60" loading="lazy" decoding="async" '
    'alt="American Board of Internal Medicine - Board Certified" '
    'style="width:60px;height:60px;display:block"></a>'
    '<p style="margin:0;font-size:14px;line-height:1.45;color:inherit">'
    '<strong>Robin Arora, MD</strong> &middot; Board certified by the American Board of '
    'Internal Medicine &middot; <a href="%s" target="_blank" rel="noopener" '
    'style="color:inherit;text-decoration:underline">Verify</a></p></div>'
) % (MARKER, VERIFY, IMG, VERIFY)


def inject(doc):
    if MARKER in doc:
        return doc, False
    i = doc.rfind("</footer>")
    if i == -1:
        return doc, False
    return doc[:i] + BLOCK + doc[i:], True


def main():
    if not os.path.isdir(SITE):
        print("abim_badge: no such directory:", SITE)
        return
    done = skipped = 0
    for root, _, files in os.walk(SITE):
        for f in files:
            if not f.endswith(".html"):
                continue
            p = os.path.join(root, f)
            with open(p, encoding="utf-8") as fh:
                doc = fh.read()
            new, changed = inject(doc)
            if changed:
                with open(p, "w", encoding="utf-8") as fh:
                    fh.write(new)
                done += 1
            else:
                skipped += 1
    print("abim_badge: added to %d pages (%d skipped)" % (done, skipped))


if __name__ == "__main__":
    main()
