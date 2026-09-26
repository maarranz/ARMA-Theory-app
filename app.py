from nicegui import ui
import arma_theory as arma

EXAMPLES = {
    'AR(1): persistent': {
        'p': 1,
        'q': 0,
        'ar': [0.8],
        'ma': [],
    },

    'AR(1): random walk': {
        'p': 1,
        'q': 0,
        'ar': [1.0],
        'ma': [],
    },

    'AR(1): explosive': {
        'p': 1,
        'q': 0,
        'ar': [1.2],
        'ma': [],
    },

    'AR(2): oscillatory': {
        'p': 2,
        'q': 0,
        'ar': [1.2, -0.8],
        'ma': [],
    },

    'MA(1)': {
        'p': 0,
        'q': 1,
        'ar': [],
        'ma': [0.5],
    },

    'MA(1): non-invertible': {
        'p': 0,
        'q': 1,
        'ar': [],
        'ma': [1.5],
    },

    'ARMA(1,1)': {
        'p': 1,
        'q': 1,
        'ar': [0.8],
        'ma': [0.5],
    },

    'Common root': {
        'p': 1,
        'q': 1,
        'ar': [0.5],
        'ma': [-0.5],
    },

    'ARMA(2,1): complex AR roots': {
        'p': 2,
        'q': 1,
        'ar': [1.2, -0.8],
        'ma': [0.5],
    },
}

# ------------------------------------------------------------
# Page configuration
# ------------------------------------------------------------

ui.page_title('ARMA Theory Explorer')


# ------------------------------------------------------------
# Header
# ------------------------------------------------------------

with ui.header().classes('items-center justify-between'):
    ui.label('ARMA Theory Explorer').classes('text-2xl font-bold')
    ui.label('ATSE • Theoretical ARMA Models').classes('text-sm')


# ------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------

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

    def current_coefficients():
        """Return the AR and MA coefficients for the current model."""

        ar_order = int(p.value)
        ma_order = int(q.value)

        ar = [
            float(phi1.value or 0.0),
            float(phi2.value or 0.0),
        ][:ar_order]

        ma = [
            float(theta1.value or 0.0),
            float(theta2.value or 0.0),
        ][:ma_order]

        return ar, ma


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
        update_model_equation()

# ------------------------------------------------------------
# Main page
# ------------------------------------------------------------

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
        
    def update_model_equation():
        ar_order = int(p.value)
        ma_order = int(q.value)

        # AR polynomial: 1 - φ₁L - φ₂L²
        ar_terms = ['1']

        ar_values = [phi1.value, phi2.value][:ar_order]

        for i, coefficient in enumerate(ar_values, start=1):
            coefficient = float(coefficient or 0.0)
            sign = '-' if coefficient >= 0 else '+'
            power = 'L' if i == 1 else f'L^{i}'
            ar_terms.append(f'{sign} {abs(coefficient):.2f}{power}')

        # MA polynomial: 1 + θ₁L + θ₂L²
        ma_terms = ['1']

        ma_values = [theta1.value, theta2.value][:ma_order]

        for i, coefficient in enumerate(ma_values, start=1):
            coefficient = float(coefficient or 0.0)
            sign = '+' if coefficient >= 0 else '-'
            power = 'L' if i == 1 else f'L^{i}'
            ma_terms.append(f'{sign} {abs(coefficient):.2f}{power}')

        ar_polynomial = ' '.join(ar_terms)
        ma_polynomial = ' '.join(ma_terms)

        model_equation.set_content(
            rf'$$ ({ar_polynomial})y_t = ({ma_polynomial})\varepsilon_t $$'
        )

    p.on_value_change(lambda _: update_model_equation())
    q.on_value_change(lambda _: update_model_equation())

    phi1.on_value_change(lambda _: update_model_equation())
    phi2.on_value_change(lambda _: update_model_equation())
    theta1.on_value_change(lambda _: update_model_equation())
    theta2.on_value_change(lambda _: update_model_equation())

    # Load the initial example only after the equation and handlers exist.
    example.on_value_change(lambda _: load_example())
    load_example()


    # --------------------------------------------------------
    # Tabs
    # --------------------------------------------------------

    with ui.tabs().classes('w-full') as tabs:
        properties = ui.tab('Properties')
        correlations = ui.tab('ACF & PACF')
        dynamics = ui.tab('Innovation Dynamics')
        values = ui.tab('Values')

    with ui.tab_panels(tabs, value=properties).classes('w-full'):

        # ----------------------------------------------------
        # Properties
        # ----------------------------------------------------

        with ui.tab_panel(properties):

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


            def update_properties():
                ar, ma = current_coefficients()
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

            p.on_value_change(lambda _: update_properties())
            q.on_value_change(lambda _: update_properties())

            phi1.on_value_change(lambda _: update_properties())
            phi2.on_value_change(lambda _: update_properties())
            theta1.on_value_change(lambda _: update_properties())
            theta2.on_value_change(lambda _: update_properties())

            update_properties()

            ui.label('Inverse Roots').classes('text-xl font-bold mt-6')

            with ui.card().classes(
                'w-full h-96 items-center justify-center'
            ):
                ui.label(
                    'Interactive inverse-root plot will appear here.'
                ).classes('text-lg')

            with ui.expansion(
                'Show root details',
                icon='functions',
            ).classes('w-full mt-4'):
                ui.label(
                    'Numerical AR and MA roots will appear here.'
                )

        # ----------------------------------------------------
        # ACF / PACF
        # ----------------------------------------------------

        with ui.tab_panel(correlations):

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

        # ----------------------------------------------------
        # Innovation dynamics
        # ----------------------------------------------------

        with ui.tab_panel(dynamics):

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

        # ----------------------------------------------------
        # Numerical values
        # ----------------------------------------------------

        with ui.tab_panel(values):

            ui.label(
                'Numerical Values'
            ).classes('text-2xl font-bold')

            ui.label(
                'Detailed roots, ACF, PACF, ψ-weights, and cumulative '
                'responses will be available here.'
            )

            with ui.card().classes('w-full mt-4'):
                ui.label('Numerical results table')


# ------------------------------------------------------------
# Run application
# ------------------------------------------------------------

ui.run(title='ARMA Theory Explorer')
