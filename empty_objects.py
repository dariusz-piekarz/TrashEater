import pathlib as pth


def is_empty_directory(folder: pth.Path) ->  bool:
    if not folder.is_dir():
        raise NotADirectoryError(f"A path: {folder} is not a valid path!")
    
    if len(list(folder.glob("*"))) == 0:
        return True
    return False


def is_fileless_tree(folder: pth.Path) -> bool:
    if not folder.is_dir():
        raise NotADirectoryError(f"A path: {folder} is not a valid path!")
    return not any(folder.iterdir())


def empty_files(folder: pth.Path) -> list[pth.Path]:
    files = list(folder.rglob("*"))

    empty: list[pth.Path] = []
    for f in files:
        if f.is_file() and f.stat().st_size == 0:
            empty.append(f)
    return empty
