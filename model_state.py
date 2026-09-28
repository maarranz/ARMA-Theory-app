"""Per-client model controls and shared helpers. Never instantiate globally."""
from collections.abc import Callable
from dataclasses import dataclass

from nicegui import ui

@dataclass
class ModelState:
    """References only the controls owned by one page/client."""

    p: ui.select
    q: ui.select
    phi1: ui.number
    phi2: ui.number
    theta1: ui.number
    theta2: ui.number

    def on_change(self, callback: Callable[[], None]) -> None:
        """Subscribe to all model inputs within this client's page."""
        for control in (self.p, self.q, self.phi1, self.phi2, self.theta1, self.theta2):
            control.on_value_change(lambda _, callback=callback: callback())

    def current_coefficients(self):
        """Return the AR and MA coefficients for the current model."""

        ar_order = int(self.p.value)
        ma_order = int(self.q.value)

        ar = [
            float(self.phi1.value or 0.0),
            float(self.phi2.value or 0.0),
        ][:ar_order]

        ma = [
            float(self.theta1.value or 0.0),
            float(self.theta2.value or 0.0),
        ][:ma_order]

        return ar, ma

    def equation(self) -> str:
        ar_order = int(self.p.value)
        ma_order = int(self.q.value)

        # AR polynomial: 1 - φ₁L - φ₂L²
        ar_terms = ['1']

        ar_values = [self.phi1.value, self.phi2.value][:ar_order]

        for i, coefficient in enumerate(ar_values, start=1):
            coefficient = float(coefficient or 0.0)
            sign = '-' if coefficient >= 0 else '+'
            power = 'L' if i == 1 else f'L^{i}'
            ar_terms.append(f'{sign} {abs(coefficient):.2f}{power}')

        # MA polynomial: 1 + θ₁L + θ₂L²
        ma_terms = ['1']

        ma_values = [self.theta1.value, self.theta2.value][:ma_order]

        for i, coefficient in enumerate(ma_values, start=1):
            coefficient = float(coefficient or 0.0)
            sign = '+' if coefficient >= 0 else '-'
            power = 'L' if i == 1 else f'L^{i}'
            ma_terms.append(f'{sign} {abs(coefficient):.2f}{power}')

        ar_polynomial = ' '.join(ar_terms)
        ma_polynomial = ' '.join(ma_terms)

        return rf'$$ ({ar_polynomial})y_t = ({ma_polynomial})\varepsilon_t $$'

    def equation_mathml(self) -> str:
        """Native browser math markup generated only from numeric model inputs."""
        ar, ma = self.current_coefficients()

        def polynomial(coefficients, ar_side):
            terms = ['<mn>1</mn>']
            for lag, coefficient in enumerate(coefficients, 1):
                if f'{abs(coefficient):.2f}' == '0.00':
                    continue
                negative = coefficient >= 0 if ar_side else coefficient < 0
                sign = '−' if negative else '+'
                power = '<mi>L</mi>' if lag == 1 else f'<msup><mi>L</mi><mn>{lag}</mn></msup>'
                terms.append(f'<mo>{sign}</mo><mn>{abs(coefficient):.2f}</mn>{power}')
            return '<mrow><mo>(</mo>' + ''.join(terms) + '<mo>)</mo></mrow>'

        return (
            '<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">'
            '<mrow>' + polynomial(ar, True) + '<msub><mi>y</mi><mi>t</mi></msub>'
            '<mo>=</mo>' + polynomial(ma, False) +
            '<msub><mi>ε</mi><mi>t</mi></msub></mrow></math>'
        )


def format_roots(roots) -> str:
    """Format diagnostic roots without exposing NumPy array notation."""
    def format_root(root):
        value = complex(root)
        real = f'{value.real:.4g}' if value.real else '0'
        if abs(value.imag) < 1e-12:
            return real
        sign = '+' if value.imag >= 0 else '−'
        return f'{real} {sign} {abs(value.imag):.4g}i'

    return '; '.join(format_root(root) for root in roots) or 'None (constant polynomial)'
