import os
import json
import PyPDF2
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
        # RESULTS TABLES
        self.allResults = QTableWidget()
        self.tagResults = QTableWidget()
        self.keywordsResults = QTableWidget()
        self.descriptionResults = QTableWidget()
        self.fieldsResults = QTableWidget()
        # STACKED WIDGET & NO RESULT PAGE
        self.mainStackedWidget = QStackedWidget(self)
        self.noResultsLabel = NoSourcesDisplay(self)
        self.resultsPage = QTabWidget(self)
        self.mainStackedWidget.addWidget(self.noResultsLabel)
        self.mainStackedWidget.addWidget(self.resultsPage)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.mainStackedWidget)
        self.setLayout(mainLayout)

    def clearResults(self):
        self.resultsPage.clear()
        self.allResults.clearContents()
        self.allResults.setRowCount(0)
        self.tagResults.clearContents()
        self.tagResults.setRowCount(0)
        self.keywordsResults.clearContents()
        self.keywordsResults.setRowCount(0)
        self.descriptionResults.clearContents()
        self.descriptionResults.setRowCount(0)
        self.fieldsResults.clearContents()
        self.fieldsResults.setRowCount(0)

    def searchInSources(self, sources, searchedText):
        self.clearResults()
        results = self.searchFromTerms(sources, searchedText.split())
        if not any(results.values()):
            self.mainStackedWidget.setCurrentIndex(0)
        else:
            self.mainStackedWidget.setCurrentIndex(1)
            # ADDING TABS FOR EACH CATEGORY BASED ON RESULTS
            self.resultsPage.addTab(self.allResults, 'ALL')
            self.populateAllResults(results)
            if results['KEYWORDS']:
                self.resultsPage.addTab(self.keywordsResults, 'KEYWORDS')
                self.populateKeywordsResults(results)
            if results['DESCRIPTION']:
                self.resultsPage.addTab(self.descriptionResults, 'DESCRIPTIONS')
                self.populateDescriptionsResults(results)
            if results['TAG']:
                self.resultsPage.addTab(self.tagResults, 'TAGS')
                self.populateTagsResults(results)
            if results['FIELDS']:
                self.resultsPage.addTab(self.fieldsResults, 'FIELDS')
                self.populateFieldsResults(results)


class SearchBar(QLineEdit):
    searchDone = pyqtSignal()
    toggleSearchingMode = pyqtSignal()

    def __init__(self, searchOptions, maxSuggestions=5, parent=None):
        super(SearchBar, self).__init__(parent)
        self.searchOptions = searchOptions
        self.maxSuggestions = maxSuggestions
        self.searching = False  # Track searching state

        # LINE EDIT COMPLETER
        self.setPlaceholderText('Search Source ...')
        searchCompleter = QCompleter(self.searchOptions, self)
        searchCompleter.setCaseSensitivity(Qt.CaseInsensitive)
        searchCompleter.setFilterMode(Qt.MatchStartsWith)
        searchCompleter.setCompletionMode(QCompleter.PopupCompletion)
        searchCompleter.setMaxVisibleItems(self.maxSuggestions)
        self.setCompleter(searchCompleter)
        searchCompleter.activated.connect(self.performSearch)

        # SEARCH ACTION BUTTON
        self.searchButtonAction = QAction(self)
        self.settings = loadSettings('settings')
        themeFolder = 'dark-theme' if self.settings['DARK_THEME'] else 'light-theme'
        self.searchButtonAction.setIcon(QIcon(f'src/icons/{themeFolder}/icons8-search-96.png'))
        self.searchButtonAction.triggered.connect(self.toggleSearchState)
        self.addAction(self.searchButtonAction, QLineEdit.TrailingPosition)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.performSearch(self.text)
        else:
            super().keyPressEvent(event)

    def changeSearchOptions(self, options):
        self.searchOptions = options
        searchCompleter = QCompleter(self.searchOptions, self)
        searchCompleter.setCaseSensitivity(Qt.CaseInsensitive)
        searchCompleter.setFilterMode(Qt.MatchStartsWith)
        searchCompleter.setCompletionMode(QCompleter.PopupCompletion)
        searchCompleter.setMaxVisibleItems(self.maxSuggestions)
        self.setCompleter(searchCompleter)
        searchCompleter.activated.connect(self.performSearch)

    def toggleSearchState(self):
        if self.searching:
            themeFolder = 'dark-theme' if self.settings['DARK_THEME'] else 'light-theme'
            self.searchButtonAction.setIcon(QIcon(f'src/icons/{themeFolder}/icons8-search-96.png'))
            self.searching = False
            self.textChanged.disconnect(self.textCheck)
            self.clearLineEdit()
        else:
            themeFolder = 'dark-theme' if self.settings['DARK_THEME'] else 'light-theme'
            self.searchButtonAction.setIcon(QIcon(f'src/icons/{themeFolder}/icons8-close-96.png'))
            self.searching = True
            self.textChanged.connect(self.textCheck)
        self.toggleSearchingMode.emit()

    def performSearch(self, text):
        if self.searching:
            if text:
                self.searchDone.emit()
            else:
                self.toggleSearchState()
        else:
            if text:
                self.toggleSearchState()

    def textCheck(self, text):
        if self.searching and not text:
            self.toggleSearchState()

    def changeTheme(self):
        self.settings = loadSettings('settings')
        themeFolder = 'dark-theme' if self.settings['DARK_THEME'] else 'light-theme'
        self.searchButtonAction.setIcon(QIcon(f'src/icons/{themeFolder}/icons8-search-96.png'))

    def clearLineEdit(self):
        self.clear()
        self.setPlaceholderText('Search Source ...')
