import tempfile
from collections.abc import Generator
from pathlib import Path

import numpy as np
import pytest
import zarr


@pytest.fixture
def fixture_zarr_small() -> Generator[Path]:
    with tempfile.TemporaryDirectory(suffix=".zarr") as f:
        f_path = Path(f)
        root = zarr.open_group(store=f_path, mode="w")

        grp = root.create_group(name="grp")

        grp.create_array(name="ar1", data=np.ones((123, 42, 42)))

        root.store.close()

        yield f_path
