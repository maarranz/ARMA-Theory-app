"""Existing correlations tab content."""
from nicegui import ui

def create_correlations() -> None:
    ui.label(
        'Theoretical ACF & PACF'
    ).classes('text-2xl font-bold')

    with ui.card().classes('w-full mb-4'):
        ui.label('What should I look for?').classes('font-bold')
        ui.label(
            'Look for cutoff, gradual decay, alternating signs, '
            'and oscillatory patterns. Change a coefficient and '
            'see how the correlation structure responds.'
        )

    with ui.row().classes('w-full gap-4'):

        with ui.card().classes(
            'grow h-96 items-center justify-center'
        ):
            ui.label('Theoretical ACF')

        with ui.card().classes(
            'grow h-96 items-center justify-center'
        ):
            ui.label('Theoretical PACF')
