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
        terms = searchedText.split()
        results = self.searchFromTerms(sources, terms)
        hasResults = any(results.values())
        print(results)
        if not hasResults:
            self.mainStackedWidget.setCurrentIndex(0)
        else:
            self.mainStackedWidget.setCurrentIndex(1)
            # ADDING TABS FOR EACH CATEGORY BASED ON RESULTS
            self.resultsPage.addTab(self.allResults, 'ALL')
            if results['KEYWORDS']:
                self.resultsPage.addTab(self.keywordsResults, 'KEYWORDS')
            if results['DESCRIPTION']:
                self.resultsPage.addTab(self.descriptionResults, 'DESCRIPTIONS')
            if results['TAG']:
                self.resultsPage.addTab(self.tagResults, 'TAGS')
            if results['FIELDS']:
                self.resultsPage.addTab(self.fieldsResults, 'FIELDS')

    @staticmethod
    def searchFromTerms(sources, terms):
        results = {'TAG': [], 'DESCRIPTION': [], 'KEYWORDS': [], 'FIELDS': []}
        for key, value in sources.items():
            for term in terms:
                if term.lower() in key.lower() or term.lower() == key.lower():
                    results['TAG'].append(key)
            if 'FIELDS' in value and value['FIELDS']:
                for fieldKey, fieldValue in value['FIELDS'].items():
                    pass

            # for fieldKey, fieldValue in value['FIELDS'].items():
            #     if isinstance(fieldValue, str):
            #         for term in terms:
            #             if term.lower() in fieldValue.lower():
            #                 results[fieldKey].append(key)
            #     elif isinstance(fieldValue, list):
            #         for item in fieldValue:
            #             if term.lower() in item.lower():
            #                 results[fieldKey].append(key)
            if 'DESCRIPTION' in value and value['DESCRIPTION']:
                for term in terms:
                    if term.lower() in value['DESCRIPTION'].lower():
                        results['DESCRIPTION'].append(key)
            if 'KEYWORDS' in value and value['KEYWORDS']:
                for keyword in value['KEYWORDS']:
                    for term in terms:
                        if term.lower() in keyword.lower():
                            results['KEYWORDS'].append(key)
            # if value['ACCESS'] == 'PDF' and value['PDF']:
            #     results['PDF'] = {}
            #     termCounts = {}
            #     with open(value['PDF'], 'rb') as pdf_file:
            #         pdfReader = PyPDF2.PdfReader(pdf_file)
            #         for pageNum in range(len(pdfReader.pages)):
            #             pageText = pdfReader.pages[pageNum].extract_text()
            #             for term in terms:
            #                 termCount = pageText.lower().count(term.lower())
            #                 if termCount > 0:
            #                     if term not in termCounts:
            #                         termCounts[term] = termCount
            #                     else:
            #                         termCounts[term] += termCount
            #     results['PDF'][key] = termCounts
        return results


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


class NoSourcesDisplay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        font = QFont()
        font.setPointSize(16)
        self.messageLabel = QLabel('NO RESULTS')
        self.messageLabel.setAlignment(Qt.AlignCenter)
        self.messageLabel.setFont(font)
        # MAIN LAYOUT
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.messageLabel, alignment=Qt.AlignCenter)
        mainLayout.setSpacing(0)
        self.setLayout(mainLayout)
