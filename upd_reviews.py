#!/usr/bin/env python3
import argparse
import math
import os
import sys
import logging
from collections import defaultdict
from typing import Tuple, List, Dict, Optional
from dataclasses import dataclass
import logging
from trilium_py.client import ETAPI


COMMON_FRONT_MATTER = """build:
  list: never
"""
COMMON_TEXT = """
*I'm [writing my mini-reviews](/post/2021/05/23/taking-notes/) since 2013, just for fun.*
*The reviews are not published (yet?), but the scores are.*

*All scores are given on a scale from 0 to 10, with exceptional titles given 11 (because why not?).*
"""


@dataclass
class Category:
    name: str
    header: str
    output_filename: str


categories = [
    Category(
        name="Games",
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
        header=f"""---
title: Book Reviews
{COMMON_FRONT_MATTER}
---

Here you can find my review scores for the books I read.

I largely read e-books on my eReader, although almost all of the books related to ships and sailing are part of my small but dear to me **maritime library**.

{COMMON_TEXT}
""",
        output_filename="books.md",
    ),
]


def find_category_ancestors(ea: ETAPI) -> Dict[str, Category]:
    cats = {}
    for cat in categories:
        res = ea.search_note(
            search=f"note.title %= '^{cat.name}$'",
            fastSearch=True,
            orderBy=["title"],
        )
        if len(res["results"]) != 1:
            logging.error(f"need exactly one result for category {cat.name}, got {res}")
            continue
        noteID: str = res["results"][0]["noteId"]
        cats[noteID] = cat
    return cats


def find_reviews_note(ea: ETAPI, parent: str) -> str:
    res = ea.search_note(
        search=r"note.title %= '^Reviews$'",
        ancestorNoteId=parent,
        fastSearch=True,
        orderBy=["title"],
    )
    if len(res["results"]) != 1:
        logging.error(f"need exactly one result for Reviews, got {res}")
        return ""
    return res["results"][0]["noteId"]


def find_year_notes(ea: ETAPI, parent: str) -> List[Tuple[str, int]]:
    res = ea.search_note(
        search=r"note.title %= '^[0123456789]{4}$'",
        ancestorNoteId=parent,
        fastSearch=True,
        orderBy=["title"],
    )
    return [(note["noteId"], int(note["title"])) for note in res["results"]]


def find_children(ea: ETAPI, parent: str) -> List[str]:
    res = ea.search_note(
        search=r"note.title %= '.*'",
        ancestorNoteId=parent,
        fastSearch=True,
        orderBy=["title"],
    )
    return [note["noteId"] for note in res["results"]]


def get_score(attributes: List[Dict[str, str]]) -> Optional[float]:
    for attr in attributes:
        if attr["name"] == "Score":
            if attr["value"]:
                return math.ceil(float(attr["value"]))
    return None


def main():
    parser = argparse.ArgumentParser(description="Update reviews page")
    parser.add_argument(
        "--output", default="./content/reviews", type=str, help="output"
    )
    parser.add_argument(
        "--address",
        default="http://localhost:37840",
        type=str,
        help="address of the Trilium server, including port",
    )

    etapi_key = os.getenv("TRILIUM_ETAPI_KEY")
    if not etapi_key:
        logging.error("no ETAPI key found in TRILIUM_ETAPI_KEY env var")
        sys.exit(1)

    args = parser.parse_args()

    ea = ETAPI(args.address, etapi_key)

    note_id_to_cat = find_category_ancestors(ea)

    for category_parent_note_id, cat in note_id_to_cat.items():
        logging.info(f"processing category {cat.name}")
        parent_note_id = find_reviews_note(ea, category_parent_note_id)
        if not parent_note_id:
            continue

        years = find_year_notes(ea, parent_note_id)
        toWrite: Dict[int, List[Tuple[str, float]]] = defaultdict(list)
        for note_id, year in years:
            logging.debug("%d", year)
            res = ea.traverse_note_tree(note_id, depth=2, limit=1000)
            for x in res:
                # ignore the year node itself and all nodes under the review
                if x["depth"] != 2:
                    continue
                n = ea.get_note(x["noteId"])
                score = get_score(n["attributes"])
                if not score:
                    logging.warning("no score found for %s", x["title"])
                    continue
                logging.debug("%d: %s: %s", year, x["title"], score)
                toWrite[year].append((x["title"], score))

        out = os.path.join(args.output, cat.output_filename)
        with open(out, "w") as f:
            f.write(cat.header + "\n\n")
            years = sorted(toWrite.keys(), reverse=True)
            f.write("Reviews per year: ")
            f.write(", ".join([f"[{year}](#{year})" for year in years]))

            for year in years:
                reviews = toWrite[year]
                logging.info("%d reviews in %s", len(reviews), year)
                # first sort by name
                reviews.sort(key=lambda x: x[0])
                # then sort by score, this way we make sure the output is stable
                reviews.sort(key=lambda x: x[1], reverse=True)
                if reviews:
                    f.write(
                        f'<h2 id="{year}" style="text-align: center;">{year}</h2>\n\n'
                    )
                    f.write("| Name | Score |\n")
                    f.write("|------|-------|\n")
                    for name, score in reviews:
                        f.write("| {} | {} |\n".format(name, score))
                    f.write("\n")

    logging.info("done")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
