import os
import json
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
class BibEditor(QTabWidget):
    change = pyqtSignal()

    def __init__(self, path, bibPath):
        super(QTabWidget, self).__init__()
        self.currentDir, self.bibPath = path, bibPath
        self.tracker = BibTracker(self.bibPath)
        self.settings = loadSettings('settings')
        self.editors = {}
        # SOURCE TABLE
        self.stackedWidget = QStackedWidget(self)
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
        self.stackedWidget.addWidget(self.sourcesTable)
        self.populateSourcesTable()
        self.stackedWidget.setCurrentIndex(0)
        # MAIN TABS
        self.addTab(self.stackedWidget, "SOURCES")
        self.addTab(QWidget(), "COMPLETION")

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
        self.stackedWidget.addWidget(self.editors[sourceTag])
        # Editor Button
        themeFolder = 'dark-theme' if self.settings['DARK_THEME'] else 'light-theme'
        editButton = IconButton(f'src/icons/{themeFolder}/icons8-edit-96.png', size=20)
        editButton.clicked.connect(lambda: self.sourceEdit(sourceTag))
        # Selecting Toggle
        debugToggle = QPushButton()
        debugToggle.setCheckable(True)
        debugToggle.setChecked(sourceDict['SELECTED'])
        debugToggle.clicked.connect(self.changeSelectedState)
        # Adding Items & Widgets to Table Row
        rowPosition = self.sourcesTable.rowCount()
        self.sourcesTable.insertRow(rowPosition)
        self.sourcesTable.setItem(rowPosition, 0, nameItem)
        self.sourcesTable.setItem(rowPosition, 1, typeItem)
        self.sourcesTable.setCellWidget(rowPosition, 2, editButton)
        self.sourcesTable.setCellWidget(rowPosition, 5, debugToggle)

    def sourceEdit(self, sourceTag):
        sourceEditor = self.editors[sourceTag]
        if not sourceEditor.generated:
            sourceEditor.initialize(sourceTag, self.tracker.sources[sourceTag])
            sourceEditor.returnClicked.connect(self.goBackToSources)
        self.stackedWidget.setCurrentWidget(sourceEditor)

    def goBackToSources(self):
        self.stackedWidget.setCurrentIndex(0)

    def changeSelectedState(self):
        senderWidget: QPushButton = self.sender()
        row = self.sourcesTable.indexAt(senderWidget.pos()).row()
        tags = list(self.tracker.sources.keys())
        self.tracker.sources[tags[row]]['SELECTED'] = senderWidget.isChecked()
        self.change.emit()


class SourceEditor(QWidget):
    returnClicked = pyqtSignal()

    def __init__(self, path):
        super().__init__()
        self.currentDir = path
        self.generators = getGeneratorList()
        self.typeFieldsEditor = None
        self.goBackButton = None
        self.generalFieldsEditor = None
        self.sourceTag, self.fields = None, None
        self.generated = False

    def initialize(self, sourceTag, fields):
        self.goBackButton = QPushButton('Go Back to Source List', self)
        self.goBackButton.clicked.connect(self.returnClicked.emit)
        self.sourceTag, self.fields = sourceTag, fields
        self.generated = True
        self.generalFieldsEditor = GeneralFieldsEditor(self.currentDir, sourceTag, fields)
        self.typeFieldsEditor = self.generators[fields['TYPE']](self.currentDir, sourceTag, fields)
        mainLayout = QGridLayout(self)
        mainLayout.addWidget(self.goBackButton, 0, 0, 1, 2)
        mainLayout.addWidget(self.generalFieldsEditor, 1, 0)
        mainLayout.addWidget(self.typeFieldsEditor, 1, 1)
        self.setLayout(mainLayout)


class NewBibTrackWindow(QDialog):
    def __init__(self, parent=None, bibTracks=[]):
        super().__init__(parent)
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


######################## FUNCTIONS ########################
def getGeneratorList():
    generators = {'ARTICLE': createArticleEditor, 'BOOK': createBookEditor, 'BOOKLET': createBookletEditor,
                  'CONFERENCE': createConferenceEditor, 'INBOOK': createInBookEditor,
                  'INCOLLECTION': createInCollectionEditor, 'INPROCEEDINGS': createInProceedingsEditor,
                  'MANUAL': createManualEditor, 'MASTERSTHESIS': createMastersThesisEditor,
                  'MISC': createMiscEditor, 'ONLINE': createOnlineEditor, 'PHDTHESIS': createPhdThesisEditor,
                  'PROCEEDINGS': createProceedingsEditor, 'STANDARD': createStandardEditor,
                  'TECHREPORT': createTechReportEditor, 'UNPUBLISHED': createUnpublishedEditor,
                  'URL': createUrlEditor}
    return generators
