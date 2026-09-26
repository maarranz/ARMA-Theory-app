# ARMA Theory Explorer

A NiceGUI teaching app for exploring theoretical autoregressive moving-average (ARMA) models. `arma_theory.py` provides the econometric engine; `app.py` assembles per-client pages from the UI components.

## Current functionality

- Choose an example model or specify a custom ARMA(p, q), with p and q from 0 to 2.
- Adjust reactive coefficient controls and see the model equation update.
- Inspect reactive diagnostics for causality, invertibility, and minimal representation.

## Planned features

- **Properties:** interactive inverse-root plots.
- **ACF & PACF:** theoretical autocorrelation and partial autocorrelation plots.
- **Innovation Dynamics:** responses to innovations.
- **Values:** numerical values and tables.

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

`examples.py` contains the built-in model specifications. `model_state.py` holds per-client control references, coefficient extraction, equation formatting, and change subscriptions. `components/sidebar.py` owns model inputs and example loading; `components/properties.py` owns diagnostics. The remaining components preserve the placeholder tabs.

The `@ui.page('/')` factory creates fresh controls and callbacks for every client. There is no shared mutable UI/model instance at module level. `arma_theory.py` remains the unchanged econometric engine.
