"""ls.py is concerned with listing contents of a ZARR store."""

import os

import psutil
import zarr
from zarr.errors import ArrayNotFoundError, ContainsArrayError, GroupNotFoundError


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
    try:
        root = zarr.open_group(store, path=path, mode="r")
    except (GroupNotFoundError, ContainsArrayError):
        if path is not None:
            try:
                root = zarr.open_array(store, path=path, mode="r")
            except ArrayNotFoundError:
                print(  # noqa: T201
                    f"No object found in store {store} at path {path}."
                    "\n--> Hint: Omit path to get more details about the groups and arrays in the"
                    " ZARR store."
                )
                proc = psutil.Process(os.getpid())
                cmdline = proc.cmdline()[:-1]
                print("-->", *cmdline)  # noqa: T201
                return
    if not no_info:
        info_lines = str(root.info_complete()).splitlines()
        for line in [*info_lines, "\n"]:
            print(line.rstrip())  # noqa: T201

    if not no_tree and isinstance(root, zarr.Group):
        tree_lines = str(root.tree(level=level)).splitlines()
        for line in [*tree_lines, "\n"]:
            print(line.rstrip())  # noqa: T201


def list_all_arrays(store: str) -> list[str]:
    """List all arrays in a ZARR store.

    Args:
        store: ZARR store to list arrays from.

    Returns:
        List of all arrays in the store.

    """
    root = zarr.open_group(store, path=None, mode="r")
    return list_arrays_recursively(root)


def list_arrays_recursively(group: zarr.Group, path: str | None = None) -> list[str]:
    """Recursively list all arrays in a Zarr group, including those in nested subgroups.

    Args:
        group: A Zarr group (or store root) to search for arrays.
        path: The current path in the hierarchy, used for building full array paths.
              Defaults to an empty string for the root group.

    Returns:
        A list of strings, where each string is the full path to an array in the group hierarchy.

    Example:
        >>> store = zarr.open("example.zarr", mode="r")
        >>> arrays = list_arrays_recursively(store)
        >>> print(arrays)
        ['array1', 'group1/array2', 'group1/subgroup/array3']

    """
    arrays: list[str] = []
    for name, item in group.members():
        current_path: str = f"{path}/{name}" if path else name
        if isinstance(item, zarr.Array):
            arrays.append(current_path)
        elif isinstance(item, zarr.Group):
            arrays.extend(list_arrays_recursively(item, current_path))
    return arrays
