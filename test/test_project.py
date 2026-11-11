from pathlib import Path

import trash_eater
from duplicates import find_duplicates
from empty_objects import empty_files, is_empty_directory
from junk_files import find_junk_files


def test_package_exports_public_helpers() -> None:
    assert callable(trash_eater.find_duplicates)
    assert callable(trash_eater.broken_images)
    assert callable(trash_eater.tiny_images)


def test_finds_duplicate_empty_and_small_files(tmp_path: Path) -> None:
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
    candidates = [
        tmp_path / "cache.PYC",
        tmp_path / "paper.synctex.gz",
        tmp_path / ".Rhistory",
        tmp_path / "notes.txt",
    ]

    assert find_junk_files(candidates) == candidates[:3]
