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
from src.references.academics import *
from src.references.books import *
from src.references.technicals import *
from src.references.others import *


######################## CLASSES ########################
class SourceEditor(QWidget):
    returnClicked = pyqtSignal()
    tagChanged = pyqtSignal()
    typeChanged = pyqtSignal()
    fieldChanged = pyqtSignal()

    def __init__(self, path, sourceTag):
        super().__init__()
        self.currentDir = path
        self.generators = getGeneratorList()
        self.typeFieldsEditor = None
        self.goBackButton = None
        self.generalFieldsEditor = None
        self.sourceTag = sourceTag
        self.generated = False

    def initialize(self, fields):
        self.goBackButton = QPushButton('Go Back to Source List', self)
        self.goBackButton.clicked.connect(self.returnClicked.emit)
        self.generated = True
        self.generalFieldsEditor = GeneralFieldsEditor(self.currentDir, self.sourceTag, fields)
        self.generalFieldsEditor.fieldChanged.connect(self.fieldChanged.emit)
        self.generalFieldsEditor.tagChanged.connect(self.tagChanged.emit)
        self.typeFieldsEditor = self.generators[fields['TYPE']](self.currentDir, self.sourceTag, fields['FIELDS'])
        self.typeFieldsEditor.fieldChanged.connect(self.fieldChanged.emit)
        mainLayout = QGridLayout(self)
        mainLayout.addWidget(self.goBackButton, 0, 0, 1, 2)
        mainLayout.addWidget(self.generalFieldsEditor, 1, 0)
        mainLayout.addWidget(self.typeFieldsEditor, 1, 1)
        self.setLayout(mainLayout)


class GeneralFieldsEditor(QWidget):
    tagChanged = pyqtSignal()
    typeChanged = pyqtSignal()
    fieldChanged = pyqtSignal()

    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path
        self.settings = loadSettings('settings')
        themeFolder = 'dark-theme' if self.settings['DARK_THEME'] else 'light-theme'
        self.sourceTypes = {'ARTICLE': 'Article', 'BOOK': 'Book', 'BOOKLET': 'Booklet', 'CONFERENCE': 'Conference',
                            'INBOOK': 'InBook', 'INCOLLECTION': 'InCollection', 'INPROCEEDINGS': 'InProceedings',
                            'MANUAL': 'Manual', 'MASTERSTHESIS': 'MastersThesis', 'MISC': 'Misc', 'ONLINE': 'Online',
                            'PHDTHESIS': 'PhdThesis', 'PROCEEDINGS': 'Proceedings', 'STANDARD': 'Standard',
                            'TECHREPORT': 'TechReport', 'UNPUBLISHED': 'Unpublished', 'URL': 'URL'}
        # GENERAL FIELDS & LABELS
        self.tagLineEdit = QLineEdit(sourceTag)
        # self.tagLineEdit.setDisabled(True)
        self.tagLineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.tagLineEdit.textChanged.connect(self.changeTag)
        self.sourceTypeComboBox = QComboBox()
        self.sourceTypeComboBox.addItems(list(self.sourceTypes.values()))
        self.sourceTypeComboBox.setCurrentText(self.sourceTypes[fields['TYPE']])
        self.sourceTypeComboBox.setDisabled(True)   # TODO : Remove when type change works
        self.sourceTypeComboBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        tagLabel, typeLabel, accessLabel, descriptionLabel = QLabel("TAG:"), QLabel("TYPE:"), QLabel("ACCESS:"), QLabel("DESCRIPTION:")
        tagLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        typeLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        accessLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        descriptionLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # ACCESS STACKED WIDGET & COMBOBOX
        self.accessTypeComboBox = QComboBox()
        self.accessOptions = ['NONE', 'PDF', 'URL']
        self.accessTypeComboBox.addItems(self.accessOptions)
        self.accessTypeComboBox.setCurrentText(fields['ACCESS'])
        self.accessTypeComboBox.currentIndexChanged.connect(self._changeAccessType)
        self.accessTypeComboBox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.accessStackWidget = QStackedWidget()
        self.accessStackWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Pdf Widget and Layout
        pdfWidget = QWidget()
        pdfLayout = QHBoxLayout()
        self.pdfLineEdit = QLineEdit(fields['PDF'])
        self.pdfLineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.pdfButton = SquareIconButton(f'src/icons/{themeFolder}/icons8-file-explorer-96.png', self)
        self.pdfButton.clicked.connect(self._changePdfAccess)
        pdfLayout.addWidget(self.pdfLineEdit)
        pdfLayout.addWidget(self.pdfButton)
        pdfWidget.setLayout(pdfLayout)
        # Url Widget and Layout
        urlWidget = QWidget()
        urlLayout = QHBoxLayout()
        self.urlLineEdit = QLineEdit(fields['URL'])
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
        self.accessStackWidget.setCurrentIndex(self.accessOptions.index(fields['ACCESS']))
        # KEYWORDS WIDGET
        # self.keywordsWidget = TagWidget('Keywords :')
        # self.keywordsWidget.populateTags(self.fields['KEYWORDS'])
        # self.keywordsWidget.tagChange.connect(self.fieldChanged.emit)
        # DESCRIPTION EDIT
        self.descriptionEdit = QPlainTextEdit(fields['DESCRIPTION'])
        self.descriptionEdit.textChanged.connect(self._changeDescription)
        self.descriptionEdit.setWordWrapMode(QTextOption.WordWrap)
        self.descriptionEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # MAIN LAYOUT
        mainLayout = QGridLayout()
        mainLayout.addWidget(tagLabel, 0, 0)
        mainLayout.addWidget(self.tagLineEdit, 0, 1, 1, 2)
        mainLayout.addWidget(typeLabel, 1, 0)
        mainLayout.addWidget(self.sourceTypeComboBox, 1, 1)
        mainLayout.addWidget(accessLabel, 2, 0)
        mainLayout.addWidget(self.accessTypeComboBox, 2, 1)
        mainLayout.addWidget(self.accessStackWidget, 2, 2)
        mainLayout.addWidget(descriptionLabel, 3, 0)
        mainLayout.addWidget(self.descriptionEdit, 4, 0, 1, 3)
        self.setLayout(mainLayout)

    def changeTag(self):
        self.tagChanged.emit()

    def _changeAccessType(self):
        self.accessStackWidget.setCurrentIndex(self.accessTypeComboBox.currentIndex())
        self.fieldChanged.emit()

    def _changePdfAccess(self):
        defaultDir = self.pdfLineEdit.text()
        filePath, _ = QFileDialog.getOpenFileName(self, "Select PDF File", defaultDir, "PDF Files (*.pdf)")
        if os.path.exists(filePath):
            self.pdfLineEdit.setText(filePath)
            self.fieldChanged.emit()

    def _changeUrlAccess(self):
        self.fieldChanged.emit()

    def _changeKeywords(self):
        self.fieldChanged.emit()

    def _changeDescription(self):
        self.fieldChanged.emit()

    def openUrlAccess(self):
        if self.urlLineEdit.text():
            import webbrowser
            webbrowser.open(self.urlLineEdit.text())
        else:
            pass


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
