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

"""
    ls_fn(store=fixture_zarr_small, path=None, level=None)

    captured = capsys.readouterr()
    assert captured.out == expected_output


def test_list_all_arrays(fixture_zarr_small) -> None:
    assert sorted(list_all_arrays(fixture_zarr_small)) == ["grp/ar1"]


def test_ls_with_array_as_path_prints_array_info(fixture_zarr_small, capsys) -> None:
    expected_output = """Type               : Array
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

"""

    ls_fn(store=fixture_zarr_small, path="grp/ar1")

    captured = capsys.readouterr()
    assert captured.out == expected_output


def test_ls_with_no_group_or_array_at_provided_path_prints_hint(fixture_zarr_small, capsys) -> None:
    ls_fn(store=fixture_zarr_small, path="grp/missing_array")

    captured = capsys.readouterr()
    assert captured.out.startswith("No object found in store")
