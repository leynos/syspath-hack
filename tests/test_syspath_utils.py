"""Tests for the public helpers that manipulate sys.path."""

from __future__ import annotations

import sys
import typing as typ
from unittest import mock

import pytest

from syspath_hack import (
    ProjectRootNotFoundError,
    add_project_root,
    add_to_syspath,
    find_project_root,
    remove_from_syspath,
)

if typ.TYPE_CHECKING:
    from pathlib import Path


def test_add_to_syspath_appends_resolved_path(tmp_path: Path) -> None:
    """It appends the resolved path and avoids duplicates."""
    target = tmp_path / "package"
    target.mkdir()
    starting_entries = ["/already-present"]

    with mock.patch.object(sys, "path", starting_entries.copy()):
        add_to_syspath(target)

        resolved = str(target.resolve())
        assert sys.path[-1] == resolved

        add_to_syspath(target)
        assert sys.path.count(resolved) == 1


def test_remove_from_syspath_removes_all_matches(tmp_path: Path) -> None:
    """It removes every occurrence of the resolved path."""
    target = tmp_path / "package"
    target.mkdir()
    resolved = str(target.resolve())
    other = str((tmp_path / "other").resolve())

    with mock.patch.object(sys, "path", [other, resolved, resolved]):
        remove_from_syspath(target)
        assert sys.path == [other]


def test_find_project_root_returns_first_match(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """It returns the first ancestor containing the marker file."""
    project_root = tmp_path / "project"
    project_root.mkdir()
    (project_root / "pyproject.toml").write_text("[project]\nname = 'demo'\n")

    nested = project_root / "src" / "demo"
    nested.mkdir(parents=True)
    monkeypatch.chdir(nested)

    result = find_project_root()

    assert result == project_root.resolve()


def test_find_project_root_raises_when_reaching_home(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """It raises once the search reaches the home directory boundary."""
    fake_home = tmp_path / "home"
    nested = fake_home / "workspace" / "repo"
    nested.mkdir(parents=True)
    monkeypatch.chdir(nested)

    with (
        mock.patch("pathlib.Path.home", return_value=fake_home),
        pytest.raises(ProjectRootNotFoundError),
    ):
        find_project_root("nonexistent.sigil")


def test_add_project_root_adds_directory_to_sys_path(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """It adds the located project root to sys.path."""
    project_root = tmp_path / "workspace"
    project_root.mkdir()
    (project_root / "pyproject.toml").write_text("[project]\nname = 'demo'\n")

    nested = project_root / "src"
    nested.mkdir()
    monkeypatch.chdir(nested)

    with mock.patch.object(sys, "path", []):
        add_project_root()

        resolved = str(project_root.resolve())
        assert sys.path == [resolved]
