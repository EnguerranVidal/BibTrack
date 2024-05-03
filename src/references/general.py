import os
import json
import webbrowser
import pandas as pd

# ------------------- PyQt Modules -------------------- #
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# --------------------- Sources ----------------------- #
from src.common.utilities.fileSystem import loadSettings, saveSettings
from src.common.widgets.fields import GeneralFieldsEditor, SourceEditor
from src.common.widgets.widgets import SquareIconButton, IconButton
# References
from src.references.search import *
from src.references.academics import *
from src.references.books import *
from src.references.technicals import *
from src.references.others import *


######################## CLASSES ########################
class BibEditor(QWidget):
    change = pyqtSignal()

    def __init__(self, path, bibPath):
        super(QWidget, self).__init__()
        self.currentDir, self.bibPath = path, bibPath
        self.tracker = BibTracker(self.bibPath)
        self.settings = loadSettings('settings')
        self.editors = {}
        # SOURCE TABLE
        self.sourceStackedWidget = QStackedWidget(self)
        self.sourcesTable = QTableWidget()
        self.sourcesTable.setColumnCount(6)
        self.sourcesTable.setFrameStyle(QTableWidget.NoFrame)
        self.sourcesTable.verticalHeader().setVisible(False)
        self.sourcesTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.sourcesTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.sourcesTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.sourcesTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.sourcesTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.sourcesTable.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.sourcesTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.sourcesTable.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.sourcesTable.setHorizontalHeaderLabels(['NAME', 'TYPE', '', '', 'DESCRIPTION', ''])
        self.sourceStackedWidget.addWidget(self.sourcesTable)
        self.populateSourcesTable()
        # SEARCH BAR & SEARCH OPTIONS
        self.searchBar = SearchBar([], 5, parent=self)
        self.searchBar.toggleSearchingMode.connect(self.toggleSearchMode)
        self.searchBar.searchDone.connect(self.searchingTerm)
        self.searchComboBox = QComboBox()
        self.searchOptions = ['SEARCH BY ...', 'BIBTEX', 'KEYWORD', 'DESCRIPTION', 'FIELDS']
        self.searchComboBox.addItems(self.searchOptions)
        self.searchComboBox.setCurrentText(self.settings['SEARCH_BY'])
        self.searchComboBox.currentIndexChanged.connect(self.changeSearchOption)
        self.searchComboBox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # MAIN LAYOUT
        searchLayout = QHBoxLayout()
        searchLayout.addWidget(self.searchBar)
        searchLayout.addWidget(self.searchComboBox)
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(searchLayout)
        mainLayout.addWidget(self.sourceStackedWidget)
        self.setLayout(mainLayout)

    def populateSourcesTable(self):
        self.sourcesTable.setRowCount(0)
        for index, row in self.tracker.references.iterrows():
            self.addRow(row['TAG'], self.tracker.sources[row['TAG']])
        self.sourcesTable.itemSelectionChanged.connect(self.change.emit)

    def addRow(self, sourceTag, sourceDict):
        # Name & Type
        nameItem = QTableWidgetItem(sourceTag)
        typeItem = QTableWidgetItem(sourceDict['TYPE'])
        # Source Editor
        self.editors[sourceTag] = SourceEditor(self.currentDir)
        self.sourceStackedWidget.addWidget(self.editors[sourceTag])
        # Editor Button
        themeFolder = 'dark-theme' if self.settings['DARK_THEME'] else 'light-theme'
        editButton = IconButton(f'src/icons/{themeFolder}/icons8-edit-96.png', size=20)
        editButton.clicked.connect(lambda: self.sourceEdit(sourceTag))
        # Access Button
        if sourceDict['ACCESS'] == 'URL':
            accessButton = QPushButton('URL')
            accessButton.clicked.connect(self.sourceAccessOpen)
        elif sourceDict['ACCESS'] == 'PDF':
            accessButton = QPushButton('PDF')
            accessButton.clicked.connect(self.sourceAccessOpen)
        else:
            accessButton = QWidget()
        # Selecting Toggle
        debugToggle = QPushButton()
        debugToggle.setCheckable(True)
        debugToggle.setChecked(sourceDict['SELECTED'])
        debugToggle.clicked.connect(self.changeSelectedState)
        # DESCRIPTION ITEM
        descriptionItem = QTableWidgetItem(sourceDict['DESCRIPTION'])
        # Adding Items & Widgets to Table Row
        rowPosition = self.sourcesTable.rowCount()
        self.sourcesTable.insertRow(rowPosition)
        self.sourcesTable.setItem(rowPosition, 0, nameItem)
        self.sourcesTable.setItem(rowPosition, 1, typeItem)
        self.sourcesTable.setCellWidget(rowPosition, 2, editButton)
        self.sourcesTable.setCellWidget(rowPosition, 3, accessButton)
        self.sourcesTable.setItem(rowPosition, 4, descriptionItem)
        self.sourcesTable.setCellWidget(rowPosition, 5, debugToggle)

    def sourceAccessOpen(self):
        senderWidget: QPushButton = self.sender()
        row = self.sourcesTable.indexAt(senderWidget.pos()).row()
        item = self.sourcesTable.item(row, 0)
        sourceTag = item.text()
        if self.tracker.sources[sourceTag]['ACCESS'] == 'PDF':
            os.startfile(self.tracker.sources[sourceTag]['PDF'])
        if self.tracker.sources[sourceTag]['ACCESS'] == 'URL':
            webbrowser.open(self.tracker.sources[sourceTag]['URL'])

    def sourceEdit(self, sourceTag):
        if not self.editors[sourceTag].generated:
            self.editors[sourceTag].initialize(sourceTag, self.tracker.sources[sourceTag])
            self.editors[sourceTag].returnClicked.connect(self.goBackToSources)
            self.editors[sourceTag].typeFieldsEditor.fieldChanged.connect(lambda: self.sourceFieldChange(sourceTag))
            self.editors[sourceTag].generalFieldsEditor.fieldChanged.connect(lambda: self.sourceFieldChange(sourceTag))
        self.sourceStackedWidget.setCurrentWidget(self.editors[sourceTag])

    def goBackToSources(self):
        self.sourceStackedWidget.setCurrentIndex(0)

    def sourceFieldChange(self, sourceTag):
        # SOURCE TYPE FIELDS CHANGE
        self.tracker.sources[sourceTag]['FIELDS'] = self.editors[sourceTag].typeFieldsEditor.fields
        # GENERAL FIELDS CHANGE
        self.tracker.sources[sourceTag]['ACCESS'] = self.editors[
            sourceTag].generalFieldsEditor.accessTypeComboBox.currentText()
        self.tracker.sources[sourceTag]['PDF'] = self.editors[sourceTag].generalFieldsEditor.pdfLineEdit.text()
        self.tracker.sources[sourceTag]['URL'] = self.editors[sourceTag].generalFieldsEditor.urlLineEdit.text()
        self.tracker.sources[sourceTag]['DESCRIPTION'] = self.editors[
            sourceTag].generalFieldsEditor.descriptionEdit.toPlainText()
        # RESET ACCESS BUTTON
        for row in range(self.sourcesTable.rowCount()):
            item = self.sourcesTable.item(row, 0)  # Assuming you're searching in column 0
            if item is not None and item.text() == sourceTag:
                break
        if self.tracker.sources[sourceTag]['ACCESS'] == 'URL':
            accessButton = QPushButton('URL')
            accessButton.clicked.connect(self.sourceAccessOpen)
        elif self.tracker.sources[sourceTag]['ACCESS'] == 'PDF':
            accessButton = QPushButton('PDF')
            accessButton.clicked.connect(self.sourceAccessOpen)
        else:
            accessButton = QWidget()
        self.sourcesTable.setCellWidget(row, 3, accessButton)
        # CHANGE DESCRIPTION ITEM
        item = QTableWidgetItem(self.tracker.sources[sourceTag]['DESCRIPTION'])
        self.sourcesTable.setItem(row, 4, item)

    def changeSelectedState(self):
        senderWidget: QPushButton = self.sender()
        row = self.sourcesTable.indexAt(senderWidget.pos()).row()
        tags = list(self.tracker.sources.keys())
        self.tracker.sources[tags[row]]['SELECTED'] = senderWidget.isChecked()
        self.change.emit()

    def toggleSearchMode(self):
        if self.searchBar.searching:
            self.searchingTerm()
        else:
            for row in range(self.sourcesTable.rowCount()):
                self.sourcesTable.setRowHidden(row, False)

    def searchingTerm(self):
        results = self.searchInSources(self.searchBar.text())
        if self.searchComboBox.currentIndex() == 0:
            for row in range(self.sourcesTable.rowCount()):
                item = self.sourcesTable.item(row, 0)
                if item is not None and item.text() in results['ALL']:
                    self.sourcesTable.setRowHidden(row, False)
                else:
                    self.sourcesTable.setRowHidden(row, True)
        else:
            for row in range(self.sourcesTable.rowCount()):
                item = self.sourcesTable.item(row, 0)
                if item is not None and item.text() in results[self.searchComboBox.currentText()]:
                    self.sourcesTable.setRowHidden(row, False)
                else:
                    self.sourcesTable.setRowHidden(row, True)

    def changeSearchOption(self):
        self.settings['SEARCH_BY'] = self.searchComboBox.currentText()
        saveSettings(self.settings, 'settings')
        if self.searchBar.searching:
            self.searchingTerm()

    def searchInSources(self, terms):
        results = {'ALL': [], 'BIBTEX': [], 'DESCRIPTION': [], 'KEYWORD': [], 'FIELDS': []}
        for key, value in self.tracker.sources.items():
            for term in terms:
                if term.lower() in key.lower() or term.lower() == key.lower():
                    results['BIBTEX'].append(key)
                    if key not in results['ALL']:
                        results['ALL'].append(key)
            if 'FIELDS' in value and value['FIELDS']:
                for fieldKey, fieldValue in value['FIELDS'].items():
                    if isinstance(fieldValue, str):
                        for term in terms:
                            if term.lower() in fieldValue.lower():
                                results['FIELDS'].append(key)
                                if key not in results['ALL']:
                                    results['ALL'].append(key)
            if 'DESCRIPTION' in value and value['DESCRIPTION']:
                for term in terms:
                    if term.lower() in value['DESCRIPTION'].lower():
                        results['DESCRIPTION'].append(key)
                        if key not in results['ALL']:
                            results['ALL'].append(key)
            if 'KEYWORD' in value and value['KEYWORD']:
                for keyword in value['KEYWORD']:
                    for term in terms:
                        if term.lower() in keyword.lower():
                            results['KEYWORD'].append(key)
                            if key not in results['ALL']:
                                results['ALL'].append(key)
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

    def deleteSelectedRows(self):
        selectedRows = [item.row() for item in self.telecommandTable.selectedItems()]
        if len(selectedRows):
            selectedRows = sorted(list(set(selectedRows)))
            dialog = SourceDeletionMessageBox(selectedRows)
            result = dialog.exec_()
            if result == QMessageBox.Yes:
                for row in reversed(selectedRows):
                    self.sourcesTable.removeRow(row)
                    sourceTag = self.sourcesTable.item(row, 0).text()
                    self.tracker.removeSource(sourceTag)
                self.change.emit()


class NewBibTrackWindow(QDialog):
    def __init__(self, parent=None, bibTracks=None):
        super().__init__(parent)
        if bibTracks is None:
            bibTracks = []
        self.bibTracks = bibTracks
        self.setWindowTitle('Create New BibTrack')
        self.setModal(True)
        self.dataChanged = False
        self.saveChanged = False
        self.resize(400, 100)
        # NAME ENTRY & BUTTONS
        self.nameLabel = QLabel('BibTrack Name :')
        self.nameLineEdit = QLineEdit()
        self.nameLineEdit.textChanged.connect(self.updateOkButtonState)
        self.okButton = QPushButton('OK')
        self.okButton.setEnabled(False)
        self.cancelButton = QPushButton('Cancel')
        self.okButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)
        # LAYOUT
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.okButton)
        buttonLayout.addWidget(self.cancelButton)
        layout = QVBoxLayout(self)
        layout.addWidget(self.nameLabel)
        layout.addWidget(self.nameLineEdit)
        layout.addLayout(buttonLayout)

    def updateOkButtonState(self):
        name = self.nameLineEdit.text()
        validNewBibTrackName = bool(name) and name not in self.bibTracks
        self.okButton.setEnabled(validNewBibTrackName)


class NewSourceWindow(QDialog):
    def __init__(self, sourceType, parent=None, sourceTags=[]):
        super().__init__(parent)
        self.sourceTags = sourceTags
        self.setWindowTitle(f'Create New {sourceType}')
        self.setWindowIcon(QIcon('src/icons/PyStrato.png'))
        self.setModal(True)
        self.resize(400, 100)
        # NAME ENTRY & BUTTONS
        self.nameLabel = QLabel(f'{sourceType} BibTex Tag :')
        self.nameLineEdit = QLineEdit()
        self.nameLineEdit.textChanged.connect(self.updateOkButtonState)
        self.okButton = QPushButton('OK')
        self.okButton.setEnabled(False)
        self.cancelButton = QPushButton('Cancel')
        self.okButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)
        # LAYOUT
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.okButton)
        buttonLayout.addWidget(self.cancelButton)
        layout = QVBoxLayout(self)
        layout.addWidget(self.nameLabel)
        layout.addWidget(self.nameLineEdit)
        layout.addLayout(buttonLayout)

    def updateOkButtonState(self):
        name = self.nameLineEdit.text()
        validNewSourceName = bool(name) and name not in self.sourceTags
        self.okButton.setEnabled(validNewSourceName)


class SourceDeletionMessageBox(QMessageBox):
    def __init__(self, selectedRows):
        super().__init__()
        self.setModal(True)
        self.setIcon(QMessageBox.Question)
        self.setWindowTitle('Confirmation')
        self.setText(f'You are going to delete {len(selectedRows)} source(s).\n Do you want to proceed?')
        self.addButton(QMessageBox.Yes)
        self.addButton(QMessageBox.No)
        self.setDefaultButton(QMessageBox.No)


class BibTracker:
    def __init__(self, path):
        self.path = path
        self.sources = None
        self.refPath = os.path.join(path, 'references.csv')
        self.columns = ['TAG', 'TYPE']
        self.bibTexCategories = []
        if not os.path.exists(self.refPath):
            self._generateReferencesFile()
        else:
            self.references = pd.read_csv(self.refPath)
        self._loadSources()

    def _generateReferencesFile(self):
        self.references = pd.DataFrame(columns=self.columns)

    def addSource(self, tag, source):
        newReference = {'TAG': tag, 'TYPE': source['TYPE']}
        self.references = pd.concat([self.references, pd.DataFrame([newReference])], ignore_index=True)
        self.sources[tag] = source

    def removeSource(self, tag):
        del self.sources[tag]

    def _loadSources(self):
        self.sources = {}
        for index, row in self.references.iterrows():
            sourcePath = os.path.join(self.path, row['TAG'])
            with open(os.path.join(sourcePath, "info.json"), 'r') as file:
                self.sources[row['TAG']] = json.load(file)

    def saveState(self, path=None):
        self.path = self.path if path is None else path
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        for index, row in self.references.iterrows():
            sourcePath = os.path.join(self.path, row['TAG'])
            if not os.path.exists(sourcePath):
                os.mkdir(sourcePath)
            with open(os.path.join(sourcePath, "info.json"), 'w') as file:
                json.dump(self.sources[row['TAG']], file)
        self.references.to_csv(self.refPath, index=False)

    def unsavedChanges(self):
        bibTracker = BibTracker(self.path)
        return self != bibTracker

    def __eq__(self, other):
        if not isinstance(other, BibTracker):
            return False
        return self.sources == other.sources and self.references.equals(other.references)
