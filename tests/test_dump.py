from explorzarr.dump import dump_fn


def test_dump_summary(fixture_zarr_small, capsys) -> None:
    expected_output = """[[[1. 1. 1. ... 1. 1. 1.]
  [1. 1. 1. ... 1. 1. 1.]
  [1. 1. 1. ... 1. 1. 1.]
  ...
  [1. 1. 1. ... 1. 1. 1.]
  [1. 1. 1. ... 1. 1. 1.]
  [1. 1. 1. ... 1. 1. 1.]]

 [[1. 1. 1. ... 1. 1. 1.]
  [1. 1. 1. ... 1. 1. 1.]
  [1. 1. 1. ... 1. 1. 1.]
  ...
  [1. 1. 1. ... 1. 1. 1.]
  [1. 1. 1. ... 1. 1. 1.]
  [1. 1. 1. ... 1. 1. 1.]]

 [[1. 1. 1. ... 1. 1. 1.]
  [1. 1. 1. ... 1. 1. 1.]
  [1. 1. 1. ... 1. 1. 1.]
  ...
  [1. 1. 1. ... 1. 1. 1.]
  [1. 1. 1. ... 1. 1. 1.]
  [1. 1. 1. ... 1. 1. 1.]]

 ...

 [[1. 1. 1. ... 1. 1. 1.]
  [1. 1. 1. ... 1. 1. 1.]
  [1. 1. 1. ... 1. 1. 1.]
  ...
  [1. 1. 1. ... 1. 1. 1.]
  [1. 1. 1. ... 1. 1. 1.]
  [1. 1. 1. ... 1. 1. 1.]]

 [[1. 1. 1. ... 1. 1. 1.]
  [1. 1. 1. ... 1. 1. 1.]
  [1. 1. 1. ... 1. 1. 1.]
  ...
  [1. 1. 1. ... 1. 1. 1.]
  [1. 1. 1. ... 1. 1. 1.]
  [1. 1. 1. ... 1. 1. 1.]]

 [[1. 1. 1. ... 1. 1. 1.]
  [1. 1. 1. ... 1. 1. 1.]
  [1. 1. 1. ... 1. 1. 1.]
  ...
  [1. 1. 1. ... 1. 1. 1.]
  [1. 1. 1. ... 1. 1. 1.]
  [1. 1. 1. ... 1. 1. 1.]]]
"""

    dump_fn(store=fixture_zarr_small, array_path="grp/ar1")

    captured = capsys.readouterr()
    assert captured.out == expected_output


def test_dump_full(fixture_zarr_tiny, capsys) -> None:
    expected_output = """[[1. 1.]]
"""

    dump_fn(store=fixture_zarr_tiny, array_path="grp/ar1", full_array=True)

    captured = capsys.readouterr()
    assert captured.out == expected_output


def test_list_arrays_if_wrong_array_path(fixture_zarr_small, capsys) -> None:
    expected_output = """['grp/ar1']

Cannot find array_path "missing/array", use any of the arrays found in the ZARR store listed above
"""
    dump_fn(store=fixture_zarr_small, array_path="missing/array")

    captured = capsys.readouterr()
    assert captured.out == expected_output
