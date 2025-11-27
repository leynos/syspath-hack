# syspath-hack

syspath-hack provides small helpers for keeping `sys.path` predictable in
scripts, notebooks, and tests. It resolves entries before adding them, avoids
duplicates, and can locate your project root with a marker file such as
`pyproject.toml`.

## Installation

Install from PyPI with your preferred tool:

- `pip install syspath-hack`
- `uv add syspath-hack`

## Quick start

Add the project root to `sys.path` so local imports work during ad-hoc scripts
or notebooks:

```python
from syspath_hack import add_project_root

add_project_root()  # finds the nearest pyproject.toml above the cwd
```

## Working with temporary paths

When you need to add a directory for a short time, pair `add_to_syspath` with
`remove_from_syspath` to leave `sys.path` tidy:

```python
from pathlib import Path

from syspath_hack import add_to_syspath, remove_from_syspath

plugins_dir = Path(__file__).parent / "plugins"
add_to_syspath(plugins_dir)

try:
    import plugin_loader  # noqa: F401
finally:
    remove_from_syspath(plugins_dir)
```

## Custom project markers

You can search for a different marker file and handle failures explicitly:

```python
from syspath_hack import ProjectRootNotFoundError, find_project_root

try:
    repo_root = find_project_root("poetry.lock")
except ProjectRootNotFoundError as err:
    raise SystemExit(f"Could not locate the repository: {err}") from err
else:
    print(repo_root)
```
