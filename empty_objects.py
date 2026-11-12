"""Find empty files and directories."""

import pathlib as pth


def is_empty_directory(folder: pth.Path) -> bool:
    """Check whether a directory has no direct entries.

    Parameters
    ----------
    folder : pathlib.Path
        Directory to inspect.

    Returns
    -------
    bool
        ``True`` if the directory is empty, otherwise ``False``.

    Raises
    ------
    NotADirectoryError
        If ``folder`` is not a directory.
    """
    if not folder.is_dir():
        raise NotADirectoryError(f"A path: {folder} is not a valid path!")

    if len(list(folder.glob("*"))) == 0:
        return True
    return False


def is_fileless_tree(folder: pth.Path) -> bool:
    """Check whether a directory has no direct entries.

    Parameters
    ----------
    folder : pathlib.Path
        Directory to inspect.

    Returns
    -------
    bool
        ``True`` if the directory has no direct entries, otherwise ``False``.

    Raises
    ------
    NotADirectoryError
        If ``folder`` is not a directory.
    """
    if not folder.is_dir():
        raise NotADirectoryError(f"A path: {folder} is not a valid path!")
    return not any(folder.iterdir())


def empty_files(folder: pth.Path) -> list[pth.Path]:
    """Find zero-byte files beneath a directory recursively.

    Parameters
    ----------
    folder : pathlib.Path
        Root directory to search.

    Returns
    -------
    list of pathlib.Path
        Zero-byte files found beneath ``folder``.
    """
    files = list(folder.rglob("*"))

    empty: list[pth.Path] = []
    for f in files:
        if f.is_file() and f.stat().st_size == 0:
            empty.append(f)
    return empty
