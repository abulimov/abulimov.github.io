#!/usr/bin/env python3
import argparse
import math
import re
import logging
from collections import defaultdict
from typing import Tuple, List


categories = {
    "Игры": "Games",
    "Музыка": "Music",
    "Книги": "Books",
}

def matches_category(line: str) -> Tuple[str, int]:
    for k, v in categories.items():
        match = re.match(r"^%s\s+(\d{4})$" % k, line)
        if match:
            return (v, int(match.group(1)))
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
        if cur_title:
            match = re.search(r".+\s+([0-9.]+)/10.*", line)
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
    parser.add_argument("--output", default="./content/reviews.md", type=str,
                            help='output')
    parser.add_argument("--header", default="./content/reviews_head.md.txt", type=str,
                            help='header to prepend to the output')

    args = parser.parse_args()

    toWrite = defaultdict(lambda: defaultdict(list))
    for filename in args.files:
        with open(filename, 'r') as f:
            data = f.readlines()
            if len(data) < 2:
                continue
            category, year = matches_category(data[0])
            if category:
                reviews = parse_reviews(data)
                reviews.sort(key=lambda x: x[1], reverse=True)
                for name, score in reviews:
                    toWrite[category][year].append("| {} | {} |".format(name, score))

    with open(args.header, 'r') as f:
        head = f.read()

    with open(args.output, "w") as f:
        f.write(head)
        for cat in ["Games", "Books", "Music"]:
            f.write("## {}\n".format(cat))
            f.write("| Name | Score |\n")
            f.write("|------|-------|\n")
            years = sorted(toWrite[cat].keys(), reverse=True)
            for year in years:
                if toWrite[cat][year]:
                    f.write("| **{}** |\n".format(year))
                    for line in toWrite[cat][year]:
                        f.write(line+"\n")

    logging.info("done")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()

