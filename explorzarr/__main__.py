"""explorZARR is a command line tool to explore ZARR stores.

It provides three separate commands
- `dump`: dumps the contents of a specified array.
- `ls`: lists the contents of a ZARR store.
- `tui`: starts a interactive TUI session.
"""

import click

from explorzarr.ls import ls_fn


@click.group()
def cli() -> None:
    """CLI app entry point."""


@cli.command()
@click.argument("store", nargs=1)
@click.argument("path", required=False)
@click.option("-v", "--verbose", is_flag=True, help="Enable more text output.")
def dump(store: str, path: str | None, *, verbose: bool) -> None:
    """Dump an array [with optional path]."""
    raise NotImplementedError


@cli.command()
@click.argument("store")
@click.argument("path", required=False)
@click.option("-l", "--level", type=int, help="Recursively list arrays in groups.")
@click.option("-v", "--verbose", is_flag=True, help="Enable more text output.")
def ls(store: str, path: str | None, *, level: int | None, verbose: bool) -> None:
    """List contents of ZARR store and sketch array shapes."""
    return ls_fn(store=store, path=path, level=level, verbose=verbose)


@cli.command()
@click.argument("store")
@click.option("-v", "--verbose", is_flag=True, help="Enable more text output.")
def tui(store: str, *, verbose: bool) -> None:
    """Start the interactive TUI for a ZARR store."""
    raise NotImplementedError


if __name__ == "__main__":
    cli()
