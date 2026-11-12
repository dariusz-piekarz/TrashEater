"""Demonstrate the file-inspection utilities."""

import argparse
from pathlib import Path

from trash_eater import (
    broken_images,
    empty_files,
    find_duplicates,
    image_duplicates,
    similar_images,
    tiny_images,
)


IMAGE_EXTENSIONS = {".bmp", ".jpg", ".jpeg", ".png", ".webp"}


def main() -> None:
    """Print duplicate, empty, and problematic-file reports for a folder."""
    parser = argparse.ArgumentParser(
        description="Report duplicate, empty, and problematic files."
    )
    parser.add_argument("folder", type=Path, help="folder to inspect")
    args = parser.parse_args()

    if not args.folder.is_dir():
        parser.error(f"{args.folder} is not a directory")

    files = [path for path in args.folder.rglob("*") if path.is_file()]
    print("Duplicate files:")
    for group in find_duplicates(files).values():
        print("  " + ", ".join(str(path) for path in group))

    print("Empty files:")
    for path in empty_files(args.folder):
        print(f"  {path}")

    image_files = [
        path for path in files if path.suffix.lower() in IMAGE_EXTENSIONS
    ]
    broken = set(broken_images(image_files))
    print("Broken images:")
    for path in sorted(broken):
        print(f"  {path}")

    valid_images = [path for path in image_files if path not in broken]
    print("Duplicate images:")
    for group in image_duplicates(valid_images).values():
        print("  " + ", ".join(str(path) for path in group))

    print("Similar images:")
    for first, second in similar_images(valid_images):
        print(f"  {first} <-> {second}")

    print("Tiny images:")
    for path in tiny_images(valid_images):
        print(f"  {path}")


if __name__ == "__main__":
    main()
