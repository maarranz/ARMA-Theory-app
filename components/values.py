"""Existing values tab content."""
from nicegui import ui

def create_values() -> None:
    ui.label(
        'Numerical Values'
    ).classes('text-2xl font-bold')

    ui.label(
        'Detailed roots, ACF, PACF, ψ-weights, and cumulative '
        'responses will be available here.'
    )

    with ui.card().classes('w-full mt-4'):
        ui.label('Numerical results table')
