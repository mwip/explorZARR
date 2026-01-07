"""explorZARR is a command line tool to explore ZARR stores.

It provides three separate commands
- `dump`: dumps the contents of a specified array.
- `ls`: lists the contents of a ZARR store.
- `tui`: starts a interactive TUI session.
"""

import click

from explorzarr.dump import dump_fn
from explorzarr.ls import ls_fn


@click.group()
def cli() -> None:
    """CLI app entry point."""


@cli.command()
@click.argument("store", nargs=1)
@click.argument("array_path", nargs=1)
@click.option("-f", "--full_array", is_flag=True, help="Enable more text output.")
@click.option("-v", "--verbose", is_flag=True, help="Enable more text output.")
def dump(store: str, array_path: str, *, full_array: bool, verbose: bool) -> int:
    """Dump an array [with optional path]."""
    dump_fn(store=store, array_path=array_path, full_array=full_array, verbose=verbose)
    return 0


@cli.command()
@click.argument("store")
@click.argument("path", required=False)
@click.option("-l", "--level", type=int, help="Recursively list arrays in groups.")
@click.option("-i", "--no-info", is_flag=True, help="Dont print the ZARR store info.")
@click.option("-t", "--no-tree", is_flag=True, help="Dont print the ZARR store tree.")
@click.option("-v", "--verbose", is_flag=True, help="Enable more text output.")
def ls(  # noqa: PLR0913
    store: str, path: str | None, *, level: int | None, no_info: bool, no_tree: bool, verbose: bool
) -> int:
    """List contents of ZARR store and sketch array shapes."""
    ls_fn(store=store, path=path, level=level, no_info=no_info, no_tree=no_tree, verbose=verbose)
    return 0


@cli.command()
@click.argument("store")
@click.option("-v", "--verbose", is_flag=True, help="Enable more text output.")
def tui(store: str, *, verbose: bool) -> None:
    """Start the interactive TUI for a ZARR store."""
    raise NotImplementedError


if __name__ == "__main__":
    cli()
