import os
import sys

IMPORTED = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.pardir
))
sys.path.append(IMPORTED)

from datamodels.models import DataCacheModel, DataModel
from const.data_types import DATA


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

    def data(self) -> list:
        return super().data(self.table)

    def __str__(self) -> str:
        
        out = ''
        if not (data := self.cache.get(self.table)) : return 'None'
        for d in data:
            out += d.__str__()
        return out

    def __repr__(self) -> str:
        
        out = ''
        if not (data := self.cache.get(self.table)) : return '!'
        for d in data:
            out += d.__repr__()
        return out


class ExpressionTable(Table):

    def __init__(self):
        super().__init__()
        self.table = DATA.EXPRESSION.value


class PerformanceTable(Table):

    def __init__(self):
        super().__init__()
        self.table = DATA.PERFORMANCE.value


class LocationTable(Table):

    def __init__(self):
        super().__init__()
        self.table = DATA.LOCATION.value
