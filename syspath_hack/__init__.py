"""syspath-hack package."""

from __future__ import annotations

from .pure import (
    ProjectRootNotFoundError,
    add_project_root,
    add_to_syspath,
    find_project_root,
    prepend_to_syspath,
    remove_from_syspath,
)

PACKAGE_NAME = "syspath_hack"

__all__ = [
    "ProjectRootNotFoundError",
    "add_project_root",
    "add_to_syspath",
    "find_project_root",
    "prepend_to_syspath",
    "remove_from_syspath",
]
