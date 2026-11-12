"""Find files older than a specified age."""

import pathlib as pth
import datetime

YEARS = 3 * 365 + 1


def old_files(
    files: list[pth.Path],
    age: datetime.timedelta = datetime.timedelta(days=YEARS),
) -> list[pth.Path]:
    """Select files whose modification time is older than a given age.

    Parameters
    ----------
    files : list of pathlib.Path
        Files to inspect.
    age : datetime.timedelta, default=3 years
        Minimum age relative to the current local time.

    Returns
    -------
    list of pathlib.Path
        Paths with modification times before the age cutoff.
    """
    cutoff = datetime.datetime.now() - age

    return [
        f for f in files if datetime.datetime.fromtimestamp(f.stat().st_mtime) < cutoff
    ]
