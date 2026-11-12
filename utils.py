from collections.abc import Iterable
from typing import Any

import pathlib as pth


def flatten_iterable(
    it: Iterable[Iterable[Any]], size: int | None = None
) -> list[Any]:
    """Flatten groups, optionally keeping only groups larger than a limit.

    Parameters
    ----------
    it : iterable of iterables
        Groups whose items are concatenated in iteration order.
    size : int or None, optional
        When provided, keep only groups with more than ``size`` items. Groups
        must support ``len`` when this option is used.

    Returns
    -------
    list
        Items from the retained groups, in their original order.
    """
    return [
        item
        for group in it
        if size is None or len(group) > size
        for item in group
    ]


def filter_files(
    files: list[pth.Path], by: frozenset[str]
) -> list[pth.Path]:
    """Select paths by filename, extension, or compound extension.

    Matching is case-insensitive. For compound extensions, the final two
    suffixes are also checked together (for example, ``.synctex.gz``).

    Parameters
    ----------
    files : list of pathlib.Path
        Paths to inspect.
    by : frozenset of str
        Lowercase filenames or suffixes to match.

    Returns
    -------
    list of pathlib.Path
        Matching paths in their original order.
    """
    matches: list[pth.Path] = []
    for file in files:
        suffixes = [suffix.lower() for suffix in file.suffixes]
        candidates = set(suffixes)
        if len(suffixes) >= 2:
            candidates.add("".join(suffixes[-2:]))
        if file.name.lower() in by or candidates.intersection(by):
            matches.append(file)
    return matches
