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
        return f'{self.variable} = {self.expression}'

    def json(self) -> dict:
        return {'type': self.datatype.value, 'variable': self.variable, 
                'expression': self.expression, 
                'description': self.description,
                'checked': self.checked}

    def cse(self) -> str:
        return f'! ${self.variable} = {self.expression} #{self.description}'

    def __str__(self) -> str:
        return self.view()

    def __repr__(self):
        return self.cse()


class Performance(DataModel):

    def __init__(self, curve: str, files: list, inlet: str, outlet: str, description: str='') -> None:
        self.curve = curve
        self.files = files
        self.inlet = self.inlet
        self.outlet = outlet
        self.description = description
        super().__init__()
        self._type = DATA.EXPRESSION

    def view(self) -> str:
        return f'{self.curve} -> files: {[os.path.split(f)[1] for f in self.files]}'

    def json(self) -> dict:
        return {'type': self.datatype.value, 'curve': self.curve,
                'inlet': self.inlet, 'outlet': self.outlet,
                'files': self.files, 'description': self.description}


class Table(DataCacheModel):

    def __init__(self):
        self.table = None

    def delete(self, idx: int) -> bool:
        return super().delete(self.table, idx)

    def get(self, idx: int) -> DataModel | None:
        return super().get(self.table, idx)

    def json(self) -> dict | None:
        return super().json(self.table)

    def view(self) -> str | None:
        return super().view(self.table)


class ExpressionTable(Table):

    def __init__(self):
        super().__init__()
        self.table = DATA.EXPRESSION.value

class PerformanceTable(Table):

    def __init__(self):
        super().__init__()
        self.table = DATA.PERFORMANCE.value
