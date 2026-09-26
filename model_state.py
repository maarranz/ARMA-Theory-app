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
