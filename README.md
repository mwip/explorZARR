# explorZARR

`explorzarr` is a tool to conveniently explore ZARR stores from the command line. It takes inspiration from tools like `h5ls` and `h5dump` ([among others](https://support.hdfgroup.org/documentation/hdf5/latest/_command_tools.html)) that are extremely useful to inspect HDF5 files and brings similar functionality to ZARR stores.

At the moment, `explorzarr` is a prototype in its early stages. The goal is to add the following functionality:

- `explorzarr ls`: lists the groups and arrays alongside some metadata of a ZARR store
- `explorzarr dump`: opens an array and dumps its contents to the terminal
- `explorzarr tui`: starts TUI session to interactively explore the contents of the ZARR store.

The goal is to support both local as well as remote ZARR stores, e.g. on S3.

## `explorzarr ls`

The `explorzarr ls` utility is meant to (recursively) list metadata of groups or arrays in the ZARR store. If a group is provided, a the complete info object is printed alongside a visual tree representation of all sub groups and arrays inside the group. For example here the "root" group (the default when no group is provided).

```shell
uv run -m explorzarr data/store.zarr
```
```
Name        :
Type        : Group
Zarr format : 3
Read-only   : True
Store type  : LocalStore
No. members : 2
No. arrays  : 1
No. groups  : 1

/
└── grp
    └── ar1 (123, 42, 42) float64
```

If an array path is specified, the array's information is printed:

```shell
uv run -m explorzarr data/store.zarr grp/ar1
```
```
Type               : Array
Zarr format        : 3
Data type          : Float64(endianness='little')
Fill value         : 0.0
Shape              : (123, 42, 42)
Chunk shape        : (62, 21, 42)
Order              : C
Read-only          : True
Store type         : LocalStore
Filters            : ()
Serializer         : BytesCodec(endian=<Endian.little: 'little'>)
Compressors        : (ZstdCodec(level=0, checksum=False),)
No. bytes          : 1735776 (1.7M)
No. bytes stored   : 926
Storage ratio      : 1874.5
Chunks Initialized : 4
```

## `explorzarr dump`

The `explorzarr dump` utility allows to print the an excerpt of an array to the terminal. Or with the `-f` / `--full_array` the full array can be dumped to stdout.

```shell
uv run -m explorzarr data/store.zarr grp/arr
```
```
[[[ 1 39 26 29  6]
  [30 15 78 53 34]
  [46 70 22 73 20]
  [42 23 91 79 50]
  [65 62 89 49 66]]
 [[56 82 71 22  9]
  [43  3 11 54 41]
  [62 97 53 61 36]
  [51 54 71 42 21]
  [12 17 32 46 97]]]
```

# Install

To install `explorzarr`, you can use `uv tool install`. See [here](https://docs.astral.sh/uv/getting-started/installation/) if you don't have `uv` installed yet.

```shell
uv tool install git+https://github.com/mwip/explorzarr
```


# Contributing

## Install `pre-commit`

Please use `pre-commit` to check for common rules when contributing.

```
uv tool install pre-commit
pre-commit install
```

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
