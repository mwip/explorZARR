# explorZARR

`explorzarr` is a tool to conveniently explore ZARR stores from the command line. It takes inspiration from tools like `h5ls` and `h5dump` ([among others](https://support.hdfgroup.org/documentation/hdf5/latest/_command_tools.html)) that are extremely useful to inspect HDF5 files and brings similar functionality to ZARR stores.

At the moment, `explorzarr` is a prototype in its early stages. The goal is to add the following functionality:

- `explorzarr ls`: lists the groups and arrays alongside some metadata of a ZARR store
- `explorzarr dump`: opens an array and dumps its contents to the terminal
- `explorzarr tui`: starts TUI session to interactively explore the contents of the ZARR store.

The goal is to support both local as well as remote ZARR stores, e.g. on S3.

## Running tests

```shell
uv sync --all-groups
uv pip install -e .
uv run pytest
```

To evalate test coverage, run

```shell
uv run coverage run -m pytest
```
