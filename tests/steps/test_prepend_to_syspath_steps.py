"""Behavioural coverage for preserving the blank sys.path sentinel."""

from __future__ import annotations

import dataclasses as dc
import sys
from pathlib import Path

import pytest
from pytest_bdd import given, scenario, then, when

from syspath_hack import prepend_to_syspath


@dc.dataclass
class PathState:
    """Shared values mutated by step functions."""

    cwd: Path | None = None
    starting: list[str] | None = None


@pytest.fixture
def path_state() -> PathState:
    """Shared state for the scenario."""
    return PathState()


@pytest.mark.usefixtures("isolated_syspath")
@scenario(
    "prepend_to_syspath.feature",
    "Prepending current working directory retains leading blank entry",
)
def test_prepend_preserves_blank() -> None:
    """Verify prepend_to_syspath keeps the blank sentinel intact."""


@given("I am in a temporary working directory")
def i_am_in_a_temporary_working_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> Path:
    """Work inside an isolated temporary directory."""
    monkeypatch.chdir(tmp_path)
    return tmp_path


@given('sys.path starts with a blank entry and "other"')
def sys_path_starts_with_blank(path_state: PathState) -> None:
    """Prime sys.path with the interpreter's CWD sentinel."""
    starting_entries = ["", "other"]
    path_state.starting = starting_entries
    sys.path[:] = starting_entries.copy()


@when("I prepend the current working directory to sys.path")
def i_prepend_current_working_directory(path_state: PathState) -> None:
    """Invoke prepend_to_syspath with the active working directory."""
    cwd = Path.cwd()
    path_state.cwd = cwd
    prepend_to_syspath(cwd)


@then(
    "sys.path lists the current working directory first and preserves the blank entry"
)
def sys_path_lists_target_then_blank(path_state: PathState) -> None:
    """Assert the target path is first and the blank entry remains."""
    assert path_state.cwd is not None
    assert path_state.starting is not None

    cwd = str(path_state.cwd)
    starting = path_state.starting

    assert sys.path[0] == cwd
    assert sys.path[1] == ""
    assert sys.path[2:] == starting[1:]
