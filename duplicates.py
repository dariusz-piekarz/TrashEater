"""Find duplicate files by comparing their content hashes."""

import hashlib as hs
import pathlib as pth

from utils import flatten_iterable

KB = 1024
MB = KB * 1024
GB = MB * 1024


def partial_hash(file: pth.Path, size: int = 4 * KB) -> str:
    """Hash the first and, when needed, last ``size`` bytes of a file.

    Parameters
    ----------
    file : pathlib.Path
        File to hash.
    size : int, default=4 * KB
        Number of bytes to read from each end when the file is larger than
        ``size``.

    Returns
    -------
    str
        Hexadecimal SHA-256 digest of the selected bytes.
    """
    h = hs.sha256()

    with file.open("rb") as f:
        h.update(f.read(size))

        if file.stat().st_size > size:
            f.seek(-size, 2)
            h.update(f.read(size))

    return h.hexdigest()


def sha256_file(file: pth.Path, chunk_size: int = MB) -> str:
    """Compute a SHA-256 digest of a file.

    Parameters
    ----------
    file : pathlib.Path
        File to hash.
    chunk_size : int, default=MB
        Number of bytes to read per iteration.

    Returns
    -------
    str
        Hexadecimal SHA-256 digest of the file contents.
    """
    h = hs.sha256()

    with open(file, "rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


def filter_by_size(files: list[pth.Path]) -> list[pth.Path]:
    """Keep files whose size is shared by at least one other input file.

    Parameters
    ----------
    files : list of pathlib.Path
        Files to group by their byte size.

    Returns
    -------
    list of pathlib.Path
        Files in size groups containing two or more paths.
    """
    sizes: dict[int, list[pth.Path]] = {}
    for f in files:
        sizes.setdefault(f.stat().st_size, []).append(f)
    sizes = {s: fs for s, fs in sizes.items() if len(fs) > 1}
    return flatten_iterable(sizes.values())


def find_partial_hashes(
    files: list[pth.Path], size: int = 4 * KB
) -> dict[str, list[pth.Path]]:
    """Group files by hashes of selected leading and trailing bytes.

    Parameters
    ----------
    files : list of pathlib.Path
        Files to hash.
    size : int, default=4 * KB
        Number of bytes selected from each end of each file.

    Returns
    -------
    dict of str to list of pathlib.Path
        Partial SHA-256 digests mapped to matching input paths.
    """
    hashes: dict[str, list[pth.Path]] = {}

    for f in files:
        h = partial_hash(f, size=size)
        hashes.setdefault(h, []).append(f)
    return hashes


def find_hashes(files: list[pth.Path]) -> dict[str, list[pth.Path]]:
    """Group files by their complete SHA-256 digest.

    Parameters
    ----------
    files : list of pathlib.Path
        Files to hash.

    Returns
    -------
    dict of str to list of pathlib.Path
        Full SHA-256 digests mapped to matching input paths.
    """
    hashes: dict[str, list[pth.Path]] = {}

    for f in files:
        h = sha256_file(f)
        if h in hashes:
            hashes[h].append(f)
        else:
            hashes[h] = [f]
    return hashes


def find_duplicates(files: list[pth.Path]) -> dict[str, list[pth.Path]]:
    """Find groups of files with identical contents.

    Candidates are narrowed by file size and partial hashes before comparing
    complete SHA-256 digests.

    Parameters
    ----------
    files : list of pathlib.Path
        Files to compare.

    Returns
    -------
    dict of str to list of pathlib.Path
        Full SHA-256 digests mapped to groups of duplicate files. Unique files
        are omitted.
    """
    sized = filter_by_size(files)
    for s in (4 * KB, 4 * MB):
        sized = find_partial_hashes(sized, s)
        sized = flatten_iterable(sized.values(), 1)
    sized = find_hashes(sized)
    return {h: p for h, p in sized.items() if len(p) > 1}
