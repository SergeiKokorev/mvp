import os
import sys

IMPORTED = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.pardir
))
sys.path.append(IMPORTED)

from const.data_types import *
from datamodels.models import *


class Expression(DataModel):

    def __init__(self, variable: str, expression: str, description: str='', checked: bool=True) -> None:
        self.variable = variable
        self.expression = expression
        self.description = description
        self.checked = checked
        super().__init__()
        self._type = DATA.EXPRESSION

    @property
    def tooltip(self) -> str:
        return self.description

    def view(self) -> str:
        return f'{self.variable} = {self.expression}\n'

    def json(self) -> dict:
        return {'type': self.datatype.value, 'variable': self.variable, 
                'expression': self.expression, 
                'description': self.description,
                'checked': self.checked}

    def data(self) -> dict:
        return self.json()

    def update(self, **settings) -> None:
        self.variable = settings.get('variable', self.variable)
        self.expression = settings.get('expression', self.expression)
        self.description = settings.get('description', self.description)
        self.checked = settings.get('checked', self.checked)
        return super().update(**settings)

    def info(self) -> str:
        return f'{self.variable} = {self.expression} ({self.description})'

    def cse(self) -> str:
        return f'! ${self.variable} = {self.expression} #{self.description}\n'

    def __str__(self) -> str:
        return self.view()

    def __repr__(self) -> str:
        return self.cse()


class Performance(DataModel):

    def __init__(self, curve: str, files: list, inlet: str, outlet: str, description: str='') -> None:
        self.curve = curve
        self.files = files
        self.inlet = inlet
        self.outlet = outlet
        self.description = description
        super().__init__()
        self._type = DATA.PERFORMANCE

    @property
    def tooltip(self):
        return self.description

    def update(self, **settings) -> None:
        self.curve = settings.get('curve', self.curve)
        self.files = settings.get('files', self.files)
        self.inlet = settings.get('inlet', self.inlet)
        self.outlet = settings.get('outlet', self.outlet)
        self.description = settings.get('description', self.description)
        return super().update(**settings)

    def view(self) -> list:
        return f'{self.curve}'

    def info(self) -> str:
        return f'{self.curve}:\t{self.files}\tInlet: {self.inlet};\tOutlet: {self.outlet}'

    def cse(self):
        return f'! my @files = ({self.files}[1:-1]);\n! for my $f (@files) {{}};\n'

    def json(self) -> dict:
        return {'type': self.datatype.value, 'curve': self.curve,
                'inlet': self.inlet, 'outlet': self.outlet,
                'files': self.files, 'description': self.description}

    def __str__(self) -> str:
        return self.view()

    def __repr__(self) -> str:
        return self.cse()
