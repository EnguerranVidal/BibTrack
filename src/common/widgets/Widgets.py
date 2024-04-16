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


class TagWidget(QWidget):
    tagChange = pyqtSignal()

    def __init__(self, title):
        super(TagWidget, self).__init__()
        self.tagTexts, self.tagWidgets = [], []
        # TAGS INPUT LINE EDIT
        self.titleLabel = QLabel(title)
        self.inputLineEdit = QLineEdit()
        self.inputLineEdit.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.inputLineEdit.returnPressed.connect(self.inputTags)
        # LISTING WIDGET
        self.listingWidget = ResizableListingWidget()

        # MAIN LAYOUT
        upperLayout = QHBoxLayout()
        upperLayout.addWidget(self.titleLabel)
        upperLayout.addWidget(self.inputLineEdit)
        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(4)
        mainLayout.addLayout(upperLayout)
        mainLayout.addWidget(self.listingWidget)
        self.setLayout(mainLayout)
        self.show()

    def inputTags(self):
        newTags = self.inputLineEdit.text().split(', ')
        self.inputLineEdit.clear()
        for tagText in newTags:
            if tagText and tagText not in self.tagTexts:
                self.addTag(tagText)
        self.tagChange.emit()

    def populateTags(self, tagList):
        for tag in tagList:
            self.addTag(tag)

    def addTag(self, text):
        newTag = QFrame()
        newTag.setStyleSheet('border:1px solid rgb(192, 192, 192); border-radius: 4px;')
        newTag.setContentsMargins(2, 2, 2, 2)
        newTag.setFixedHeight(28)
        tagLayout = QHBoxLayout()
        tagLayout.setContentsMargins(4, 4, 4, 4)
        tagLayout.setSpacing(10)

        tagLabel = QLabel(text)
        tagLabel.setStyleSheet('border:0px')
        tagLabel.setFixedHeight(16)
        # tagLabelWidth = tagLabel.fontMetrics().boundingRect(text).width() + 20
        # tagLabel.setFixedWidth(tagLabelWidth)

        deleteButton = QPushButton('x')
        deleteButton.setFixedSize(20, 20)
        deleteButton.setStyleSheet('border:0px; font-weight:bold')
        deleteButton.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        deleteButton.clicked.connect(lambda _, name=text: self.deleteTag(name))
        tagLayout.addWidget(tagLabel)
        tagLayout.addWidget(deleteButton)
        newTag.setLayout(tagLayout)
        newTag.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)

        # ADDING TAG TO TAGS & LISTING WIDGET
        self.tagTexts.append(text)
        self.listingWidget.addWidget(newTag)
        self.tagWidgets.append(newTag)

    def deleteTag(self, tagText):
        for tagWidget in self.tagWidgets:
            label = tagWidget.findChild(QLabel)
            if label.text() == tagText:
                self.tagTexts.remove(tagText)
                self.listingWidget.removeWidget(tagWidget)
                tagWidget.deleteLater()
                self.tagWidgets.remove(tagWidget)
                self.tagChange.emit()


class ResizableListingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.rows = 1
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSizeConstraint(QVBoxLayout.SetMinimumSize)
        self.widgets = []
        self.adjustWidgets()

    def resizeEvent(self, event):
        self.adjustWidgets()

    def adjustWidgets(self):
        currentX, currentY = 0, 0
        maxHeight = 0
        self.rows = 1
        for widget in self.widgets:
            widgetWidth = widget.width()
            widgetHeight = widget.height()
            if currentX + widgetWidth > self.width():
                currentY += maxHeight
                currentX = 0
                maxHeight = 0
                self.rows += 1
            widget.move(currentX, currentY)
            currentX += widgetWidth
            maxHeight = max(maxHeight, widgetHeight)
        self.adjustSize()

    def addWidget(self, widget):
        self.widgets.append(widget)
        self.layout.addWidget(widget)
        self.adjustWidgets()

    def removeWidget(self, widget):
        # self.layout.removeWidget(widget)
        self.widgets.remove(widget)
        self.adjustWidgets()


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
