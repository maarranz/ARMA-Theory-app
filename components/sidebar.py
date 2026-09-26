"""Model controls and example-loading callbacks, created for each client."""
from nicegui import ui

from examples import EXAMPLES
from model_state import ModelState

def create_sidebar() -> ModelState:
    with ui.left_drawer(value=True).classes('p-4'):

        ui.label('Model Specification').classes('text-xl font-bold')
        ui.label(
            'Choose an example or construct your own ARMA model.'
        ).classes('text-sm mb-4')

        example = ui.select(
            options=['Custom model'] + list(EXAMPLES.keys()),
            value='AR(1): persistent',
            label='Try an example',
        ).classes('w-full')

        ui.separator().classes('my-4')

        with ui.row().classes('w-full gap-4'):
            p = ui.select(
                options=[0, 1, 2],
                value=1,
                label='AR order p',
            ).classes('grow')

            q = ui.select(
                options=[0, 1, 2],
                value=0,
                label='MA order q',
            ).classes('grow')

        ui.label('AR coefficients').classes('font-bold mt-4')
        phi1 = ui.number(
            label='φ₁',
            value=0.7,
            min=-2.0,
            max=2.0,
            step=0.05,
            format='%.2f',
        ).classes('w-full')

        phi2 = ui.number(
            label='φ₂',
            value=0.0,
            min=-2.0,
            max=2.0,
            step=0.05,
            format='%.2f',
        ).classes('w-full')

        ui.label('MA coefficients').classes('font-bold mt-4')
        theta1 = ui.number(
            label='θ₁',
            value=0.0,
            min=-2.0,
            max=2.0,
            step=0.05,
            format='%.2f',
        ).classes('w-full')

        theta2 = ui.number(
            label='θ₂',
            value=0.0,
            min=-2.0,
            max=2.0,
            step=0.05,
            format='%.2f',
        ).classes('w-full')

        state = ModelState(p, q, phi1, phi2, theta1, theta2)

        def update_coefficient_visibility():
            ar_order = int(p.value)
            ma_order = int(q.value)

            phi1.set_visibility(ar_order >= 1)
            phi2.set_visibility(ar_order >= 2)

            theta1.set_visibility(ma_order >= 1)
            theta2.set_visibility(ma_order >= 2)

        p.on_value_change(lambda _: update_coefficient_visibility())
        q.on_value_change(lambda _: update_coefficient_visibility())

        update_coefficient_visibility()

        def load_example():
            name = example.value

            if name == 'Custom model':
                return

            spec = EXAMPLES[name]

            # Set model orders
            p.set_value(spec['p'])
            q.set_value(spec['q'])

            # Reset all coefficients first
            phi1.set_value(0.0)
            phi2.set_value(0.0)
            theta1.set_value(0.0)
            theta2.set_value(0.0)

            # Load AR coefficients
            if len(spec['ar']) >= 1:
                phi1.set_value(spec['ar'][0])

            if len(spec['ar']) >= 2:
                phi2.set_value(spec['ar'][1])

            # Load MA coefficients
            if len(spec['ma']) >= 1:
                theta1.set_value(spec['ma'][0])

            if len(spec['ma']) >= 2:
                theta2.set_value(spec['ma'][1])

            update_coefficient_visibility()

        example.on_value_change(lambda _: load_example())
        load_example()

    return state
