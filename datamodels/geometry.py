import os
import sys

IMPORTED = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.pardir
))
sys.path.append(IMPORTED)

from const.data_types import *
from datamodels.models import *
from utils.errorhandler import Error


class AbstractLocationBuilder(Builder):

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def add_isosurface(self) -> bool:
        pass

    @abstractmethod
    def add_plane(self) -> bool:
        pass

    @abstractmethod
    def add_polyline(self) -> bool:
        pass

    @abstractmethod
    def add_turbosurface(self) -> bool:
        pass


class LocationBuilder(AbstractLocationBuilder):

    def __init__(self) -> None:
        self.obj = Location()

    def add_isosurface(self, name: str, domains: list, definition: dict) -> bool:

        if not (definition.get('variable') or definition.get('value')): 
            raise Error.KEYERROR.value.format('Add isosurface definition error.')

        setattr(self.obj, 'loc_type', DATA.ISOSURFACE)
        setattr(self.obj, 'domain_list', domains)
        setattr(self.obj, 'name', name)
        setattr(self.obj, 'variable', definition['variable'])
        setattr(self.obj, 'value', definition['value'])

        return True

    def add_plane(self, name: str, domains: list, definition: dict) -> bool:
        
        if not definition.get('option'):
            raise Error.KEYERROR.value.format('Add plane definition error.')

        setattr(self.obj, 'loc_type', DATA.PLANE)
        setattr(self.obj, 'domain_list', domains)
        setattr(self.obj, 'name', name)
        setattr(self.obj, 'definition', definition)

    def add_polyline(self, name: str, domains: list, definition: dict) -> bool:

        if not (definition.get('boundary list') or definition.get('location')):
            raise Error.KEYERROR.value.format('Add polyline definition error.')
        
        setattr(self.obj, 'loc_type', DATA.POLYLINE)
        setattr(self.obj, 'name', name)
        setattr(self.obj, 'domain_list', domains)
        setattr(self.obj, 'definition', definition)

        return True

    def add_turbosurface(self, name: str, domains: list, definition: dict) -> bool:
        
        if not definition.get('option'):
            raise Error.KEYERROR.value.format('Add turbo surface definition error.')

        setattr(self.obj, 'loc_type', DATA.TURBOSURFACE)
        setattr(self.obj, 'name', name)
        setattr(self.obj, 'domain_list', domains)
        setattr(self.obj, 'definition', definition)


class LocationDirector(Director):

    def __init__(self) -> None:
        super().__init__()

    def construct(self, location_list: dict) -> None:
        
        for location_type, settings in location_list.items():
            if location_type == DATA.ISOSURFACE.value:
                self._builder.add_isosurface(**settings)
            elif location_type == DATA.PLANE.value:
                self._builder.add_plane(**settings)
            elif location_type == DATA.TURBOSURFACE.value:
                self._builder.add_turbosurface(**settings)
            elif location_type == DATA.POLYLINE.value:
                self._builder.add_polyline(**settings)


class Location(DataModel):

    def __init__(self, name: str=None, domain_list: list=None, definition: dict=None) -> None:
        self.name = name
        self.domain_list = domain_list
        self.definition = definition
        self.loc_type: DATA = None
        super().__init__()
        self._type = DATA.LOCATION

    @property
    def tooltip(self):
        return self.loc_type.value

    def update(self, **settings) -> None:

        self.name = self.name if not (n:=settings.get('name', None)) else n
        self.domain_list = self.domain_list if not (dm:=settings.get('domains', None)) else dm
        self.definition = self.definition if not (df:=settings.get('definition', None)) else df

    def view(self) -> str:
        return f'{self.loc_type.value}: {self.name}'

    def cse(self) -> str:
        out = f'{self.loc_type.name}: {self.name}\n'
        for k, v in self.definition.items():
            out += f'\t{str(k).capitalize()} = {str(v)[1:-1] if isinstance(v, list) else v}\n'
        out += f'\tDomain List = {str(self.domain_list)[1:-1]}\n'
        out += 'END\n'
        return out

    def json(self) -> dict:
        return {'type': self.loc_type.value, 'name': self.name,
                'definition': self.definition}

    def __str__(self) -> str:
        return self.view()

    def __repr__(self) -> str:
        return self.cse()

