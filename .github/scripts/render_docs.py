#!/usr/bin/env python3
"""Render README.md into a styled docs page for gh-pages."""

import os
import re
import yaml
import markdown
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
DIST = REPO_ROOT / "dist"
DIST.mkdir(exist_ok=True)

# Load chart metadata
with open(REPO_ROOT / "charts/mlflow/Chart.yaml") as f:
    chart = yaml.safe_load(f)

chart_version = chart.get("version", "")
app_version = chart.get("appVersion", "")
description = chart.get("description", "")

# Read chart README (full detail: examples, values table, etc.)
readme = (REPO_ROOT / "charts/mlflow/README.md").read_text()

md = markdown.Markdown(
    extensions=[
        "fenced_code",
        "tables",
        "pymdownx.highlight",
        "pymdownx.superfences",
        "toc",
        "attr_list",
    ],
    extension_configs={
        "pymdownx.highlight": {"use_pygments": True, "noclasses": True},
    },
)
body_html = md.convert(readme)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>mlflow Helm Chart — MLflow Community</title>
  <meta name="description" content="{description}" />
  <link rel="icon" href="https://raw.githubusercontent.com/mlflow/mlflow/master/assets/logo.svg" />
  <style>
    *, *::before, *::after {{ box-sizing: border-box; }}

    :root {{
      --bg: #0d1117;
      --surface: #161b22;
      --border: #30363d;
      --text: #e6edf3;
      --muted: #8b949e;
      --accent: #58a6ff;
      --accent-hover: #79c0ff;
      --green: #3fb950;
      --code-bg: #1f2428;
      --inline-code-bg: #1f2428;
      --radius: 6px;
    }}

    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      font-size: 16px;
      line-height: 1.65;
      background: var(--bg);
      color: var(--text);
    }}

    header {{
      background: var(--surface);
      border-bottom: 1px solid var(--border);
      padding: 16px 24px;
      display: flex;
      align-items: center;
      gap: 16px;
    }}
    header img {{ height: 36px; }}
    header .meta {{ display: flex; flex-direction: column; }}
    header .meta strong {{ font-size: 1.1rem; color: var(--text); }}
    header .meta span {{ font-size: 0.85rem; color: var(--muted); }}

    .badges {{
      margin-left: auto;
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      align-items: center;
    }}
    .badge {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      background: var(--code-bg);
      border: 1px solid var(--border);
      border-radius: 999px;
      padding: 2px 10px;
      font-size: 0.78rem;
      color: var(--muted);
      white-space: nowrap;
    }}
    .badge .label {{ color: var(--muted); }}
    .badge .value {{ color: var(--green); font-weight: 600; }}

    .layout {{
      max-width: 960px;
      margin: 0 auto;
      padding: 32px 24px 64px;
    }}

    .install-card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 20px 24px;
      margin-bottom: 32px;
    }}
    .install-card h2 {{
      margin: 0 0 12px;
      font-size: 1rem;
      color: var(--muted);
      font-weight: 500;
      text-transform: uppercase;
      letter-spacing: 0.06em;
    }}
    .install-card pre {{
      margin: 0;
      background: var(--code-bg);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 12px 16px;
      overflow-x: auto;
      font-size: 0.9rem;
    }}

    .content h1, .content h2, .content h3,
    .content h4, .content h5, .content h6 {{
      color: var(--text);
      margin-top: 1.8em;
      margin-bottom: 0.5em;
      padding-bottom: 0.3em;
    }}
    .content h1 {{ display: none; }}  /* already in header */
    .content h2 {{ font-size: 1.35rem; border-bottom: 1px solid var(--border); }}
    .content h3 {{ font-size: 1.1rem; }}

    .content a {{ color: var(--accent); text-decoration: none; }}
    .content a:hover {{ color: var(--accent-hover); text-decoration: underline; }}

    .content p {{ margin: 0.6em 0 1em; }}

    .content code {{
      background: var(--inline-code-bg);
      border: 1px solid var(--border);
      border-radius: 3px;
      padding: 2px 5px;
      font-size: 0.87em;
      font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
    }}

    .content pre {{
      background: var(--code-bg);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 16px;
      overflow-x: auto;
      line-height: 1.5;
    }}
    .content pre code {{
      background: none;
      border: none;
      padding: 0;
      font-size: 0.88rem;
    }}

    .content table {{
      border-collapse: collapse;
      width: 100%;
      margin: 1em 0;
      font-size: 0.9rem;
      overflow-x: auto;
      display: block;
    }}
    .content th, .content td {{
      border: 1px solid var(--border);
      padding: 8px 12px;
      text-align: left;
    }}
    .content th {{
      background: var(--surface);
      color: var(--text);
      font-weight: 600;
    }}
    .content tr:nth-child(even) td {{ background: #0d1117; }}

    .content blockquote {{
      border-left: 4px solid var(--accent);
      margin: 1em 0;
      padding: 4px 16px;
      color: var(--muted);
    }}

    .content hr {{
      border: none;
      border-top: 1px solid var(--border);
      margin: 2em 0;
    }}

    .content img {{ max-width: 100%; }}

    footer {{
      text-align: center;
      padding: 24px;
      font-size: 0.82rem;
      color: var(--muted);
      border-top: 1px solid var(--border);
    }}
    footer a {{ color: var(--accent); text-decoration: none; }}

    @media (max-width: 600px) {{
      header {{ flex-wrap: wrap; }}
      .badges {{ margin-left: 0; }}
    }}
  </style>
</head>
<body>
  <header>
    <img src="https://raw.githubusercontent.com/mlflow/mlflow/master/assets/logo.svg" alt="MLflow logo" />
    <div class="meta">
      <strong>mlflow</strong>
      <span>MLflow Community Helm Chart</span>
    </div>
    <div class="badges">
      <span class="badge"><span class="label">chart</span><span class="value">v{chart_version}</span></span>
      <span class="badge"><span class="label">app</span><span class="value">v{app_version}</span></span>
      <a href="https://artifacthub.io/packages/helm/mlflow-community/mlflow" target="_blank">
        <img src="https://img.shields.io/endpoint?url=https://artifacthub.io/badge/repository/mlflow-community" alt="Artifact Hub" style="height:20px;border-radius:4px;" />
      </a>
    </div>
  </header>

  <div class="layout">
    <div class="install-card">
      <h2>Install</h2>
      <pre><code>helm repo add mlflow-community https://mlflow-community.github.io/helm-charts
helm repo update
helm install mlflow mlflow-community/mlflow</code></pre>
    </div>

    <div class="content">
      {body_html}
    </div>
  </div>

  <footer>
    <p>
      <a href="https://github.com/mlflow-community/helm-charts">GitHub</a> &nbsp;·&nbsp;
      <a href="https://artifacthub.io/packages/helm/mlflow-community/mlflow">Artifact Hub</a> &nbsp;·&nbsp;
      <a href="https://mlflow.org">MLflow</a>
    </p>
  </footer>
</body>
</html>
"""

out = DIST / "index.html"
out.write_text(html)
print(f"Written: {out} ({out.stat().st_size} bytes)")
