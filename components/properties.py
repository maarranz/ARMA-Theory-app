"""Reactive model diagnostics, inverse-root plot, and root details."""
from nicegui import ui
import arma_theory as arma
from model_state import ModelState, format_roots



def create_properties(state: ModelState) -> None:
    ui.label('Model Properties').classes('text-2xl font-bold')

    with ui.row().classes('w-full gap-4'):

        with ui.card().classes('grow'):
            ui.label('Causality').classes('font-bold')
            causality_label = ui.label().classes('text-lg')

        with ui.card().classes('grow'):
            ui.label('Invertibility').classes('font-bold')
            invertibility_label = ui.label().classes('text-lg')

        with ui.card().classes('grow'):
            ui.label('Representation').classes('font-bold')
            representation_label = ui.label().classes('text-lg')

    ui.label('Inverse Roots').classes('text-xl font-bold mt-6')
    ui.label('Inverse roots are shown relative to the unit circle: AR roots diagnose '
             'causality; MA roots diagnose invertibility.').classes('text-sm')
    with ui.card().classes('w-full items-center'):
        inverse_root_plot = ui.plotly({'data': [], 'layout': {}}).classes('w-full')

    with ui.expansion('Show root details', icon='functions').classes('w-full mt-4'):
        root_labels = {
            key: ui.label()
            for key in ('ar_roots', 'inverse_ar_roots', 'ma_roots', 'inverse_ma_roots')
        }

    def update_properties():
        ar, ma = state.current_coefficients()
        diagnostics = arma.arma_diagnostics(ar, ma)

        if diagnostics['causal']:
            causality_label.set_text('✓ Causal')
        else:
            causality_label.set_text('✗ Non-causal')

        if diagnostics['invertible']:
            invertibility_label.set_text('✓ Invertible')
        else:
            invertibility_label.set_text('✗ Non-invertible')

        if diagnostics['minimal_representation']:
            representation_label.set_text('✓ Minimal')
        else:
            representation_label.set_text('✗ Non-minimal')

        inverse_root_plot.update_figure(arma.plotly_arma_inverse_roots(ar, ma))
        for key, title in (
            ('ar_roots', 'AR roots'),
            ('inverse_ar_roots', 'Inverse AR roots'),
            ('ma_roots', 'MA roots'),
            ('inverse_ma_roots', 'Inverse MA roots'),
        ):
            root_labels[key].set_text(f'{title}: {format_roots(diagnostics[key])}')

    state.on_change(update_properties)
    update_properties()
