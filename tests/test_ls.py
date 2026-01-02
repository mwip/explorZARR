from explorzarr.ls import list_all_arrays, ls_fn


def test_ls_correct_ouput(fixture_zarr_small, capsys):
    expected_output = """Name        : 
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
 

"""  # noqa: W291, W293
    ls_fn(store=fixture_zarr_small, path=None, level=None)

    captured = capsys.readouterr()
    assert captured.out == expected_output


def test_list_all_arrays(fixture_zarr_small) -> None:
    assert sorted(list_all_arrays(fixture_zarr_small)) == ["grp/ar1"]
