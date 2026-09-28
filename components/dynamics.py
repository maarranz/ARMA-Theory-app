"""Per-client innovation and cumulative responses from the ARMA engine."""
from nicegui import ui

import arma_theory as arma
from model_state import ModelState

NONCAUSAL_MESSAGE = (
    'This model is non-causal. Finite-horizon innovation responses are shown, '
    'but they need not decay or converge. No long-run response is defined.'
)


def create_dynamics(state: ModelState) -> None:
    ui.label('Innovation Dynamics').classes('text-2xl font-bold')
    ui.label(
        'Innovation-response coefficients trace the effect of a one-unit innovation through time. '
        'The cumulative response adds those effects through each horizon.'
    ).classes('text-sm')
    horizon = ui.select(list(range(5, 51)), value=20, label='Response horizon').classes('w-48')
    message = ui.label(NONCAUSAL_MESSAGE)
    with ui.column().classes('w-full'):
        with ui.card() as long_run_card:
            ui.label('Analytical long-run cumulative response').classes('font-bold')
            long_run = ui.label().classes('text-xl')
        with ui.element('div').classes('w-full').style(
            'display: grid; gap: 1rem; '
            'grid-template-columns: repeat(auto-fit, minmax(min(100%, 400px), 1fr))'
        ):
            with ui.card().classes('w-full min-w-0'):
                ui.label('Innovation response: ψⱼ').classes('font-bold')
                response = ui.plotly({'data': [], 'layout': {}}).classes('w-full')
            with ui.card().classes('w-full min-w-0'):
                ui.label('Cumulative innovation response').classes('font-bold')
                cumulative = ui.plotly({'data': [], 'layout': {}}).classes('w-full')

    def update_dynamics():
        ar, ma = state.current_coefficients()
        causal = arma.arma_diagnostics(ar, ma)['causal']
        message.set_visibility(not causal)
        h = int(horizon.value)
        data = arma.arma_dynamics(ar, ma, horizon=h)
        response.update_figure(arma.plotly_arma_dynamic_response(ar, ma, horizon=h))
        figure = arma.plotly_arma_cumulative_response(ar, ma, horizon=h)
        # Present the analytical limit in the card, without its engine-added overlay.
        figure.layout.shapes = tuple(s for s in figure.layout.shapes if s.line.dash != 'dash')
        figure.layout.annotations = ()
        cumulative.update_figure(figure)
        long_run_card.set_visibility(causal and data['long_run_exists'])
        long_run.set_text(f"{data['long_run_response']:.6g}" if causal and data['long_run_exists'] else '')

    state.on_change(update_dynamics)
    horizon.on_value_change(lambda _: update_dynamics())
    update_dynamics()
