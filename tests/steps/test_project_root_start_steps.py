"""Behavioural coverage for explicit project-root start directories."""

from __future__ import annotations

import dataclasses as dc
import sys
import typing as typ

import pytest
from pytest_bdd import given, scenario, then, when

from syspath_hack import add_project_root, find_project_root

if typ.TYPE_CHECKING:
    from pathlib import Path


@dc.dataclass
class RootState:
    """Shared values mutated by step functions."""

    project_root: Path | None = None
    start_dir: Path | None = None
    found_root: Path | None = None


@pytest.fixture
def root_state() -> RootState:
    """Shared state for the scenarios."""
    return RootState()


@scenario(
    "project_root_start.feature",
    "Finding a project root from an explicit start directory",
)
def test_find_project_root_with_explicit_start() -> None:
    """Verify find_project_root uses the provided start directory."""


@pytest.mark.usefixtures("isolated_syspath")
@scenario(
    "project_root_start.feature",
    "Adding a project root from an explicit start directory",
)
def test_add_project_root_with_explicit_start() -> None:
    """Verify add_project_root uses the provided start directory."""


@given('a project root with marker "pyproject.toml"')
def a_project_root_with_marker(tmp_path: Path, root_state: RootState) -> None:
    """Create a project root that contains the marker file."""
    project_root = tmp_path / "workspace"
    project_root.mkdir()
    (project_root / "pyproject.toml").write_text("[project]\nname = 'demo'\n")
    root_state.project_root = project_root


@given("a nested start directory beneath the project root")
def a_nested_start_directory(root_state: RootState) -> None:
    """Create a nested directory to use as the explicit start path."""
    assert root_state.project_root is not None
    start_dir = root_state.project_root / "src" / "pkg"
    start_dir.mkdir(parents=True)
    root_state.start_dir = start_dir


@given("I am in a different working directory")
def i_am_in_a_different_working_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Move the working directory away from the project root."""
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    monkeypatch.chdir(elsewhere)


@given("sys.path is empty")
def sys_path_is_empty() -> None:
    """Ensure sys.path starts empty for this scenario."""
    sys.path[:] = []


@when("I search for the project root from the explicit start directory")
def i_search_for_the_project_root(root_state: RootState) -> None:
    """Invoke find_project_root with an explicit start directory."""
    assert root_state.start_dir is not None
    root_state.found_root = find_project_root(start=root_state.start_dir)


@when("I add the project root from the explicit start directory")
def i_add_the_project_root(root_state: RootState) -> None:
    """Invoke add_project_root with an explicit start directory."""
    assert root_state.start_dir is not None
    add_project_root(start=root_state.start_dir)


@then("the located project root is the one containing the marker")
def the_located_project_root_is_correct(root_state: RootState) -> None:
    """Assert the resolved project root is correct."""
    assert root_state.project_root is not None
    assert root_state.found_root == root_state.project_root.resolve()


@then("sys.path begins with the project root")
def sys_path_begins_with_project_root(root_state: RootState) -> None:
    """Assert sys.path starts with the resolved project root."""
    assert root_state.project_root is not None
    assert sys.path[0] == str(root_state.project_root.resolve())
