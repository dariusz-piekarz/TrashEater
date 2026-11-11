from collections.abc import Iterable
from typing import Any

import pathlib as pth


def flatten_iterable(
    it: Iterable[Iterable[Any]], size: int | None = None
) -> list[Any]:
    """Flatten groups, optionally keeping only groups larger than ``size``."""
    return [
        item
        for group in it
        if size is None or len(group) > size
        for item in group
    ]


def filter_files(
    files: list[pth.Path], by: frozenset[str]
) -> list[pth.Path]:
    matches: list[pth.Path] = []
    for file in files:
        suffixes = [suffix.lower() for suffix in file.suffixes]
        candidates = set(suffixes)
        if len(suffixes) >= 2:
            candidates.add("".join(suffixes[-2:]))
        if file.name.lower() in by or candidates.intersection(by):
            matches.append(file)
    return matches
