######################## IMPORTS ########################
import os.path

# ------------------- PyQt Modules -------------------- #
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *

# --------------------- Sources ----------------------- #
from src.common.utilities.fileSystem import loadSettings, saveSettings


######################## CLASSES ########################
class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About")
        # ABOUT TEXT EDIT
        aboutText = """
        <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>About BibTrack</title>
    </head>
    <body>
        <h1>About BibTrack</h1>
        <p>
            BibTrack is a powerful and intuitive bibliography management tool designed to streamline the organization of sources for your academic pursuits, whether it's a PhD thesis, research paper, or any documentation project. With its user-friendly interface and robust features, BibTrack simplifies the process of managing and tracking your sources, allowing you to focus more on your research and less on administrative tasks.
        </p>
        <h2>Key Features:</h2>
        <ul>
            <li><strong>Effortless Source Management:</strong> Easily add, edit, and categorize your sources, including texts, books, articles, websites, and more. BibTrack provides a centralized hub for all your references, ensuring easy access and retrieval whenever you need them.</li>
            <li><strong>Comprehensive Metadata:</strong> Capture essential metadata for each source, including title, author(s), publication year, keywords, description, and notes. This detailed information enables you to quickly locate and reference your sources with precision.</li>
            <li><strong>BibTeX Export Compatibility:</strong> Seamlessly export your bibliography in BibTeX format, ensuring compatibility with popular LaTeX editors and reference management software. BibTrack empowers you to integrate your sources seamlessly into your academic documents, enhancing the efficiency and accuracy of your writing process.</li>
            <li><strong>Progress Tracking:</strong> Stay organized and on track with BibTrack's progress tracking feature. Monitor your reading progress, set completion goals, and track your overall progress towards completing your sources. BibTrack helps you stay accountable and motivated throughout your research journey.</li>
        </ul>
        <p>
            BibTrack is proudly crafted by <a href='https://github.com/EnguerranVidal'>Enguerran Vidal</a>. Whether you're a seasoned academic or a budding researcher, BibTrack is your trusted companion for managing your bibliography with ease and efficiency. Experience the convenience and productivity of BibTrack today and elevate your research to new heights.
        </p>
    </body>
    </html>
        """
        testEdit = ExternalLinkTextEdit()
        testEdit.setReadOnly(True)
        testEdit.setTextInteractionFlags(Qt.TextBrowserInteraction)
        testEdit.setHtml(aboutText)
        testEdit.setFixedWidth(400)
        testEdit.setFixedHeight(500)
        doneButt = QPushButton("Done")
        doneButt.clicked.connect(self.accept)
        # MAIN LAYOUT
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(testEdit)
        self.layout.addWidget(doneButt)


class ExternalLinkTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super(QTextEdit, self).__init__(parent)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            anchor = self.anchorAt(event.pos())
            if anchor:
                QDesktopServices.openUrl(QUrl(anchor))
            else:
                super().mousePressEvent(event)
        else:
            super().mousePressEvent(event)


class IconButton(QPushButton):
    def __init__(self, icon: str, parent=None, size=25):
        super(IconButton, self).__init__(parent)
        self.iconPath = icon
        self.setIcon(QIcon(self.iconPath))
        self.setIconSize(QSize(size, size))


class SquareIconButton(QPushButton):
    def __init__(self, icon: str, parent=None, size=25, flat=False, centered=False):
        super(SquareIconButton, self).__init__(parent)
        self.iconPath = icon
        self.setIcon(QIcon(self.iconPath))
        self.setIconSize(QSize(size, size))
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Style Sheet
        margin = (size - 20) // 2
        styleSheet = 'QPushButton { text-align: center; padding: 0px; }'
        if flat:
            styleSheet += 'QPushButton { border: none; }'
        if centered:
            styleSheet += f'QPushButton {{ margin-left: {margin}px; margin-right: {margin}px; }}'

        self.setStyleSheet(styleSheet)
        self.setAutoFillBackground(False)

    def setIconSize(self, size):
        super().setIconSize(size)
        self.setFixedSize(size)

    def sizeHint(self):
        return self.iconSize()


class GeneralFieldsEditor(QWidget):
    tagChanged = pyqtSignal()
    pdfChanged = pyqtSignal()
    urlChanged = pyqtSignal()
    accessTypeChanged = pyqtSignal()
    typeChanged = pyqtSignal()
    returnClicked = pyqtSignal()

    def __init__(self, sourceTag, fields):
        super().__init__()
        self.settings = loadSettings('settings')
        themeFolder = 'dark-theme' if self.settings['DARK_THEME'] else 'light-theme'
        self.sourceTypes = {'ARTICLE': 'Article', 'BOOK': 'Book', 'BOOKLET': 'Booklet', 'CONFERENCE': 'Conference',
                            'INBOOK': 'InBook', 'INCOLLECTION': 'InCollection', 'INPROCEEDINGS': 'InProceedings',
                            'MANUAL': 'Manual', 'MASTERSTHESIS': 'MastersThesis', 'MISC': 'Misc', 'ONLINE': 'Online',
                            'PHDTHESIS': 'PhdThesis', 'PROCEEDINGS': 'Proceedings', 'STANDARD': 'Standard',
                            'TECHREPORT': 'TechReport', 'UNPUBLISHED': 'Unpublished', 'URL': 'URL'}
        # GO BACK BUTTON
        self.goBackButton = QPushButton('Go Back to Source List', self)
        self.goBackButton.clicked.connect(self.returnClicked.emit)
        # GENERAL FIELDS
        self.tagLineEdit = QLineEdit(sourceTag)
        self.sourceTypeComboBox = QComboBox()
        self.sourceTypeComboBox.addItems(list(self.sourceTypes.values()))
        self.sourceTypeComboBox.setCurrentText(self.sourceTypes[fields['TYPE']])
        self.accessTypeComboBox = QComboBox()
        self.accessOptions = ['NONE', 'PDF', 'URL']
        self.accessTypeComboBox.addItems(self.accessOptions)
        self.accessTypeComboBox.setCurrentText(fields['ACCESS'])
        self.accessTypeComboBox.currentIndexChanged.connect(self.changeAccessType)
        # ACCESS STACKED WIDGET
        self.accessStackWidget = QStackedWidget()
        # Pdf Widget and Layout
        pdfWidget = QWidget()
        pdfLayout = QHBoxLayout()
        self.pdfLineEdit = QLineEdit(fields['PDF'])
        self.pdfLineEdit.textChanged.connect(self.pdfChanged.emit)
        self.pdfButton = SquareIconButton(f'src/icons/{themeFolder}/icons8-file-explorer-96.png', self)
        self.pdfButton.clicked.connect(self.changePdfAccess)
        pdfLayout.addWidget(self.pdfLineEdit)
        pdfLayout.addWidget(self.pdfButton)
        pdfWidget.setLayout(pdfLayout)
        # Url Widget and Layout
        urlWidget = QWidget()
        urlLayout = QHBoxLayout()
        self.urlLineEdit = QLineEdit(fields['URL'])
        self.urlLineEdit.textChanged.connect(self.urlChanged.emit)
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

        # MAIN LAYOUT
        tagTypeLayout = QHBoxLayout()
        tagTypeLayout.addWidget(self.tagLineEdit)
        tagTypeLayout.addWidget(self.sourceTypeComboBox)
        refAccessLayout = QHBoxLayout()
        refAccessLayout.addWidget(self.accessTypeComboBox)
        refAccessLayout.addWidget(self.accessStackWidget)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.goBackButton)
        mainLayout.addLayout(tagTypeLayout)
        mainLayout.addLayout(refAccessLayout)
        self.setLayout(mainLayout)

    def changeAccessType(self):
        self.accessStackWidget.setCurrentIndex(self.accessTypeComboBox.currentIndex())
        self.accessTypeChanged.emit()

    def changePdfAccess(self):
        defaultDir = self.pdfLineEdit.text()
        filePath, _ = QFileDialog.getOpenFileName(self, "Select PDF File", defaultDir, "PDF Files (*.pdf)")
        if os.path.exists(filePath):
            self.pdfLineEdit.setText(filePath)

    def openUrlAccess(self):
        if self.urlLineEdit.text():
            import webbrowser
            webbrowser.open(self.urlLineEdit.text())
        else:
            pass
