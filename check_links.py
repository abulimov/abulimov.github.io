#!/usr/bin/python3
import re
import sys
import stat
import os
import argparse


# not a full URL regexp, but good enough for what could be found in this blog
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")


def find_links(line: str) -> list[str]:
    return [url for _, url in LINK_RE.findall(line)]


def parse_file(path: str) -> list[tuple[int, str]]:
    line_no = 0
    results = []
    with open(path, "r") as f:
        for line in f:
            line_no += 1
            for match in find_links(line):
                results.append((line_no, match))
    return results


def is_valid_target(site_root: str, target: str) -> bool:
    if target.startswith("//"):
        # no protocol-relative links
        return False
    if target.startswith("http://") or target.startswith("https://"):
        return True
    if target.startswith("/"):
        return is_valid_relative_target(site_root, target)
    return False


def is_valid_relative_target(site_root: str, target: str) -> bool:
    try:
        target = target.lstrip("/").split("#", 1)[0].split("?", 1)[0]
        full_target = os.path.join(site_root, target)
        mode = os.lstat(full_target).st_mode
        if stat.S_ISDIR(mode):
            full_target = os.path.join(full_target, "index.html")
        mode = os.lstat(full_target).st_mode
        return not stat.S_ISDIR(mode)
    except FileNotFoundError:
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+")
    parser.add_argument("--site-root", default="./public")
    args = parser.parse_args()

    found_problems = 0

    for input in args.inputs:
        links = parse_file(input)
        first_problem_in_file = True
        for line_no, link in links:
            if not is_valid_target(args.site_root, link):
                found_problems += 1
                if first_problem_in_file:
                    print(input)
                    first_problem_in_file = False
                print(f"{line_no}: bad link {link}")
    if found_problems:
        print(f"❌ found {found_problems} bad links")
        sys.exit(1)
    print("✅ no bad links found")


if __name__ == "__main__":
    main()
