# Utility Shelf Dashboard v2

## Product goals

Find a useful snippet fast, use it through an accessible interface, inspect
its Python implementation, and download outputs without losing them when
Streamlit reruns. The project is a **library of independent Python utilities**
first and an optional hosted user interface second.

## Architecture

- `dashboard_catalogue.py`: static searchable registry (34 tools, 8 categories).
- `dashboard_handlers.py`: one UI handler per utility. All original operations
  were preserved, including their local-only safety gates.
- `dashboard_style.py`: responsive visual tokens for Light and Dark modes.
- `app.py`: home, search, categories, tool workspaces, source viewer and
  session-scoped favourites, recent tools and generated outputs.
- Original utility packages: Python implementations remain importable.

## User journey

1. Open the overview, search a keyword, or pick a category in the sidebar.
2. Open a tool or select one from its category.
3. Use the Workspace tab for inputs, processing and downloads.
4. Use the Python snippet tab for copyable source and the GitHub link.
5. Find your generated outputs on the same workspace, even after switching
   elsewhere and returning. Use Clear result to remove those outputs.
6. Star a tool to find it under Favourites in the overview.

Generated results are kept in server-side Streamlit session state, subject to a 64 MiB per-session budget. Oversized results are offered for immediate download but are not retained.

Generated results are stored in the server-side Streamlit session. They are
**not** persisted to a database, across browsers, or after a server restart.
Favourites and recently used tools are also session-scoped. Results from
different tools remain separated.

## Safety

All privileged filesystem, network and destructive operations remain
disabled on the hosted Space. `ENABLE_LOCAL_OPERATIONS=1` is for a
**trusted local environment only**. Files are processed in temporary
directories and bounded by the original upload limits. The original
security and zip-validation regression tests remain in CI.

Do not convert the server into a public arbitrary file or URL execution API.
If a future version moves away from Streamlit, reuse the registry and Python
utility modules, but implement explicit request validation, rate limits,
authentication for privileged actions, content limits and process isolation.

## Design choices

The first v2 release keeps Streamlit 1.67.0 because it already supports the
required category navigation, source display, upload controls and session
state. Replatforming to React and FastAPI would substantially expand the
security surface and risk breaking the existing Hugging Face deployment
without a proven user benefit. The front-end modules are deliberately
separated so a later migration can happen without rewriting the snippets.

## Testing

The quality workflow validates the catalogue and module contracts on
Python 3.11 and 3.12. The Linux integration workflow exercises Streamlit
`AppTest` interactions and the existing conversion, audio and image
processing paths. The Docker workflow builds the production image and
probes the health endpoint. Review all checks before merging and deploying.
