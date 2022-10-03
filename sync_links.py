#!/usr/bin/env python3
import os
import shutil
import sys

NEW="https://bulimov.me/"
INDEX_HTML="index.html"
INDEX_XML="index.xml"
DIR="post"
ROOT="./public"
TARGET=sys.argv[1]

TEMPLATE="""
<!DOCTYPE html>
<meta charset="utf-8">
<title>Redirecting to {target}</title>
<meta http-equiv="refresh" content="0; URL={target}">
<link rel="canonical" href="{target}">
"""

r = os.path.join(ROOT, DIR)
for root, subdirs, files in os.walk(r):
    for fname in files:
        if fname != INDEX_HTML:
            continue
        rp = os.path.relpath(root, ROOT)
        print("processing " + rp)
        os.makedirs(os.path.join(TARGET, rp), exist_ok=True)
        with open(os.path.join(TARGET, rp, INDEX_HTML), "w") as f:
            f.write(TEMPLATE.format(target=NEW+rp+"/"))

print("processing index.xml")
shutil.copyfile(
    os.path.join(ROOT, INDEX_XML),
    os.path.join(TARGET, INDEX_XML),
)
print("redirect sync done")

