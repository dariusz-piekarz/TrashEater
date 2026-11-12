import imagehash as ih
import pathlib as pth

from itertools import combinations
from PIL import Image, UnidentifiedImageError
from PIL.Image import open as image_open

from utils import filter_files

IMAGE_EXTESIONS = frozenset({".jpg", ".jpeg", ".png", ".bmp", ".webp"})


def image_duplicates(
    files: list[pth.Path],
) -> dict[ih.ImageHash, list[pth.Path]]:
    """Group supported images that have identical perceptual hashes.

    Parameters
    ----------
    files : list of pathlib.Path
        Paths to inspect. Only supported image extensions are considered.

    Returns
    -------
    dict of ImageHash to list of pathlib.Path
        Perceptual hashes mapped to groups with at least two paths.
    """
    ffiles = filter_files(files, IMAGE_EXTESIONS)
    hashes: dict[ih.ImageHash, list[pth.Path]] = {}
    for f in ffiles:
        with image_open(f) as im:
            hs = ih.phash(im)
            hashes.setdefault(hs, []).append(f)
    return {h: p for h, p in hashes.items() if len(p) > 1}


def similar_images(
    files: list[pth.Path], similarity_lvl: int = 6
) -> list[tuple[pth.Path, pth.Path]]:
    """Find image pairs within a perceptual-hash distance threshold.

    Candidates are compared only when their hashes share the same leading
    12-bit bucket.

    Parameters
    ----------
    files : list of pathlib.Path
        Paths to inspect. Only supported image extensions are considered.
    similarity_lvl : int, default=6
        Maximum Hamming distance between perceptual hashes.

    Returns
    -------
    list of tuple of pathlib.Path
        Matching image-path pairs.
    """
    ffiles = filter_files(files, IMAGE_EXTESIONS)

    buckets: dict[int, list[tuple[ih.ImageHash, pth.Path]]] = {}
    for f in ffiles:
        with image_open(f) as im:
            fhs = ih.phash(im)
            hs = int(str(fhs), 16)  # hash image converted into 16-numeral int
            bc = hs >> 52  # take only first 12-most significant bits
            buckets.setdefault(bc, []).append((fhs, f))

    pairs: list[tuple[pth.Path, pth.Path]] = []

    for bucket in buckets.values():
        if len(bucket) < 2:
            continue

        for (h1, f1), (h2, f2) in combinations(bucket, 2):
            if h1 - h2 <= similarity_lvl:
                pairs.append((f1, f2))

    return pairs


def broken_images(files: list[pth.Path]) -> list[pth.Path]:
    """Find supported image files that cannot be verified as images.

    Parameters
    ----------
    files : list of pathlib.Path
        Paths to inspect. Only supported image extensions are considered.

    Returns
    -------
    list of pathlib.Path
        Supported image paths that fail image verification.
    """
    ffiles = filter_files(files, IMAGE_EXTESIONS)
    bf: list[pth.Path] = []
    for f in ffiles:
        try:
            with Image.open(f) as image:
                image.verify()
        except (OSError, UnidentifiedImageError):
            bf.append(f)
    return bf


def tiny_images(files: list[pth.Path],
                max_pixels: int = 128 * 128,
                ) -> list[pth.Path]:
    """Find readable images at or below a pixel-count limit.

    Paths that cannot be opened as images are skipped.

    Parameters
    ----------
    files : list of pathlib.Path
        Paths to inspect.
    max_pixels : int, default=128 * 128
        Maximum number of pixels for an image to be included.

    Returns
    -------
    list of pathlib.Path
        Paths to images whose width times height does not exceed
        ``max_pixels``.
    """
    tiny: list[pth.Path] = []

    for f in files:
        try:
            with Image.open(f) as im:
                if im.width * im.height <= max_pixels:
                    tiny.append(f)
        except Exception:
            pass

    return tiny
