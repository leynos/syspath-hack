"""syspath-hack package."""

from __future__ import annotations

from .pure import (
    ProjectRootNotFoundError,
    add_project_root,
    add_to_syspath,
    find_project_root,
    remove_from_syspath,
)
from .pure import (
    hello as _pure_hello,
)

PACKAGE_NAME = "syspath_hack"

try:  # pragma: no cover - Rust optional
    rust = __import__(f"_{PACKAGE_NAME}_rs")
    hello = rust.hello  # type: ignore[attr-defined]
except ModuleNotFoundError:  # pragma: no cover - Python fallback
    hello = _pure_hello

__all__ = [
    "ProjectRootNotFoundError",
    "add_project_root",
    "add_to_syspath",
    "find_project_root",
    "hello",
    "remove_from_syspath",
]
