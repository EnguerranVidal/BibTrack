import os
import json
import webbrowser
import pandas as pd

# ------------------- PyQt Modules -------------------- #
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# --------------------- Sources ----------------------- #
from src.common.utilities.fileSystem import loadSettings
from src.common.widgets.fields import GeneralFieldsEditor
from src.common.widgets.widgets import SquareIconButton, IconButton
# References
from src.references.academics import *
from src.references.books import *
from src.references.technicals import *
from src.references.others import *


######################## CLASSES ########################
class ReferenceSearch(QWidget):
    def __init__(self, path):
        super().__init__()
        self.currentDir = path


class SearchBar(QLineEdit):
    searchDone = pyqtSignal()

    def __init__(self, searchOptions, maxSuggestions=5, parent=None):
        super(SearchBar, self).__init__(parent)
        self.selection = ''
        self.searchOptions = searchOptions
        self.maxSuggestions = maxSuggestions

        # LINE EDIT
        self.setPlaceholderText('Search Source ...')
        searchCompleter = QCompleter(self.searchOptions, self)
        searchCompleter.setCaseSensitivity(Qt.CaseInsensitive)
        searchCompleter.setFilterMode(Qt.MatchStartsWith)
        searchCompleter.setCompletionMode(QCompleter.PopupCompletion)
        searchCompleter.setMaxVisibleItems(self.maxSuggestions)
        self.setCompleter(searchCompleter)
        searchCompleter.activated.connect(self.onCompleterActivated)

        # SEARCH ACTION BUTTON
        self.searchButtonAction = QAction(self)
        self.settings = loadSettings('settings')
        themeFolder = 'dark-theme' if self.settings['DARK_THEME'] else 'light-theme'
        self.searchButtonAction.setIcon(QIcon(f'src/icons/{themeFolder}/icons8-search-96.png'))
        self.searchButtonAction.triggered.connect(self.performSearch)
        self.addAction(self.searchButtonAction, QLineEdit.TrailingPosition)

    def performSearch(self):
        if self.text() != '':
            closestSuggestion = self.completer().currentCompletion()
            self.selection = closestSuggestion
            self.searchDone.emit()
            QTimer.singleShot(0, self.clearLineEdit)

    def changeTheme(self):
        self.settings = loadSettings('settings')
        themeFolder = 'dark-theme' if self.settings['DARK_THEME'] else 'light-theme'
        self.searchButtonAction.setIcon(QIcon(f'src/icons/{themeFolder}/icons8-search-96.png'))

    def onCompleterActivated(self, text):
        self.selection = text
        self.searchDone.emit()
        QTimer.singleShot(0, self.clearLineEdit)

    def clearLineEdit(self):
        self.clear()
        self.setPlaceholderText('Search Location ...')

