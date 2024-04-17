######################## IMPORTS ########################
import os.path

# ------------------- PyQt Modules -------------------- #
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *

# --------------------- Sources ----------------------- #
from src.common.utilities.fileSystem import loadSettings, saveSettings
from src.common.widgets.widgets import SquareIconButton


######################## CLASSES ########################
class GeneralFieldsEditor(QWidget):
    tagChanged = pyqtSignal()
    typeChanged = pyqtSignal()
    fieldsChanged = pyqtSignal()

    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path
        self.settings = loadSettings('settings')
        self.sourceTag, self.fields = sourceTag, fields
        themeFolder = 'dark-theme' if self.settings['DARK_THEME'] else 'light-theme'
        self.sourceTypes = {'ARTICLE': 'Article', 'BOOK': 'Book', 'BOOKLET': 'Booklet', 'CONFERENCE': 'Conference',
                            'INBOOK': 'InBook', 'INCOLLECTION': 'InCollection', 'INPROCEEDINGS': 'InProceedings',
                            'MANUAL': 'Manual', 'MASTERSTHESIS': 'MastersThesis', 'MISC': 'Misc', 'ONLINE': 'Online',
                            'PHDTHESIS': 'PhdThesis', 'PROCEEDINGS': 'Proceedings', 'STANDARD': 'Standard',
                            'TECHREPORT': 'TechReport', 'UNPUBLISHED': 'Unpublished', 'URL': 'URL'}
        # GENERAL FIELDS & LABELS
        self.tagLineEdit = QLineEdit(self.sourceTag)
        self.tagLineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.sourceTypeComboBox = QComboBox()
        self.sourceTypeComboBox.addItems(list(self.sourceTypes.values()))
        self.sourceTypeComboBox.setCurrentText(self.sourceTypes[self.fields['TYPE']])
        self.sourceTypeComboBox.setDisabled(True)   # TODO : Remove when type change works
        self.sourceTypeComboBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        tagLabel, typeLabel, accessLabel, descriptionLabel = QLabel("Tag:"), QLabel("Type:"), QLabel("Access:"), QLabel("Description:")
        tagLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        typeLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        accessLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        descriptionLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # ACCESS STACKED WIDGET & COMBOBOX
        self.accessTypeComboBox = QComboBox()
        self.accessOptions = ['NONE', 'PDF', 'URL']
        self.accessTypeComboBox.addItems(self.accessOptions)
        self.accessTypeComboBox.setCurrentText(self.fields['ACCESS'])
        self.accessTypeComboBox.currentIndexChanged.connect(self._changeAccessType)
        self.accessTypeComboBox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.accessStackWidget = QStackedWidget()
        self.accessStackWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Pdf Widget and Layout
        pdfWidget = QWidget()
        pdfLayout = QHBoxLayout()
        self.pdfLineEdit = QLineEdit(self.fields['PDF'])
        self.pdfLineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.pdfButton = SquareIconButton(f'src/icons/{themeFolder}/icons8-file-explorer-96.png', self)
        self.pdfButton.clicked.connect(self._changePdfAccess)
        pdfLayout.addWidget(self.pdfLineEdit)
        pdfLayout.addWidget(self.pdfButton)
        pdfWidget.setLayout(pdfLayout)
        # Url Widget and Layout
        urlWidget = QWidget()
        urlLayout = QHBoxLayout()
        self.urlLineEdit = QLineEdit(self.fields['URL'])
        self.urlLineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.urlLineEdit.textChanged.connect(self._changeUrlAccess)
        self.urlButton = SquareIconButton(f'src/icons/{themeFolder}/icons8-globe-96.png', self)
        self.urlButton.clicked.connect(self.openUrlAccess)
        urlLayout.addWidget(self.urlLineEdit)
        urlLayout.addWidget(self.urlButton)
        urlWidget.setLayout(urlLayout)
        # Adding Widgets
        self.accessStackWidget.addWidget(QWidget())
        self.accessStackWidget.addWidget(pdfWidget)
        self.accessStackWidget.addWidget(urlWidget)
        self.accessStackWidget.setCurrentIndex(self.accessOptions.index(self.fields['ACCESS']))
        # KEYWORDS WIDGET
        # self.keywordsWidget = TagWidget('Keywords :')
        # self.keywordsWidget.populateTags(self.fields['KEYWORDS'])
        # self.keywordsWidget.tagChange.connect(self.fieldsChanged.emit)
        # DESCRIPTION EDIT
        self.descriptionEdit = QLineEdit(self.fields['DESCRIPTION'])
        self.descriptionEdit.textChanged.connect(self._changeDescription)
        self.descriptionEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # MAIN LAYOUT
        mainLayout = QGridLayout()
        mainLayout.addWidget(tagLabel, 0, 0)
        mainLayout.addWidget(self.tagLineEdit, 0, 1, 1, 2)
        mainLayout.addWidget(typeLabel, 1, 0)
        mainLayout.addWidget(self.sourceTypeComboBox, 1, 1)
        mainLayout.addWidget(accessLabel, 2, 0)
        mainLayout.addWidget(self.accessTypeComboBox, 2, 1)
        mainLayout.addWidget(self.accessStackWidget, 2, 2)  # Access stack widget spans two columns
        mainLayout.addWidget(descriptionLabel, 3, 0)
        mainLayout.addWidget(self.descriptionEdit, 4, 0, 1, 3)
        self.setLayout(mainLayout)

    def _changeAccessType(self):
        self.accessStackWidget.setCurrentIndex(self.accessTypeComboBox.currentIndex())
        self.fields['ACCESS'] = self.accessTypeComboBox.currentText()
        self.fieldsChanged.emit()

    def _changePdfAccess(self):
        defaultDir = self.pdfLineEdit.text()
        filePath, _ = QFileDialog.getOpenFileName(self, "Select PDF File", defaultDir, "PDF Files (*.pdf)")
        if os.path.exists(filePath):
            self.pdfLineEdit.setText(filePath)
            self.fields['PDF'] = filePath
            self.fieldsChanged.emit()

    def _changeUrlAccess(self):
        self.fields['URL'] = self.urlLineEdit.text()
        self.fieldsChanged.emit()

    def _changeKeywords(self):
        self.fields['KEYWORDS'] = self.keywordsWidget.tagTexts
        self.fieldsChanged.emit()

    def _changeDescription(self):
        self.fields['DESCRIPTION'] = self.descriptionEdit.text()
        self.fieldsChanged.emit()

    def openUrlAccess(self):
        if self.urlLineEdit.text():
            import webbrowser
            webbrowser.open(self.urlLineEdit.text())
        else:
            pass


class MonthComboBox(QComboBox):
    def __init__(self, inputMonth: str):
        super().__init__()
        self.months = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        self.addItems(self.months)
        inMonths = [month.lower() for month in self.months]
        abbreviations = [month[:3].lower() for month in self.months]
        if inputMonth.lower() in inMonths:
            self.setCurrentText(self.months[inMonths.index(inputMonth.lower())])
        elif inputMonth.lower() in abbreviations:
            self.setCurrentText(self.months[abbreviations.index(inputMonth.lower())])
        else:
            self.setCurrentText('')


class EditionComboBox(QComboBox):
    def __init__(self, inputEdition: str):
        super().__init__()
        self.editions = ['', 'First', 'Second', 'Third', 'Fourth', 'Fifth', 'Sixth', 'Seventh', 'Eight', 'Ninth', 'Tenth']
        self.addItems(self.editions)
        inEditions = [edition.lower() for edition in self.editions]
        abbreviations = [edition[:3].lower() for edition in self.editions]
        if inputEdition.lower() in inEditions:
            self.setCurrentText(self.editions[inEditions.index(inputEdition.lower())])
        elif inputEdition.lower() in abbreviations:
            self.setCurrentText(self.editions[abbreviations.index(inputEdition.lower())])
        else:
            self.setCurrentText('')