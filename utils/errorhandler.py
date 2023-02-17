from enum import StrEnum, Enum


class Error(StrEnum):

    NOTINT = '{} must be int type not {}'
    NOTSTR = '{} must be str type not {}'
    KEYERR = 'There is no data with datatype {}'
    TYPEERR = 'Data type error. Type must be {}, given {}'
    ATTRERROR = 'Data {} doesn\'t contain any elements'
