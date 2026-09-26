"""Existing dynamics tab content."""
from nicegui import ui

def create_dynamics() -> None:
    ui.label(
        'Innovation Dynamics'
    ).classes('text-2xl font-bold')

    with ui.card().classes('w-full mb-4'):
        ui.label('Experiment').classes('font-bold')
        ui.label(
            'A unit innovation occurs at time 0. '
            'How quickly does its effect disappear?'
        )

    with ui.row().classes('w-full gap-4'):

        with ui.card().classes(
            'grow h-96 items-center justify-center'
        ):
            ui.label('Innovation response: ψⱼ')

        with ui.card().classes(
            'grow h-96 items-center justify-center'
        ):
            ui.label('Cumulative response')
