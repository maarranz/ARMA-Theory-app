# ARMA Theory Explorer

A NiceGUI teaching app for exploring theoretical autoregressive moving-average (ARMA) models. `arma_theory.py` provides the econometric engine; `app.py` currently contains the working interface.

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

## Pre-refactor structure

```text
ARMA-Theory-app/
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

`examples.py`, `model_state.py`, and all files in `components/` are empty placeholders for a future refactor. No working code has been moved or duplicated; the existing app behavior is preserved.
