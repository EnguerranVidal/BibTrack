import os
import json
import pandas as pd

# ------------------- PyQt Modules -------------------- #
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


# --------------------- Sources ----------------------- #

######################## CLASSES ########################
class BibEditor(QWidget):
    def __init__(self, path):
        super(QWidget, self).__init__()

        self.bibPath = path
        self.tracker = BibTracker(self.bibPath)
        self.topLabel = QLabel(os.path.basename(self.bibPath))

        # SOURCE TABS
        self.sourceTabs = QTabWidget()
        self.sourceTabs.addTab(QWidget(), "BOOKS")
        self.sourceTabs.addTab(QWidget(), "Tab 2")

        layout = QVBoxLayout()
        layout.addWidget(self.topLabel)
        layout.addWidget(self.sourceTabs)
        self.setLayout(layout)


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
        self.sources = {}
        for index, row in self.references.iterrows():
            sourcePath = os.path.join(self.path, row['TAG'])
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
