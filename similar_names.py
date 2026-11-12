"""Find file paths with similar names."""

import pathlib as pth
from rapidfuzz.fuzz import ratio
from itertools import combinations


def similar_names(
    files: list[pth.Path],
    threshold: int = 85,
) -> list[tuple[pth.Path, pth.Path]]:
    """Find path pairs whose filename stems have a high similarity ratio.

    Parameters
    ----------
    files : list of pathlib.Path
        Paths whose stems are compared pairwise.
    threshold : int, default=85
        Minimum RapidFuzz ratio, from 0 to 100, required for a pair.

    Returns
    -------
    list of tuple of pathlib.Path
        Matching path pairs in combination order.
    """
    pairs: list[tuple[pth.Path, pth.Path]] = []

    for f1, f2 in combinations(files, 2):
        if ratio(f1.stem, f2.stem) >= threshold:
            pairs.append((f1, f2))

    return pairs
