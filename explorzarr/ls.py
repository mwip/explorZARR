"""ls.py is concerned with listing contents of a ZARR store."""

import zarr
import zarr.storage


def ls_fn(  # noqa: PLR0913
    store: str,
    path: str | None,
    level: int | None = None,
    *,
    no_info: bool = False,
    no_tree: bool = False,
    verbose: bool = False,  # noqa: ARG001, unused ignoring `verbose` for now, will be relevant for remote stores
) -> None:
    """List contents of ZARR store."""
    root = zarr.open_group(store, path=path, mode="r")
    if not no_info:
        print(root.info_complete(), "\n")  # noqa: T201

    if not no_tree:
        print(root.tree(level=level), "\n")  # noqa: T201
