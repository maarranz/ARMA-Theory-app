"""Per-client theoretical ACF and PACF plots."""
from nicegui import ui

import arma_theory as arma
from model_state import ModelState


def create_correlations(state: ModelState) -> None:
    ui.label('Theoretical ACF & PACF').classes('text-2xl font-bold')

    with ui.card().classes('w-full mb-4'):
        ui.label('What should I look for?').classes('font-bold')
        ui.label(
            'Look for cutoff, gradual decay, alternating signs, '
            'and oscillatory patterns. Change a coefficient and '
            'see how the correlation structure responds.'
        )

    maximum_lag = ui.select(
        options=list(range(10, 51)), value=20, label='Maximum lag',
    ).classes('w-40')
    noncausal_message = ui.label(
        'The theoretical ACF and PACF are not displayed because '
        'this ARMA specification is not causal.'
    )

    with ui.element('div').classes('w-full').style(
        'display: grid; gap: 1rem; '
        'grid-template-columns: repeat(auto-fit, minmax(min(100%, 400px), 1fr))'
    ) as plots:
        with ui.card().classes('w-full min-w-0'):
            ui.label('Theoretical ACF').classes('font-bold')
            acf_plot = ui.plotly({'data': [], 'layout': {}}).classes('w-full')
        with ui.card().classes('w-full min-w-0'):
            ui.label('Theoretical PACF').classes('font-bold')
            pacf_plot = ui.plotly({'data': [], 'layout': {}}).classes('w-full')

    def update_correlations():
        ar, ma = state.current_coefficients()
        causal = arma.arma_diagnostics(ar, ma)['causal']
        noncausal_message.set_visibility(not causal)
        plots.set_visibility(causal)
        if not causal:
            return

        n_lags = int(maximum_lag.value)
        acf_plot.update_figure(arma.plotly_arma_acf(ar, ma, n_lags=n_lags))
        pacf_plot.update_figure(arma.plotly_arma_pacf(ar, ma, n_lags=n_lags))

    state.on_change(update_correlations)
    maximum_lag.on_value_change(lambda _: update_correlations())
    update_correlations()
