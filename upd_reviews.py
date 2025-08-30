#!/usr/bin/env python3
import argparse
import math
import re
import os
import logging
from collections import defaultdict
from typing import Tuple, List
from dataclasses import dataclass

COMMON_FRONT_MATTER="""build:
  list: never
"""
COMMON_TEXT="""
*I'm [writing my mini-reviews](/post/2021/05/23/taking-notes/) since 2013, just for fun.*
*The reviews are not published (yet?), but the scores are.*

*All scores are given on a scale from 0 to 10, with exceptional titles given 11 (because why not?).*
"""

@dataclass
class Category:
    name: str
    alt_name: str
    header: str
    output_filename: str

categories = [
    Category(
        name="Games",
        alt_name="Игры",
        header=f"""---
title: Video Game Reviews
{COMMON_FRONT_MATTER}
---

Here you can find my review scores for video games I played.

{COMMON_TEXT}
""",
        output_filename="video-games.md",
    ),
    Category(
        name="Music",
        alt_name="Музыка",
        header=f"""---
title: Music Album Reviews
{COMMON_FRONT_MATTER}
---

Here you can find my review scores for the music albums I extensively listened to.

Which almost always means that I [bought them on Bandcamp](https://bandcamp.com/lazywolf0).

{COMMON_TEXT}
""",
        output_filename="music.md",
    ),
    Category(
        name="Books",
        alt_name="Книги",
        header=f"""---
title: Book Reviews
{COMMON_FRONT_MATTER}
---

Here you can find my review scores for the books I read.

I largely read e-books on my Kindle, although almost all of the books related to ships and sailing are part of my small but dear to me **maritime library**.

{COMMON_TEXT}
""",
        output_filename="books.md",
    ),
]


def matches_category(line: str) -> Tuple[str, int]:
    for cat in categories:
        match = re.match(r"^(%s|%s)\s+(\d{4})$" % (cat.name, cat.alt_name), line)
        if match:
            return (cat.name, int(match.group(2)))
    return ("", 0)


def parse_reviews(lines: List[str]) -> List[Tuple[str, int]]:
    results = []
    cur_title = ""
    for line in lines:
        line = line.strip()
        if not cur_title:
            match = re.match(r"\*\*(.+)\*\*$", line)
            if match:
                cur_title = match.group(1)
            else:
                match = re.match(r"## (.+)$", line)
                if match:
                    cur_title = match.group(1)
        if cur_title:
            match = re.search(r".*?([0-9.]+)/10.*", line)
            if match:
                cur_score = match.group(1)
                results.append((cur_title, math.ceil(float(cur_score))))
                cur_title = ""

        if len(line) == 0:
            if cur_title:
                logging.warning("no score found for %s", cur_title)
            cur_title = ""

    return results


def main():
    parser = argparse.ArgumentParser(description="Update reviews page")
    parser.add_argument("files", metavar='file', type=str, nargs='*',
                            help='file to convert')
    parser.add_argument("--output", default="./content/reviews", type=str,
                            help='output')

    args = parser.parse_args()

    toWrite = defaultdict(lambda: defaultdict(list))
    for filename in args.files:
        if os.path.isdir(filename):
            logging.warning("skipping directory %s", filename)
            continue
        with open(filename, 'r') as f:
            try:
                data = f.readlines()
            except Exception as e:
                logging.error("failed to read %s: %s", filename, e)
                continue
            if len(data) < 2:
                continue
            category, year = matches_category(data[0])
            if category:
                reviews = parse_reviews(data)
                reviews.sort(key=lambda x: x[1], reverse=True)
                for name, score in reviews:
                    toWrite[category][year].append("| {} | {} |".format(name, score))

    for cat in categories:
        if not toWrite[cat.name]:
            continue
        out = os.path.join(args.output, cat.output_filename)
        with open(out, "w") as f:
            f.write(cat.header+"\n\n")
            years = sorted(toWrite[cat.name].keys(), reverse=True)
            f.write("Reviews per year: ")
            f.write(", ".join([f"[{year}](#{year})" for year in years]))
                
            for year in years:
                if toWrite[cat.name][year]:
                    f.write(f'<h2 id="{year}" style="text-align: center;">{year}</h2>\n\n')
                    f.write("| Name | Score |\n")
                    f.write("|------|-------|\n")
                    for line in toWrite[cat.name][year]:
                        f.write(line+"\n")
                    f.write("\n")

    logging.info("done")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()

