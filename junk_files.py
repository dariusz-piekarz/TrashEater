import pathlib as pth
from utils import filter_files

JUNK_EXTENSIONS = frozenset({
    # general temporary / backup
    ".tmp",
    ".temp",
    ".bak",
    ".old",
    ".orig",
    ".rej",
    ".swp",
    ".swo",
    ".swn",

    # logs
    ".log",
    ".dmp",
    ".stackdump",

    # Python
    ".pyc",
    ".pyo",

    # C/C++
    ".o",
    ".obj",
    ".a",
    ".lib",
    ".exp",
    ".ilk",
    ".pch",
    ".idb",
    ".pdb",

    # executable outputs
    ".exe",
    ".dll",
    ".so",
    ".dylib",

    # LaTeX
    ".aux",
    ".bbl",
    ".bcf",
    ".blg",
    ".fdb_latexmk",
    ".fls",
    ".lof",
    ".log",
    ".lot",
    ".nav",
    ".out",
    ".run.xml",
    ".snm",
    ".synctex.gz",
    ".toc",
    ".xdv",

    # R
    ".rhistory",
    ".rdata",
    ".rproj.user",

    # Julia
    ".ji",

    # VBA / Office
    ".wbk",
})


def find_junk_files(files: list[pth.Path]) -> list[pth.Path]:
    """Select paths with known temporary or generated-file extensions.

    Parameters
    ----------
    files : list of pathlib.Path
        Paths to inspect.

    Returns
    -------
    list of pathlib.Path
        Matching paths in their original order.
    """
    return filter_files(files, JUNK_EXTENSIONS)
