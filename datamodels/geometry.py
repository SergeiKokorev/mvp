import os
import sys

IMPORTED = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.pardir
))
sys.path.append(IMPORTED)

from const.data_types import *
from datamodels.models import *


class InterfaceBuilder():
    pass
