# Trash Eater

Small Python utilities for inspecting files and finding duplicate or invalid images.

## Install

```console
python -m pip install .
```

The distribution requires Python 3.10 or newer. Image helpers use Pillow and ImageHash.

## Example

Install the package, then run the example from the repository root against a folder:

```console
python -m pip install -e .
python -m example.example photos
```

The example reports findings without deleting or modifying files.

## Quick start

```python
from pathlib import Path

from trash_eater import find_duplicates, empty_files

files = [path for path in Path("photos").rglob("*") if path.is_file()]
duplicates = find_duplicates(files)
empty = empty_files(Path("photos"))
```

`find_duplicates` returns a mapping from SHA-256 hashes to groups of matching paths. The library only reports files; it does not delete or modify them.
