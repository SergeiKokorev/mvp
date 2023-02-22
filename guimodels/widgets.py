from __future__ import annotations

import os
import sys

IMPORTED = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.pardir
))
sys.path.append(IMPORTED)

from typing import Optional, Sequence, Union, Any

from PySide6.QtWidgets import (
    QWidget, QTabWidget, QListView,
    QAbstractScrollArea
)
from PySide6.QtCore import (
    QModelIndex, QPersistentModelIndex, QSize
)

from guimodels.models import *


class TabView(QTabWidget, AbstractWidget):

    def __init__(self, parent: Optional[QWidget]=None, tabs: Sequence[(QWidget, str)]=None) -> None:
        super(TabView, self).__init__(parent)
        for tab in tabs:
            self.addTab(*tab)
        
    def setup(self, **settings) -> None:
        self.setMovable(settings.get('movable', True))
        self.setTabEnabled(settings.get('enbaled', True))
        return super().update(**settings)
    
    def update(self, **settings) -> None:
        return super().update(**settings)

    def data(self) -> Any:
        return super().data()


class ListView(QListView, AbstractWidget):

    def __init__(self, parent: Optional[QWidget]=None) -> None:
        super(ListView, self).__init__(parent)
        self.data_model = None

    def setup(self, **settings) -> dict:
        self.setMinimumSize(QSize(*settings.get('min_size', [300, 600])))
        self.setMaximumSize(QSize(*settings.get('max_size', [500, 1200])))
        self.setSizeAdjustPolicy(settings.get('adjust_size', QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents))

    def update(self, index: Union[QModelIndex, QPersistentModelIndex]) -> None:
        return super().update(index)
