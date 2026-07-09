# AGENTS.md — ROSS (High-Signal Notes for OpenCode)

## Commands That Matter

```bash
python -m pip install -e ".[dev]"
```

```bash
ruff check ross
ruff format ross
```

```bash
pytest -q ross
```

## Biggest Foot-Gun

- Do **not** run bare `pytest` from the repo root: `pytest.ini` enables `--doctest-modules`, so pytest will import non-test modules, including `docs/run_notebooks.py`, which executes every `*.ipynb` it can find at import time.
- If you actually want to execute notebooks, run the script explicitly from the directory you intend to cover (it uses `Path.cwd().rglob("*.ipynb")`):
  - Docs notebooks only: `cd docs && python run_notebooks.py`

## Doctest Stability

- Doctests are always on (`pytest.ini: addopts = --doctest-modules`). Keep docstring example output stable.
- For truncated/large outputs, use `# doctest: +ELLIPSIS`.
- Numpy printing differences are handled in `ross/conftest.py` (sets `np.set_printoptions(legacy="1.25")` for numpy>=2). If doctests fail, check output formatting first.

## Repo Entry Points (When Editing Behavior)

- `ross/rotor_assembly.py`: `Rotor` assembly + most `.run_*()` analyses.
- `ross/results.py`: results containers + `.plot_*()`.
- `ross/element.py` + `ross/*_element.py`: element implementations.
- Units are SI internally; `rs.Q_` and `@check_units` are used heavily (see `ross/units.py`).

## Docs Build

- From `docs/`: `make html`
- To skip notebook execution during docs build: `make EXECUTE_NOTEBOOKS=off html` (read by `docs/conf.py`).
- If Sphinx deps are missing/pinned: `python -m pip install -r docs/requirements.txt`.

## Cross-References

- `CLAUDE.md`: library workflow, API table, and dev conventions.
- `docs/cookbook/`: self-contained analysis recipes.
- `01_Sinha_HOS_replication/CLAUDE.md`: separate notebook/research guardrails (read before editing anything under that directory).

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
