from __future__ import annotations

from abc import abstractmethod
from typing import Any, Union, Optional, Sequence, TypeVar

from PySide6.QtWidgets import (
    QWidget, QListView,
    QDialog, QLineEdit, QTabWidget,
    QGridLayout, QAbstractScrollArea
)
from PySide6.QtCore import (
    Qt, QAbstractListModel, QModelIndex,
    QPersistentModelIndex, QSize
)
from PySide6 import QtCore, QtGui


class AbstractWidget(QWidget):

    def __init__(self, parent: Optional[QWidget]=None) -> None:
        super().__init__(parent)

    @abstractmethod
    def setup(self, **settings) -> bool:
        pass

    @abstractmethod
    def update(sefl, **settings) -> bool:
        pass
    
    @abstractmethod
    def data(self) -> Any:
        pass


class AbstractEditor(QDialog):

    def __init__(self, parent: Optional[QWidget]=None, f: Qt.WindowType=Qt.WindowType.Dialog) -> None:
        super().__init__(parent, f)
        self.setObjectName('editor')
        self.editor = QLineEdit()
        self.editor.setObjectName('editor')

        layout = QGridLayout()
        layout.addWidget(self.editor)
        self.setLayout(layout)

    def setup(self, **settings):
        self.editor.clear()
        self.editor.setPlaceholderText(settings.get('placeholder', ''))
        self.editor.setText(settings.get('text', ''))


class ListModel(QAbstractListModel):

    def __init__(self, data: Any) -> None:
        super(ListModel, self).__init__()
        self._data = data
        self.editor = AbstractEditor()

    def data(self, index: Union[QModelIndex, QPersistentModelIndex], role: int = ...) -> Any:

        if role == Qt.ItemDataRole.DisplayRole:
            if not index.isValid() : return None
            if not 0 <= index.row() <= len(self._data.data()) : return None
            return str(self._data.get(index.row()))

        if role == Qt.ItemDataRole.ToolTipRole:
            return self._data.get(index.row()).tooltip

        if role == Qt.ItemDataRole.EditRole:
            self.editor.show()

    def flags(self, index: Union[QModelIndex, QPersistentModelIndex]) -> Qt.ItemFlag:
        
        if not index.isValid() : return Qt.ItemFlag.ItemIsEnabled
        return Qt.ItemFlags(QAbstractListModel.flags(self, index) | Qt.ItemFlag.ItemIsEditable)

    def rowCount(self, index: Union[QModelIndex, QPersistentModelIndex]) -> int:
        return len(self._data.view())
