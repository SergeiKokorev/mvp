from __future__ import annotations

from typing import Optional, Union
from PySide6.QtWidgets import (
    QWidget, QMainWindow, QGridLayout,
    QLayout, QWidgetItem, QLineEdit,
    QCheckBox
)
from PySide6 import QtCore, QtGui

import os
import sys

IMPORTED = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.pardir
))
sys.path.append(IMPORTED)

from guimodels.models import *
from datamodels.tables import *
from guimodels.widgets import *


class Tab(object):

    def __init__(self, parent: Optional[QWidget]=None):
        self.datamodel: DataCacheModel = None
        self.dataview: Union[QtCore.QAbstractListModel, QtCore.QAbstractTableModel] = None

    def update(self, **settings) -> None:
        self.dataview.update(**settings)
        self.datamodel.update(**settings)


class ExpressionEditor(QGridLayout):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.variable = QLineEdit()
        self.expression = QLineEdit()
        self.description = QLineEdit()
        self.checked = QCheckBox()

        self.variable.resize(QSize(32, 64))
        self.expression.resize(QSize(128, 64))

        self.addWidget(self.variable, 0, 0)
        self.addWidget(QLabel(' = '), 0, 1)
        self.addWidget(self.expression, 0, 2)
        self.addWidget(QLabel('Description: '), 1, 0)
        self.addWidget(self.description, 1, 1)
        self.addWidget(self.checked, 1, 2)

    def update(self, data: dict) -> None:
        self.variable.setText(data.get('variable'))
        self.expression.setText(data.get('expression'))
        self.description.setText(data.get('description'))
        self.checked.setChecked(data.get('checked', False))
    
class ExpressionTab(QWidget, Tab):

    def __init__(self, parent: Optional[QWidget] = None):
        super(ExpressionTab, self).__init__(parent)
        self.datamodel = ListModel(data=ExpressionTable())
        self.dataview = ListView()
        self.dataview.setModel(self.datamodel)
        self.dataview.setup()

        layout = QGridLayout()
        layout.setSpacing(0)
        wupper = QWidget()
        self.info = ExpressionEditor()
        self.info.setObjectName('info')
        wupper.setObjectName('empty')
        layout.addWidget(wupper, 0, 0)
        layout.addWidget(self.dataview, 1, 0)
        layout.addLayout(self.info, 0, 1, 1, 1)

        self.setLayout(layout)

        self.dataview.clicked.connect(self.itemClicked)

    def itemClicked(self):
        data = self.datamodel.getData(self.dataview.currentIndex()).json()
        self.info.update(data)
        

class PerformanceTab(QWidget, Tab):

    def __init__(self, parent: Optional[QWidget] = None):
        super(PerformanceTab, self).__init__(parent)
        self.datamodel = ListModel(data=PerformanceTable())
        self.dataview = ListView()
        self.dataview.setup()
        self.dataview.setModel(self.datamodel)

        layout = QGridLayout()
        layout.setSpacing(0)
        layout = QGridLayout()
        layout.setSpacing(0)
        wupper = QWidget()
        wright = QWidget()
        wright.setObjectName('empty')
        wupper.setObjectName('empty')
        layout.addWidget(wupper, 0, 0)
        layout.addWidget(self.dataview, 1, 0)
        layout.addWidget(wright, 0, 1, 1, 1)

        self.setLayout(layout)


class View(QMainWindow):

    def __init__(self, parent=None) -> None:
        super(View, self).__init__(parent)

        layout = QGridLayout()

        expressions = ExpressionTab()
        performance = PerformanceTab()

        tabs = [
            (expressions, 'Expressions'),
            (performance, 'PerformanceMap')
        ]
        self.tab_view = TabView(self, tabs=tabs)
        layout.addWidget(self.tab_view, 0, 0)

        self.setWindowTitle('ANSYS CFX Post Processing')

        w = QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)

    def setup(self, **settings):
        self.resize(QtCore.QSize(*settings.get('size', [1280, 728])))
