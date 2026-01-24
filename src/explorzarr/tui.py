"""Interactive TUI for exploring ZARR stores using textual library."""

import logging
from pathlib import Path

import zarr
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import (
    Label,
    Static,
    Tree,
)
from textual.widgets.tree import TreeNode
from zarr import Array, Group

logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler()])

logger = logging.getLogger(__name__)


class ZarrTree(Tree):
    """Tree widget for navigating ZARR hierarchy."""

    def __init__(self, store_path: str | Path, **kwargs) -> None:  # noqa: ANN003
        """Set up ZarrTree.

        Args:
            store_path: ZARR store path.
            kwargs: Passed to `textual.widgets.Tree`.

        """
        super().__init__("ZARR Store", **kwargs)
        self.store_path = Path(store_path)
        self.root_label = str(self.store_path.name)
        self.load_store()

    def load_store(self) -> None:
        """Load the ZARR store and populate the tree."""
        try:
            # Open the ZARR store
            zarr_store = zarr.open(str(self.store_path), mode="r")
            self.clear()

            # Add root node
            root_node = self.root.add(self.root_label, data=zarr_store, expand=True)

            # Recursively add children
            self._populate_children(root_node, zarr_store)

        except Exception as e:  # noqa: BLE001
            self.clear()
            self.root.add(f"Error: {e!s}")

    def _populate_children(self, parent_node: TreeNode, zarr_obj: Group | Array) -> None:
        """Recursively add children to the tree."""
        try:
            if isinstance(zarr_obj, Group):
                # For groups, add all children
                for key in zarr_obj:
                    child_obj = zarr_obj[key]
                    node_label = key

                    # Determine if it's a group or array
                    if isinstance(child_obj, Group):
                        node = parent_node.add(
                            f"[blue]{node_label}[/]", data=child_obj, expand=True
                        )
                        self._populate_children(node, child_obj)
                    else:
                        node = parent_node.add(f"[green]{node_label}[/]", data=child_obj)
            # If it's an array, we don't add children
        except Exception as e:
            msg = f"Error loading children: {e}"
            logger.exception(msg)


class MetadataDisplay(Static):
    """Widget to display metadata for selected ZARR object."""

    def __init__(self, **kwargs) -> None:  # noqa: ANN003
        """Set up metadata display."""
        super().__init__("No selection", **kwargs)

    def update_metadata(self, zarr_obj: Group | Array) -> None:
        """Update the displayed metadata."""
        if zarr_obj is None:
            self.update("No selection")
            return

        try:
            # Get object type
            obj_type = "Array" if isinstance(zarr_obj, Array) else "Group"

            # Build metadata text
            metadata_lines = [
                f"[bold blue]Object Type:[/]: {obj_type}",
                f"[bold blue]Path:[/]: {getattr(zarr_obj, 'path', 'Unknown')}",
            ]

            if isinstance(zarr_obj, Array):
                metadata_lines.extend(
                    [
                        f"[bold blue]Shape:[/]: {zarr_obj.shape}",
                        f"[bold blue]Chunks:[/]: {zarr_obj.chunks}",
                        f"[bold blue]Data Type:[/]: {zarr_obj.dtype}",
                        f"[bold blue]Fill Value:[/]: {zarr_obj.fill_value}",
                        f"[bold blue]Compressor:[/]: {zarr_obj.compressor}",
                        f"[bold blue]Filters:[/]: {zarr_obj.filters}",
                    ]
                )
            else:
                metadata_lines.append(f"[bold blue]Number of Members:[/]: {len(zarr_obj)}")

            # Add attributes if they exist
            if hasattr(zarr_obj, "attrs") and zarr_obj.attrs:
                metadata_lines.append("\n[bold blue]Attributes:[/]")
                for key, value in zarr_obj.attrs.items():
                    metadata_lines.append(f"  {key}: {value}")

            self.update("\n".join(metadata_lines))

        except Exception as e:  # noqa: BLE001
            self.update(f"Error displaying metadata: {e!s}")


class ExplorZARRTui(App):
    """Main TUI application for exploring ZARR stores."""

    CSS_PATH = "tui.css"

    def __init__(self, store_path: str | Path, **kwargs) -> None:  # noqa: ANN003
        """Initialize the explorzarr tui.

        Args:
            store_path: Zarr store path.
            kwargs: Passed to `textual.app.App`.

        """
        super().__init__(**kwargs)
        self.store_path = Path(store_path)
        self.selected_object = None

    def compose(self) -> ComposeResult:
        """Compose the layout."""
        yield Label(f"ZARR Explorer - {self.store_path.name}", id="title")

        with Horizontal(id="main-content"):
            # Left panel - Tree explorer
            with Vertical(id="explorer-panel"):
                yield Label("Explorer", id="explorer-title")
                yield ZarrTree(self.store_path, id="zarr-tree")

            # Right panel - Metadata display
            with Vertical(id="metadata-panel"):
                yield Label("Metadata", id="metadata-title")
                yield MetadataDisplay(id="metadata-display")
        # Command bar at bottom
        yield Label(
            "[bold]Commands:[/] "
            "[green]↑/↓[/] Navigate | "
            "[green]Enter[/] Select | "
            "[green]Ctrl+q[/] Quit",
            id="command-bar",
        )

    def on_mount(self) -> None:
        """Called when the app is mounted."""  # noqa: D401
        self.title = f"ZARR Explorer - {self.store_path.name}"

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        """Handle selection of a tree node."""
        node = event.node
        if node.data is not None:
            self.selected_object = node.data
            # Find the metadata display widget and update it
            metadata_display = self.query_one("#metadata-display", MetadataDisplay)
            metadata_display.update_metadata(node.data)
