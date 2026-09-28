"""Compact, per-client numerical counterparts of the graphical tabs."""
from nicegui import ui

import arma_theory as arma
from model_state import ModelState, format_roots
from components.dynamics import NONCAUSAL_MESSAGE


def create_values(state: ModelState) -> None:
    ui.label('Numerical Values').classes('text-2xl font-bold')
    ui.label('Inspect the model properties and the population quantities behind the plots. '
             'Values are rounded for display.').classes('text-sm')
    with ui.card().classes('w-full'):
        ui.label('Model properties and roots').classes('text-lg font-bold')
        properties = ui.label()
        with ui.expansion('Show numerical roots', icon='functions').classes('w-full'):
            root_labels = {key: ui.label() for key in (
                'ar_roots', 'inverse_ar_roots', 'ma_roots', 'inverse_ma_roots'
            )}
    maximum = ui.select([5, 10, 20, 30, 40, 50], value=10,
                        label='Values through lag / horizon').classes('w-64')

    def table(columns):
        return ui.table(
            columns=[{'name': key, 'label': title, 'field': key, 'align': 'right'}
                     for key, title in columns],
            rows=[], row_key='lag', pagination=11,
        ).classes('w-full').props('dense')

    with ui.card().classes('w-full'):
        ui.label('Theoretical ACF & PACF').classes('text-lg font-bold')
        correlations_message = ui.label(
            'The theoretical ACF and PACF are not displayed because '
            'this ARMA specification is not causal.'
        )
        correlations = table([('lag', 'Lag'), ('acf', 'ACF'), ('pacf', 'PACF')])
    with ui.card().classes('w-full'):
        ui.label('Finite-horizon innovation dynamics').classes('text-lg font-bold')
        dynamics_message = ui.label(NONCAUSAL_MESSAGE)
        long_run = ui.label()
        dynamics = table([('lag', 'Horizon'), ('psi', 'ψⱼ'), ('cumulative', 'Cumulative response')])

    def update_values():
        ar, ma = state.current_coefficients()
        diagnostics = arma.arma_diagnostics(ar, ma)
        properties.set_text(' / '.join([
            'Causal' if diagnostics['causal'] else 'Non-causal',
            'Invertible' if diagnostics['invertible'] else 'Non-invertible',
            'Minimal' if diagnostics['minimal_representation'] else 'Non-minimal',
        ]))
        for key, title in [('ar_roots', 'AR roots'), ('inverse_ar_roots', 'Inverse AR roots'),
                           ('ma_roots', 'MA roots'), ('inverse_ma_roots', 'Inverse MA roots')]:
            root_labels[key].set_text(f'{title}: {format_roots(diagnostics[key])}')
        causal = diagnostics['causal']
        correlations.set_visibility(causal)
        correlations_message.set_visibility(not causal)
        dynamics_message.set_visibility(not causal)
        n = int(maximum.value)
        if causal:
            acf = arma.arma_acf(ar, ma, n_lags=n)
            pacf = arma.arma_pacf(ar, ma, n_lags=n)
            correlations.rows = [dict(lag=j, acf=f'{acf[j]:.6g}', pacf=f'{pacf[j]:.6g}')
                                 for j in range(n + 1)]
        else:
            correlations.rows = []
        data = arma.arma_dynamics(ar, ma, horizon=n)
        long_run.set_visibility(causal and data['long_run_exists'])
        dynamics.rows = [dict(lag=j, psi=f"{data['psi'][j]:.6g}",
                             cumulative=f"{data['cumulative_psi'][j]:.6g}") for j in range(n + 1)]
        long_run.set_text(f"Analytical long-run cumulative response: {data['long_run_response']:.6g}"
                          if causal and data['long_run_exists'] else '')

    state.on_change(update_values)
    maximum.on_value_change(lambda _: update_values())
    update_values()
