set positional-arguments

test *args: install
  uv run pytest {{args}}

format *args: install
  uv run ruff format {{args}}

lint *args: install
  uv run ruff check {{args}}

lint-fix *args: install
  uv run ruff check --fix {{args}}

format-check *args: install
  uv run ruff format --check {{args}}

typecheck *args: install
  uv run ty check {{args}}

check: install
  uv run ruff format --check .
  uv run ruff check .
  uv run ty check

install:
  uv sync --all-extras --group dev
