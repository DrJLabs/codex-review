## Python Style
- Follow Python's PEP 8 for spacing, naming, and 79/99 char line guidance; keep imports grouped stdlib/third-party/local and use `from __future__ import annotations` in new modules for forward references.
- Format and lint with Ruff (`ruff check`, `ruff format`). Enable the upstream `pyproject.toml` defaults plus rule sets `E,F,I,N,UP,SIM,PL,PERF,BLE,DTZ` for modern safety/perf checks.
- Require type hints on public APIs (PEP 484). Prefer `typing.Protocol` for structural typing, `TypedDict` for dict contracts, and `Literal` for enums. Validate with `mypy` or `pyright` when available.
- Model structured data with `@dataclass(slots=True)` or Pydantic models. Keep validation in constructors/factories, not scattered across call sites.
- Write docstrings per PEP 257 (Google style or numpydoc) summarizing behaviour, parameters, return types, and raised exceptions.
- Use pathlib for filesystem work, f-strings for formatting, context managers for resource handling, and avoid bare `except Exception`.
