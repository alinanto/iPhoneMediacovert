#!/usr/bin/env python3
"""Move image and video files from the current folder into Images and Videos folders."""

from __future__ import annotations
import argparse
from pathlib import Path

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff', '.heic', '.webp'}
VIDEO_EXTENSIONS = {'.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.webm'}


def move_media(root: Path) -> None:
    images_folder = root / 'Images'
    videos_folder = root / 'Videos'
    images_folder.mkdir(exist_ok=True)
    videos_folder.mkdir(exist_ok=True)

    for item in root.iterdir():
        if not item.is_file():
            continue
        if item.parent == images_folder or item.parent == videos_folder:
            continue

        ext = item.suffix.lower()
        if ext in IMAGE_EXTENSIONS:
            item.rename(images_folder / item.name)
        elif ext in VIDEO_EXTENSIONS:
            item.rename(videos_folder / item.name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Move images to Images and videos to Videos folders.')
    parser.add_argument(
        'path', nargs='?', default='.', help='Root folder to sort (default: current directory)'
    )
    args = parser.parse_args()
    root_path = Path(args.path).expanduser().resolve()
    move_media(root_path)
    print(f"Done. Images moved to '{root_path / 'Images'}' and videos moved to '{root_path / 'Videos'}'.")
