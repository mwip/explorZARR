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
