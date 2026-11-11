import hashlib as hs
import pathlib as pth

from utils import flatten_iterable

KB = 1024
MB = KB * 1024
GB = MB * 1024


def partial_hash(file: pth.Path, size: int = 4 * KB) -> str:
    h = hs.sha256()

    with file.open("rb") as f:
        h.update(f.read(size))

        if file.stat().st_size > size:
            f.seek(-size, 2)
            h.update(f.read(size))

    return h.hexdigest()


def sha256_file(file: pth.Path, chunk_size: int = MB) -> str:
    h = hs.sha256()

    with open(file, "rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


def filter_by_size(files: list[pth.Path]) -> list[pth.Path]:
    sizes: dict[int, list[pth.Path]] = {}
    for f in files:
        sizes.setdefault(f.stat().st_size, []).append(f)
    sizes = {s: fs for s, fs in sizes.items() if len(fs) > 1}
    return flatten_iterable(sizes.values())


def find_partial_hashes(files: list[pth.Path], size: int = 4 * KB) -> dict[str, list[pth.Path]]:
    hashes: dict[str, list[pth.Path]] = {}

    for f in files:
        h = partial_hash(f, size=size)
        hashes.setdefault(h, []).append(f)
    return hashes


def find_hashes(files: list[pth.Path]) -> dict[str, list[pth.Path]]:
    hashes: dict[str, list[pth.Path]] = {}

    for f in files:
        h = sha256_file(f)
        if h in hashes:
            hashes[h].append(f)
        else:
            hashes[h] = [f]
    return hashes


def find_duplicates(files: list[pth.Path]) -> dict[str, list[pth.Path]]:
    sized = filter_by_size(files)
    for s in (4 * KB, 4 * MB):
        sized = find_partial_hashes(sized, s)
        sized = flatten_iterable(sized.values(), 1)
    sized = find_hashes(sized)
    return {h: p for h, p in sized.items() if len(p) > 1}
