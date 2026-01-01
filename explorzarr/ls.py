"""ls.py is concerned with listing contents of a ZARR store."""

import zarr
import zarr.storage


def ls_fn(store: str, path: str | None, level: int | None = None, *, verbose: bool = False) -> None:  # noqa: ARG001, unused ignoring `verbose` for now, will be relevant for remote stores
    """List contents of ZARR store."""
    root = zarr.group(store, path=path)
    print(root.tree(level=level))  # noqa: T201
