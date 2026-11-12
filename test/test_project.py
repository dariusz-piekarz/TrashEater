import datetime
import os
from pathlib import Path

import trash_eater
from PIL import Image

from duplicates import find_duplicates
from empty_objects import empty_files, is_empty_directory
from images import broken_images, image_duplicates, similar_images, tiny_images
from junk_files import find_junk_files
from old_files import old_files
from similar_names import similar_names


def test_package_exports_public_helpers() -> None:
    """Verify that the package exposes its documented helpers."""
    assert callable(trash_eater.find_duplicates)
    assert callable(trash_eater.broken_images)
    assert callable(trash_eater.tiny_images)


def test_finds_duplicate_empty_and_small_files(tmp_path: Path) -> None:
    """Detect duplicate-content groups and recursively find empty files."""
    first = tmp_path / "first.txt"
    second = tmp_path / "second.txt"
    empty_first = tmp_path / "empty-first.txt"
    empty_second = tmp_path / "empty-second.txt"
    first.write_text("same content", encoding="utf-8")
    second.write_text("same content", encoding="utf-8")
    empty_first.touch()
    empty_second.touch()

    groups = find_duplicates([first, second, empty_first, empty_second])

    assert {
        frozenset(paths) for paths in groups.values()
    } == {
        frozenset((first, second)),
        frozenset((empty_first, empty_second)),
    }


def test_finds_empty_files_recursively(tmp_path: Path) -> None:
    """Find nested empty files and recognize an empty directory."""
    empty_dir = tmp_path / "empty-dir"
    empty_dir.mkdir()
    nested = tmp_path / "nested"
    nested.mkdir()
    empty_file = nested / "empty.txt"
    empty_file.touch()
    (nested / "non-empty.txt").write_text("data", encoding="utf-8")

    assert empty_files(tmp_path) == [empty_file]
    assert is_empty_directory(empty_dir)


def test_finds_junk_files_with_case_and_compound_extensions(
    tmp_path: Path,
) -> None:
    """Match junk suffixes case-insensitively, including compound suffixes."""
    candidates = [
        tmp_path / "cache.PYC",
        tmp_path / "paper.synctex.gz",
        tmp_path / ".Rhistory",
        tmp_path / "notes.txt",
    ]

    assert find_junk_files(candidates) == candidates[:3]


def test_finds_only_files_with_matching_content_after_contents_change(
    tmp_path: Path,
) -> None:
    """Recompute duplicate groups after one file's contents change."""
    first = tmp_path / "first.txt"
    second = tmp_path / "second.txt"
    first.write_text("matching content", encoding="utf-8")
    second.write_text("matching content", encoding="utf-8")

    assert len(find_duplicates([first, second])) == 1

    second.write_text("different content", encoding="utf-8")

    assert find_duplicates([first, second]) == {}


def test_finds_broken_images_and_ignores_non_image_files(
    tmp_path: Path,
) -> None:
    """Report a corrupt image but ignore paths with unsupported extensions."""
    broken = tmp_path / "broken.png"
    non_image = tmp_path / "notes.txt"
    broken.write_bytes(b"not an image")
    non_image.write_bytes(b"not an image")

    assert broken_images([broken, non_image]) == [broken]


def test_finds_duplicate_and_similar_images(tmp_path: Path) -> None:
    """Find duplicate, similar, and small images."""
    first = tmp_path / "first.png"
    second = tmp_path / "second.png"
    image = Image.new("RGB", (16, 16), "white")
    image.save(first)
    image.save(second)

    assert list(image_duplicates([first, second]).values()) == [[first, second]]
    assert similar_images([first, second], similarity_lvl=0) == [(first, second)]
    assert tiny_images([first, second], max_pixels=256) == [first, second]


def test_finds_names_above_threshold_only(tmp_path: Path) -> None:
    """Apply the configured similarity threshold to filename stems."""
    first = tmp_path / "photo.png"
    second = tmp_path / "photo1.png"

    assert similar_names([first, second]) == [(first, second)]
    assert similar_names([first, second], threshold=100) == []


def test_finds_files_older_than_requested_age(tmp_path: Path) -> None:
    """Select files older than the supplied age, excluding recent files."""
    stale = tmp_path / "stale.txt"
    recent = tmp_path / "recent.txt"
    stale.touch()
    recent.touch()
    now = datetime.datetime.now().timestamp()
    os.utime(stale, (now - 10 * 86400, now - 10 * 86400))
    os.utime(recent, (now - 86400, now - 86400))

    assert old_files([stale, recent], age=datetime.timedelta(days=5)) == [stale]
