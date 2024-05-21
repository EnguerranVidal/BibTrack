import os
import json
import pandas as pd

# ------------------- PyQt Modules -------------------- #
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# --------------------- Sources ----------------------- #
from src.common.utilities.fileSystem import loadSettings
from src.common.widgets.widgets import MonthComboBox, EditionComboBox
from src.common.widgets.widgets import SquareIconButton, IconButton


######################## CLASSES ########################
class BookEditor(QWidget):
    fieldChanged = pyqtSignal()

    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path
        self.sourceTag, self.fields = sourceTag, fields
        # FIELDS LINE EDITS
        self.titleLineEdit = QLineEdit(fields['title'])
        self.authorLineEdit = QLineEdit(fields['author'])
        self.publisherLineEdit = QLineEdit(fields['publisher'])
        self.yearLineEdit = QLineEdit(fields['year'])
        self.volumeLineEdit = QLineEdit(fields['volume'])
        self.seriesLineEdit = QLineEdit(fields['series'])
        self.addressLineEdit = QLineEdit(fields['address'])
        self.crossrefLineEdit = QLineEdit(fields['crossref'])
        self.noteLineEdit = QLineEdit(fields['note'])
        self.editionComboBox = EditionComboBox(fields['edition'])
        self.monthComboBox = MonthComboBox(fields['month'])
        # FIELD CHANGES CONNECTS
        self.titleLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'title'))
        self.authorLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'author'))
        self.publisherLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'publisher'))
        self.yearLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'year'))
        self.volumeLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'volume'))
        self.seriesLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'series'))
        self.addressLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'address'))
        self.crossrefLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'crossref'))
        self.noteLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'note'))
        self.monthComboBox.currentTextChanged.connect(lambda text: self.userFieldChange(text, 'month'))
        self.editionComboBox.currentTextChanged.connect(lambda text: self.userFieldChange(text, 'edition'))
        # MAIN LAYOUT CREATION
        mainLayout = QGridLayout()
        mainLayout.addWidget(QLabel('TITLE:'), 0, 0)
        mainLayout.addWidget(self.titleLineEdit, 1, 0, 1, 4)
        mainLayout.addWidget(QLabel('AUTHORS:'), 2, 0)
        mainLayout.addWidget(self.authorLineEdit, 3, 0, 1, 4)
        mainLayout.addWidget(QLabel('PUBLISHER:'), 4, 0)
        mainLayout.addWidget(self.publisherLineEdit, 5, 0, 1, 4)
        mainLayout.addWidget(QLabel('YEAR:'), 6, 0)
        mainLayout.addWidget(self.yearLineEdit, 6, 1)
        mainLayout.addWidget(QLabel('MONTH:'), 6, 2)
        mainLayout.addWidget(self.monthComboBox, 6, 3)
        mainLayout.addWidget(QLabel('VOLUME:'), 7, 0)
        mainLayout.addWidget(self.volumeLineEdit, 8, 0, 1, 4)
        mainLayout.addWidget(QLabel('SERIES:'), 9, 0)
        mainLayout.addWidget(self.seriesLineEdit, 10, 0, 1, 4)
        mainLayout.addWidget(QLabel('ADDRESS:'), 11, 0)
        mainLayout.addWidget(self.addressLineEdit, 12, 0, 1, 4)
        mainLayout.addWidget(QLabel('EDITION:'), 13, 0)
        mainLayout.addWidget(self.editionComboBox, 13, 1)
        mainLayout.addWidget(QLabel('CROSSREF:'), 14, 0)
        mainLayout.addWidget(self.crossrefLineEdit, 15, 0, 1, 4)
        mainLayout.addWidget(QLabel('NOTE:'), 16, 0)
        mainLayout.addWidget(self.noteLineEdit, 17, 0, 1, 4)
        self.setLayout(mainLayout)

    def userFieldChange(self, text, field):
        self.fields[field] = text
        self.fieldChanged.emit()


class BookletEditor(QWidget):
    fieldChanged = pyqtSignal()

    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path
        self.sourceTag, self.fields = sourceTag, fields
        # FIELDS LINE EDITS
        self.titleLineEdit = QLineEdit(fields['title'])
        self.authorLineEdit = QLineEdit(fields['author'])
        self.howPublishedLineEdit = QLineEdit(fields['howpublished'])
        self.yearLineEdit = QLineEdit(fields['year'])
        self.addressLineEdit = QLineEdit(fields['address'])
        self.crossrefLineEdit = QLineEdit(fields['crossref'])
        self.noteLineEdit = QLineEdit(fields['note'])
        self.monthComboBox = MonthComboBox(fields['month'])
        # FIELD CHANGES CONNECTS
        self.titleLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'title'))
        self.authorLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'author'))
        self.howPublishedLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'howpublished'))
        self.yearLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'year'))
        self.addressLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'address'))
        self.crossrefLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'crossref'))
        self.noteLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'note'))
        self.monthComboBox.currentTextChanged.connect(lambda text: self.userFieldChange(text, 'month'))
        # MAIN LAYOUT CREATION
        mainLayout = QGridLayout()
        mainLayout.addWidget(QLabel('TITLE:'), 0, 0)
        mainLayout.addWidget(self.titleLineEdit, 1, 0, 1, 4)
        mainLayout.addWidget(QLabel('AUTHORS:'), 2, 0)
        mainLayout.addWidget(self.authorLineEdit, 3, 0, 1, 4)
        mainLayout.addWidget(QLabel('HOW PUBLISHED:'), 4, 0)
        mainLayout.addWidget(self.howPublishedLineEdit, 5, 0, 1, 4)
        mainLayout.addWidget(QLabel('YEAR:'), 6, 0)
        mainLayout.addWidget(self.yearLineEdit, 6, 1)
        mainLayout.addWidget(QLabel('MONTH:'), 6, 2)
        mainLayout.addWidget(self.monthComboBox, 6, 3)
        mainLayout.addWidget(QLabel('ADDRESS:'), 7, 0)
        mainLayout.addWidget(self.addressLineEdit, 8, 0, 1, 4)
        mainLayout.addWidget(QLabel('CROSSREF:'), 9, 0)
        mainLayout.addWidget(self.crossrefLineEdit, 10, 0, 1, 4)
        mainLayout.addWidget(QLabel('NOTE:'), 11, 0)
        mainLayout.addWidget(self.noteLineEdit, 12, 0, 1, 4)
        self.setLayout(mainLayout)

    def userFieldChange(self, text, field):
        self.fields[field] = text
        self.fieldChanged.emit()


class InBookEditor(QWidget):
    fieldChanged = pyqtSignal()

    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path
        self.sourceTag, self.fields = sourceTag, fields
        # FIELDS LINE EDITS
        self.titleLineEdit = QLineEdit(fields['title'])
        self.authorLineEdit = QLineEdit(fields['author'])
        self.chapterLineEdit = QLineEdit(fields['chapter'])
        self.publisherLineEdit = QLineEdit(fields['publisher'])
        self.yearLineEdit = QLineEdit(fields['year'])
        self.addressLineEdit = QLineEdit(fields['address'])
        self.volumeLineEdit = QLineEdit(fields['volume'])
        self.seriesLineEdit = QLineEdit(fields['series'])
        self.typeLineEdit = QLineEdit(fields['type'])
        self.crossrefLineEdit = QLineEdit(fields['crossref'])
        self.noteLineEdit = QLineEdit(fields['note'])
        self.editionComboBox = EditionComboBox(fields['edition'])
        self.monthComboBox = MonthComboBox(fields['month'])
        # FIELD CHANGES CONNECTS
        self.titleLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'title'))
        self.authorLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'author'))
        self.chapterLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'chapter'))
        self.publisherLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'publisher'))
        self.yearLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'year'))
        self.addressLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'address'))
        self.volumeLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'volume'))
        self.seriesLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'series'))
        self.typeLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'type'))
        self.crossrefLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'crossref'))
        self.noteLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'note'))
        self.monthComboBox.currentTextChanged.connect(lambda text: self.userFieldChange(text, 'month'))
        self.editionComboBox.currentTextChanged.connect(lambda text: self.userFieldChange(text, 'edition'))
        # MAIN LAYOUT CREATION
        mainLayout = QGridLayout()
        mainLayout.addWidget(QLabel('TITLE:'), 0, 0)
        mainLayout.addWidget(self.titleLineEdit, 1, 0, 1, 4)
        mainLayout.addWidget(QLabel('AUTHORS:'), 2, 0)
        mainLayout.addWidget(self.authorLineEdit, 3, 0, 1, 4)
        mainLayout.addWidget(QLabel('Chapter:'), 4, 0)
        mainLayout.addWidget(self.chapterLineEdit, 5, 0, 1, 4)
        mainLayout.addWidget(QLabel('PUBLISHER:'), 6, 0)
        mainLayout.addWidget(self.publisherLineEdit, 7, 0, 1, 4)
        mainLayout.addWidget(QLabel('YEAR:'), 8, 0)
        mainLayout.addWidget(self.yearLineEdit, 8, 1)
        mainLayout.addWidget(QLabel('MONTH:'), 8, 2)
        mainLayout.addWidget(self.monthComboBox, 8, 3)
        mainLayout.addWidget(QLabel('VOLUME:'), 9, 0)
        mainLayout.addWidget(self.volumeLineEdit, 10, 0, 1, 4)
        mainLayout.addWidget(QLabel('SERIES:'), 11, 0)
        mainLayout.addWidget(self.seriesLineEdit, 12, 0, 1, 4)
        mainLayout.addWidget(QLabel('TYPE:'), 13, 0)
        mainLayout.addWidget(self.typeLineEdit, 14, 0, 1, 4)
        mainLayout.addWidget(QLabel('ADDRESS:'), 15, 0)
        mainLayout.addWidget(self.addressLineEdit, 16, 0, 1, 4)
        mainLayout.addWidget(QLabel('EDITION:'), 17, 0)
        mainLayout.addWidget(self.editionComboBox, 17, 1)
        mainLayout.addWidget(QLabel('CROSSREF:'), 18, 0)
        mainLayout.addWidget(self.crossrefLineEdit, 19, 0, 1, 4)
        mainLayout.addWidget(QLabel('NOTE:'), 20, 0)
        mainLayout.addWidget(self.noteLineEdit, 21, 0, 1, 4)
        self.setLayout(mainLayout)

    def userFieldChange(self, text, field):
        self.fields['FIELDS'][field] = text
        self.fieldChanged.emit()


class InCollectionEditor(QWidget):
    fieldChanged = pyqtSignal()

    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path
        self.sourceTag, self.fields = sourceTag, fields
        # FIELDS LINE EDITS
        self.titleLineEdit = QLineEdit(fields['title'])
        self.authorLineEdit = QLineEdit(fields['author'])
        self.bookTitleLineEdit = QLineEdit(fields['booktitle'])
        self.publisherLineEdit = QLineEdit(fields['publisher'])
        self.yearLineEdit = QLineEdit(fields['year'])
        self.editorLineEdit = QLineEdit(fields['editor'])
        self.volumeLineEdit = QLineEdit(fields['volume'])
        self.seriesLineEdit = QLineEdit(fields['series'])
        self.typeLineEdit = QLineEdit(fields['type'])
        self.chapterLineEdit = QLineEdit(fields['chapter'])
        self.pagesLineEdit = QLineEdit(fields['pages'])
        self.addressLineEdit = QLineEdit(fields['address'])
        self.organizationLineEdit = QLineEdit(fields['organization'])
        self.crossrefLineEdit = QLineEdit(fields['crossref'])
        self.noteLineEdit = QLineEdit(fields['note'])
        self.editionComboBox = EditionComboBox(fields['edition'])
        self.monthComboBox = MonthComboBox(fields['month'])
        # FIELD CHANGES CONNECTS
        self.titleLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'title'))
        self.authorLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'author'))
        self.bookTitleLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'booktitle'))
        self.publisherLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'publisher'))
        self.yearLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'year'))
        self.editorLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'editor'))
        self.volumeLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'volume'))
        self.seriesLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'series'))
        self.typeLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'type'))
        self.chapterLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'chapter'))
        self.pagesLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'pages'))
        self.addressLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'address'))
        self.organizationLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'organization'))
        self.crossrefLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'crossref'))
        self.noteLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'note'))
        self.monthComboBox.currentTextChanged.connect(lambda text: self.userFieldChange(text, 'month'))
        self.editionComboBox.currentTextChanged.connect(lambda text: self.userFieldChange(text, 'edition'))
        # MAIN LAYOUT CREATION
        mainLayout = QGridLayout()
        mainLayout.addWidget(QLabel('TITLE:'), 0, 0)
        mainLayout.addWidget(self.titleLineEdit, 1, 0, 1, 4)
        mainLayout.addWidget(QLabel('AUTHORS:'), 2, 0)
        mainLayout.addWidget(self.authorLineEdit, 3, 0, 1, 4)
        mainLayout.addWidget(QLabel('BOOK TITLE:'), 4, 0)
        mainLayout.addWidget(self.bookTitleLineEdit, 5, 0, 1, 4)
        mainLayout.addWidget(QLabel('PUBLISHER:'), 6, 0)
        mainLayout.addWidget(self.publisherLineEdit, 7, 0, 1, 4)
        mainLayout.addWidget(QLabel('YEAR:'), 8, 0)
        mainLayout.addWidget(self.yearLineEdit, 8, 1)
        mainLayout.addWidget(QLabel('MONTH:'), 8, 2)
        mainLayout.addWidget(self.monthComboBox, 8, 3)
        mainLayout.addWidget(QLabel('EDITOR:'), 9, 0)
        mainLayout.addWidget(self.editorLineEdit, 10, 0, 1, 4)
        mainLayout.addWidget(QLabel('VOLUME:'), 11, 0)
        mainLayout.addWidget(self.volumeLineEdit, 12, 0, 1, 4)
        mainLayout.addWidget(QLabel('SERIES:'), 13, 0)
        mainLayout.addWidget(self.seriesLineEdit, 14, 0, 1, 4)
        mainLayout.addWidget(QLabel('TYPE:'), 15, 0)
        mainLayout.addWidget(self.typeLineEdit, 16, 0, 1, 4)
        mainLayout.addWidget(QLabel('CHAPTER:'), 15, 0)
        mainLayout.addWidget(self.chapterLineEdit, 16, 0, 1, 4)
        mainLayout.addWidget(QLabel('PAGES:'), 17, 0)
        mainLayout.addWidget(self.pagesLineEdit, 18, 0, 1, 4)
        mainLayout.addWidget(QLabel('ADDRESS:'), 17, 0)
        mainLayout.addWidget(self.addressLineEdit, 18, 0, 1, 4)
        mainLayout.addWidget(QLabel('ORGANIZATION:'), 17, 0)
        mainLayout.addWidget(self.organizationLineEdit, 18, 0, 1, 4)
        mainLayout.addWidget(QLabel('EDITION:'), 19, 0)
        mainLayout.addWidget(self.editionComboBox, 19, 1)
        mainLayout.addWidget(QLabel('CROSSREF:'), 20, 0)
        mainLayout.addWidget(self.crossrefLineEdit, 21, 0, 1, 4)
        mainLayout.addWidget(QLabel('NOTE:'), 22, 0)
        mainLayout.addWidget(self.noteLineEdit, 23, 0, 1, 4)
        self.setLayout(mainLayout)

    def userFieldChange(self, text, field):
        self.fields[field] = text
        self.fieldChanged.emit()


######################## FUNCTIONS ########################
def createBookEditor(path, sourceTag, fields):
    return BookEditor(path, sourceTag, fields)


def createBookletEditor(path, sourceTag, fields):
    return BookletEditor(path, sourceTag, fields)


def createInBookEditor(path, sourceTag, fields):
    return InBookEditor(path, sourceTag, fields)


def createInCollectionEditor(path, sourceTag, fields):
    return InCollectionEditor(path, sourceTag, fields)
