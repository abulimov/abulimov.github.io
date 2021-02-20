#!/usr/bin/env python3
import argparse
import os
import sys

from wand.image import Image


def main():
    parser = argparse.ArgumentParser(description="Add new image(s) to content/images folder")
    parser.add_argument("files", metavar='file', type=str, nargs='*',
                            help='file to convert')
    parser.add_argument("--size", default=1920, type=int,
                            help='size to resize')
    parser.add_argument("--quality", default=80, type=int,
                            help='compression quality')

    args = parser.parse_args()
    dir_path = os.path.join("content", "images")
    for filename in args.files:
        with Image(filename=filename) as img:
            name = os.path.basename(filename)
            new_path = os.path.join(dir_path, name)
            with img.clone() as i:
                i.compression_quality = args.quality
                i.transform("", str(args.size))
                i.strip()
                i.save(filename=new_path)
                print(f"Saved {new_path}")

if __name__ == "__main__":
    main()
