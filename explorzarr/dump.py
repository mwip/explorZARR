"""dump.py is concerned with printing (dumping) contents of a ZARR store to the terminal."""

import sys
from pprint import pprint

import numpy as np
import zarr
from zarr.errors import ArrayNotFoundError

from explorzarr.ls import list_all_arrays


def dump_fn(
    store: str,
    array_path: str,
    *,
    full_array: bool = False,
    verbose: bool = False,  # noqa: ARG001, unused ignoring `verbose` for now, will be relevant for remote stores
) -> None:
    """TODO document function."""
    try:
        arr = zarr.open_array(store, path=array_path, mode="r")
        if full_array:
            with np.printoptions(threshold=sys.maxsize):
                print(arr[:])  # noqa: T201

        else:
            print(arr[:])  # noqa: T201

    except ArrayNotFoundError:
        pprint(list_all_arrays(store))  # noqa: T203
        msg = (
            f'\nCannot find array_path "{array_path}", use any of the arrays found in the'
            " ZARR store listed above"
        )
        print(msg)  # noqa: T201
        return
