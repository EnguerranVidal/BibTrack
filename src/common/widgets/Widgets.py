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
