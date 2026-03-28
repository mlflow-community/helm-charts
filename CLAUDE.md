# Claude Code Guidelines

## Python

- Always use `uv` for Python package management — never `pip` or `pip3`
- Install into the repo's `.venv` (run `uv venv` first if it doesn't exist)
- Install deps from `pyproject.toml`: `uv pip install -e .`
- Run scripts with `.venv/bin/python <script>` or after activating the venv
- In CI workflows, use `astral-sh/setup-uv` and `uv pip install`

## Docs

The docs page is generated from `charts/mlflow/README.md` and published to the `gh-pages` branch.

- Source of truth: `charts/mlflow/README.md` (and its template `charts/mlflow/README.md.gotmpl`)
- Render locally: `.venv/bin/python .github/scripts/render_docs.py && open dist/index.html`
- Output: `dist/index.html` (gitignored, published to gh-pages via `.github/workflows/docs.yml`)
- After editing `README.md.gotmpl`, manually mirror the changes to `README.md` (helm-docs is not run automatically)
