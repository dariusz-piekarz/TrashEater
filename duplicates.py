import hashlib as hs
import pathlib as pth


def partial_hash(file: pth.Path, size: int = 4096) -> str:
    h = hs.sha256()

    with file.open("rb") as f:
        h.update(f.read(size))

    return h.hexdigest()


def sha256_file(path: pth.Path, chunk_size: int = 1024*1024) -> str:
    h = hs.sha256()

    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)

    return h.hexdigest()


def group_by_size(files: list[pth.Path]) -> list[pth.Path]:
    sizes: dict[int, list[pth.Path]] = {}
    for f in files:
        if (s := f.stat().st_size) in sizes:
            sizes[s].append(f)
        else:
            sizes[s] = [f]
    sizes = {s: fs for s, fs in sizes.items() if len(fs) > 1}
    return [f for files in sizes.values() for f in files]


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
    sized = group_by_size(files)
    sized = find_hashes(sized)
    return {h: p for h, p in sized.items() if len(p) > 1}