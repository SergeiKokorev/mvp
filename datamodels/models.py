from __future__ import annotations

import os
import sys

IMPORTED = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.pardir
))
sys.path.append(IMPORTED)

from copy import deepcopy
from abc import ABCMeta, abstractmethod


from const.data_types import DATA
from utils.errorhandler import Error


class DataModel(metaclass=ABCMeta):

    def __init__(self) -> None:
        self._type: DATA = None

    @property
    def datatype(self) -> DATA:
        return self._type

    @datatype.setter
    def datatype(self, datatype: str) -> None:
        if not isinstance(datatype, str) : raise TypeError(f'Data type must be str type, given {type(datatype).__class__.__name__}')
        self._type = datatype

    @abstractmethod
    def view(self) -> str:
        pass

    @abstractmethod
    def json(self) -> dict:
        pass

    def clone(self) -> DataModel:
        return deepcopy(self)


class AbstractDataCacheModel(metaclass=ABCMeta):

    cache = {}
    
    @abstractmethod
    def add(self, data: DataModel) -> bool:
        pass

    @abstractmethod
    def delete(self, table: str, idx: int) -> bool:
        pass

    @abstractmethod
    def insert(self, data: DataModel, idx: int) -> bool:
        pass

    @abstractmethod
    def get(self, datatype: str, id: int) -> DataModel:
        pass

    @abstractmethod
    def json(self, datatype: str) -> dict | None:
        pass

    @abstractmethod
    def view(self, datatype: str) -> str | None:
        pass


class DataCacheModel(AbstractDataCacheModel):

    cache = dict([(data.value, []) for data in (DATA)])

    def add(self, data: DataModel) -> bool:
        
        if not isinstance(data, DataModel) : raise TypeError(Error.TYPEERR.format(DataModel.__class__.__name__, type(data).__class__.__name__))
        
        try:
            self.cache[data.datatype.value].append(data)
            return True
        except KeyError:
            raise Error.KEYERR.format(data.datatype.value)
        except AttributeError:
            raise Error.ATTRERROR.format(data.__class__.__name__)
        except Exception:
            return False

    def delete(self, table: str, idx: int) -> bool:

        if not isinstance(table, str) : raise Error.NOTSTR.format('Data type', type(table).__class__.__name__)
        if not isinstance(idx, int) : raise Error.NOTINT.format('ID', type(idx).__class__.__name__)

        try:
            del self.cache[table][idx]
            return True
        except (KeyError, IndexError):
            raise Error.KEYERR.format(table)
        except Exception:
            return False

    def insert(self, data: DataModel, idx: int) -> bool:

        if not isinstance(data, DataModel) : raise Error.NOTSTR.format('Data type', type(data).__class__.__name__)
        if not isinstance(idx, int) : raise Error.NOTINT.format('ID', type(idx).__class__.__name__)
        if not data.datatype in self.cache.keys() : return False

        try:
            self.cache[data.datatype].insert(idx, data)
            return True
        except Exception:
            return False

    def get(self, datatype: str, idx: int) -> DataModel | None:

        if not isinstance(datatype, str) : raise Error.NOTSTR.format('Data type', type(datatype).__class__.__name__)
        if not isinstance(idx, int) : raise Error.NOTINT.format('ID', type(idx).__class__.__name__)
        if not datatype in self.cache.keys() : return None

        try:
            return self.cache[datatype][idx].clone()
        except IndexError:
            return None
        except Exception:
            return None

    def json(self, datatype: str) -> dict | None:
        if not isinstance(datatype, str) : raise Error.NOTSTR.format('Data type', type(datatype).__class__.__name__)
        if not datatype in self.cache.keys() : return None

        try:
            return dict([(i, data.json()) for i, data in enumerate(self.cache[datatype])])
        except AttributeError:
            raise Error.ATTRERROR(datatype)
        except TypeError:
            return None

    def view(self, datatype: str) -> str | None:
        
        if not isinstance(datatype, str) : raise Error.NOTSTR.format('Data type', type(datatype).__class__.__name__)
        if not datatype in self.cache.keys() : return None

        try:
            return dict([(i, data.view()) for i, data in enumerate(self.cache[datatype])])
        except AttributeError:
            raise Error.ATTRERROR(datatype)
        except TypeError:
            return None
