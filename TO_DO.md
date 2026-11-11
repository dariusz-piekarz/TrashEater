# To do

- Move implementation modules under `trash_eater/` and use package-relative imports; the initial packaging currently preserves the existing top-level module imports.
- Add automated tests for duplicate detection across larger files and changing file contents.
- Add tests for unreadable images, image duplicates, and similar-image threshold behavior.
- Implement or remove the currently empty modules: `filetree_stats.py`, `old_files.py`, and `similar_names.py`.
- Define and document behavior for inaccessible paths, symlinks, and files that change while scanning.
- Add type checking and lint configuration, then document supported Python versions and public APIs.
- Review whether partial hashing and image similarity bucketing can miss candidates; compare results against a simple exhaustive implementation.
