"""Pure Python helpers for managing sys.path state."""

from __future__ import annotations

import sys
import typing as typ
from pathlib import Path

Pathish = Path | str


class ProjectRootNotFoundError(RuntimeError):
    """Raised when a project root marker cannot be located safely."""


def _to_resolved_path(pth: Pathish) -> Path:
    """Return an absolute, normalised Path for comparisons."""
    path = Path(pth).expanduser()
    return path.resolve(strict=False)


def _resolve_sys_path_entry(entry: object) -> Path | None:
    """Resolve a sys.path entry when it resembles a filesystem location."""
    if not isinstance(entry, str):
        return None

    candidate = Path.cwd() if entry == "" else Path(entry)

    try:
        return candidate.expanduser().resolve(strict=False)
    except (OSError, RuntimeError, ValueError):
        return None


def _iter_resolved_sys_path() -> typ.Iterator[tuple[int, Path]]:
    """Provide index and resolved path pairs for usable sys.path entries."""
    for index, entry in enumerate(sys.path):
        resolved = _resolve_sys_path_entry(entry)
        if resolved is None:
            continue
        yield index, resolved


def add_to_syspath(pth: Pathish) -> None:
    """Append the resolved path to sys.path when it is not yet present."""
    target = _to_resolved_path(pth)

    for _, existing in _iter_resolved_sys_path():
        if existing == target:
            return

    sys.path.append(str(target))


def prepend_to_syspath(pth: Pathish) -> None:
    """Place the resolved path at the front of sys.path exactly once."""
    target = _to_resolved_path(pth)

    indexes_to_remove = [
        index for index, entry in _iter_resolved_sys_path() if entry == target
    ]

    for index in reversed(indexes_to_remove):
        del sys.path[index]

    sys.path.insert(0, str(target))


def remove_from_syspath(pth: Pathish) -> None:
    """Remove all occurrences of the resolved path from sys.path."""
    target = _to_resolved_path(pth)
    indexes_to_remove = [
        index for index, entry in _iter_resolved_sys_path() if entry == target
    ]

    for index in reversed(indexes_to_remove):
        del sys.path[index]


def find_project_root(sigil: str = "pyproject.toml") -> Path:
    """Find the nearest ancestor containing the marker file.

    The search stops before returning the user's home directory or any higher
    directory. A dedicated runtime error communicates when no marker is found.
    """
    if not sigil:
        msg = "sigil must be a non-empty string"
        raise ValueError(msg)

    current = Path.cwd().resolve()
    home = Path.home().resolve()

    while True:
        if current == home:
            break

        candidate = current / sigil
        if candidate.is_file():
            return current

        parent = current.parent
        if parent == current:
            break

        current = parent

    msg = (
        f"Unable to locate {sigil!r} when ascending from {Path.cwd()} "
        f"before reaching the home directory {home}"
    )
    raise ProjectRootNotFoundError(msg)


def add_project_root(sigil: str = "pyproject.toml") -> None:
    """Locate the project root and place it on sys.path."""
    project_root = find_project_root(sigil)
    add_to_syspath(project_root)
