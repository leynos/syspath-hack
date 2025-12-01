"""Shared test fixtures."""

from __future__ import annotations

import sys
import typing as typ

import pytest


@pytest.fixture
def isolated_syspath() -> typ.Iterator[None]:
    """Preserve sys.path for tests that mutate it."""
    original = list(sys.path)
    try:
        yield
    finally:
        sys.path[:] = original
