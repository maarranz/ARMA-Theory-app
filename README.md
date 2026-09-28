# ARMA Theory Explorer

A NiceGUI teaching app for exploring theoretical autoregressive moving-average (ARMA) models. `arma_theory.py` provides the econometric engine; `app.py` assembles per-client pages from the UI components.

## Current functionality

- Specify ARMA(p, q) models with p and q from 0 to 2, or start from a teaching example.
- Inspect reactive equations, inverse roots, and causality/invertibility/minimality diagnostics.
- Explore theoretical ACF/PACF for causal models and finite innovation dynamics for all models.
- Inspect numerical tables and analytical long-run responses where defined.
- Each client has independent model inputs and lag/horizon settings.

## Setup and run

With Conda installed, run from the repository root:

```bash
conda env create -f environment.yml
conda activate arma_theory_app
python app.py
```

Open the local URL printed by NiceGUI in your browser (normally http://localhost:8080).

## Repository structure

```text
ARMA-Theory-app/
├── .gitignore
├── .python-version
├── requirements.txt
├── app.py
├── arma_theory.py
├── environment.yml
├── README.md
├── LICENSE
├── examples.py
├── model_state.py
└── components/
    ├── __init__.py
    ├── sidebar.py
    ├── properties.py
    ├── correlations.py
    ├── dynamics.py
    └── values.py
```

`examples.py` contains the built-in model specifications. `model_state.py` holds per-client control references, coefficient extraction, equation formatting, and change subscriptions. `components/sidebar.py` owns model inputs and example loading; `components/properties.py` owns diagnostics. The remaining components provide theoretical correlations, finite innovation dynamics, and numerical values.

The `@ui.page('/')` factory creates fresh controls and callbacks for every client. There is no shared mutable UI/model instance at module level. `arma_theory.py` remains the unchanged econometric engine.

## Provisional Render deployment

Create a **Web Service** using the **Python** runtime, with the repository root as
its root directory. This is not a Static Site. No Blueprint, Dockerfile, database,
authentication, secrets, or persistent disk is required.

- Python: **3.14.7**, specified in `.python-version` (matches the tested local runtime).
  Remove any conflicting `PYTHON_VERSION` override in the Render dashboard.
- Build command: `pip install -r requirements.txt`
- Start command: `python app.py`
- Use a single service instance/process initially; do not wrap it in a multi-worker
  Gunicorn command. NiceGUI owns the ASGI server and per-client in-memory UI state.
- Render supplies `PORT`; do not manually hard-code a port. Hosted startup binds
  to `0.0.0.0`, reads `PORT`, and disables auto-reload and browser opening.
- Without `PORT`, local startup uses port 8080. `RENDER=true` also selects hosted
  startup, retaining the fallback port if `PORT` is absent.

For a clean pip installation and production-like local run:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PORT=8091 python app.py
```

Open http://localhost:8091. Test the Examples link (opens GitHub in a new tab),
select an example, edit a coefficient to create a Custom model, and inspect all
four tabs. The Examples URL opens the GitHub file view, not a hosted HTML page.

The four requirements are direct runtime imports, not a full environment freeze.
Matplotlib is required because the engine imports it, even though the UI uses
Plotly. NiceGUI's own dependencies are installed by pip. Pandas, SciPy, and
notebook tooling are not required by the current runtime imports;
`environment.yml` remains available for local Conda development.

### Operational limits

- The app uses live WebSocket connections, which Render Web Services support.
- Models are per-client and in memory. Restarting/redeploying or losing a session
  can reset the student's model. No persistent storage is expected.
- Free services can spin down after inactivity and have cold-start delays. Confirm
  the chosen service plan can handle the class size; local smoke tests are not
  a concurrency or Render Linux load test.
- The known Plotly hidden-chart resize console warning may appear during tab
  changes even when visible charts render correctly.

References: [Render Web Services](https://render.com/docs/web-services),
[Python version selection](https://render.com/docs/python-version),
[WebSockets](https://render.com/docs/websocket),
[Free service limitations](https://render.com/docs/free).
