import pathlib as pth

from PIL import Image, UnidentifiedImageError
from utils import filter_files
from image_duplicates import IMAGE_EXTESIONS


def broken_images(files: list[pth.Path]) -> list[pth.Path]:
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
    tiny: list[pth.Path] = []

    for f in files:
        try:
            with Image.open(f) as im:
                if im.width * im.height <= max_pixels:
                    tiny.append(f)
        except Exception:
            pass

    return tiny