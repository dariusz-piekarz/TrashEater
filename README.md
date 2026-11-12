# Trash Eater

Trash Eater provides read-only Python utilities for finding duplicate,
empty, junk, and old files, as well as identifying image problems.

## Requirements and installation

Trash Eater requires Python 3.10 or newer. Install the package with:

```console
python -m pip install .
```

Image utilities use Pillow and ImageHash. Similar-name matching uses RapidFuzz.

## Quick start

```python
from pathlib import Path

from trash_eater import empty_files, find_duplicates

root = Path("photos")
files = [path for path in root.rglob("*") if path.is_file()]

duplicates = find_duplicates(files)
empty = empty_files(root)

for group in duplicates.values():
    print("Duplicate files:", *(str(path) for path in group))
for path in empty:
    print("Empty file:", path)
```

`find_duplicates` maps full SHA-256 digests to groups of files with identical
contents. `empty_files` searches recursively. These functions only report
matches; they do not delete or modify files.

## Image utilities

The package exports `broken_images`, `image_duplicates`, `similar_images`, and
`tiny_images`:

```python
from pathlib import Path

from trash_eater import broken_images, image_duplicates, similar_images

images = list(Path("photos").rglob("*.jpg"))
broken = broken_images(images)
readable = [path for path in images if path not in broken]

duplicates = image_duplicates(readable)
similar = similar_images(readable, similarity_lvl=6)
```

`image_duplicates` groups identical perceptual hashes. `similar_images`
returns candidate pairs that share a hash bucket and are within the requested
perceptual-hash distance. `broken_images`, `image_duplicates`, and
`similar_images` recognize JPEG, PNG, BMP, and WebP files. `tiny_images` can
inspect any image format supported by Pillow.

## Other helpers

The following helpers are available from their respective top-level modules:

```python
from datetime import timedelta
from pathlib import Path

from junk_files import find_junk_files
from old_files import old_files
from similar_names import similar_names

files = [path for path in Path("photos").rglob("*") if path.is_file()]
junk = find_junk_files(files)
old = old_files(files, age=timedelta(days=365))
similar = similar_names(files)
```

- `find_junk_files(files)` finds common temporary and generated-file suffixes.
- `old_files(files, age=...)` selects files older than the given age.
- `similar_names(files, threshold=85)` compares file-name stems.

## Example

Run the command-line example from the repository root:

```console
python -m pip install -e .
python -m example.example photos
```

The example reports findings without deleting or modifying files.

## Tests

Install the optional test dependency and run the test suite:

```console
python -m pip install -e ".[test]"
python -m pytest
```
