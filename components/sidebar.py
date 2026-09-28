"""Model controls and example-loading callbacks, created for each client."""
from math import isfinite

from nicegui import ui

from examples import EXAMPLES
from model_state import ModelState


class CoefficientNumber(ui.number):
    """Keep NiceGUI numeric semantics without native browser locale formatting.

    Native type=number renders commas on some browsers even with lang=en.
    Only the presentation is text; the standard float conversion and Number
    sanitization still apply. Invalid drafts retain the last valid value and
    are restored to its formatted representation on blur.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.props('type=text inputmode=decimal lang=en')

    def _event_args_to_value(self, event):
        try:
            value = super()._event_args_to_value(event)
        except (TypeError, ValueError, OverflowError):
            return self.value
        if value is None or not isfinite(value):
            return self.value
        # Keep the existing allowed range before any reactive calculations run.
        return float(max(self.min, min(self.max, value)))


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
        phi1 = CoefficientNumber(
            label='φ₁',
            value=0.7,
            min=-2.0,
            max=2.0,
            step=0.05,
            format='%.2f',
        ).classes('w-full')

        phi2 = CoefficientNumber(
            label='φ₂',
            value=0.0,
            min=-2.0,
            max=2.0,
            step=0.05,
            format='%.2f',
        ).classes('w-full')

        ui.label('MA coefficients').classes('font-bold mt-4')
        theta1 = CoefficientNumber(
            label='θ₁',
            value=0.0,
            min=-2.0,
            max=2.0,
            step=0.05,
            format='%.2f',
        ).classes('w-full')

        theta2 = CoefficientNumber(
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

        loading_example = False

        def load_example():
            nonlocal loading_example
            name = example.value

            if name == 'Custom model':
                return

            spec = EXAMPLES[name]

            loading_example = True
            try:
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
            finally:
                loading_example = False

        example.on_value_change(lambda _: load_example())
        load_example()

        def mark_custom():
            if not loading_example:
                example.set_value('Custom model')

        state.on_change(mark_custom)

    return state
