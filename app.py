"""Application assembly; each page owns its model controls and callbacks."""
from nicegui import ui

from components.sidebar import create_sidebar
from components.properties import create_properties
from components.correlations import create_correlations
from components.dynamics import create_dynamics
from components.values import create_values

@ui.page('/')
def index():
    ui.page_title('ARMA Theory Explorer')

    # ------------------------------------------------------------
    # Header
    # ------------------------------------------------------------

    with ui.header().classes('items-center justify-between'):
        ui.label('ARMA Theory Explorer').classes('text-2xl font-bold')
        ui.label('ATSE • Theoretical ARMA Models').classes('text-sm')

    state = create_sidebar()

    with ui.column().classes('w-full max-w-7xl mx-auto p-6'):

        # Welcome / pedagogical banner
        with ui.card().classes('w-full'):
            ui.label('Explore the model').classes('text-lg font-bold')
            ui.label(
                'Start with one of the examples or change the coefficients yourself. '
                'Watch how the roots, correlations, and responses change. '
                'You cannot break anything.'
            )

        # Model display

        ui.label('Current model').classes('text-xl font-bold mt-4')

        with ui.card().classes('w-full items-center'):
            model_equation = ui.markdown(
                r'$$ (1 - 0.70L)y_t = \varepsilon_t $$'
            ).classes('text-xl')

        state.on_change(lambda: model_equation.set_content(state.equation()))
        model_equation.set_content(state.equation())

        with ui.tabs().classes('w-full') as tabs:
            properties = ui.tab('Properties')
            correlations = ui.tab('ACF & PACF')
            dynamics = ui.tab('Innovation Dynamics')
            values = ui.tab('Values')

        with ui.tab_panels(tabs, value=properties).classes('w-full'):

            with ui.tab_panel(properties):
                create_properties(state)

            with ui.tab_panel(correlations):
                create_correlations()

            with ui.tab_panel(dynamics):
                create_dynamics()

            with ui.tab_panel(values):
                create_values()

if __name__ in {'__main__', '__mp_main__'}:
    ui.run(title='ARMA Theory Explorer')
