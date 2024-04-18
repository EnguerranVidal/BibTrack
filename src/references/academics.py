import os
import json
import pandas as pd

# ------------------- PyQt Modules -------------------- #
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# --------------------- Sources ----------------------- #
from src.common.utilities.fileSystem import loadSettings
from src.common.widgets.fields import MonthComboBox


######################## CLASSES ########################
class ArticleEditor(QWidget):
    fieldChanged = pyqtSignal()

    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path
        self.sourceTag, self.fields = sourceTag, fields
        # FIELDS LINE EDITS
        self.titleLineEdit = QLineEdit(fields['title'])
        self.authorLineEdit = QLineEdit(fields['author'])
        self.journalLineEdit = QLineEdit(fields['journal'])
        self.yearLineEdit = QLineEdit(fields['year'])
        self.volumeLineEdit = QLineEdit(fields['volume'])
        self.numberLineEdit = QLineEdit(fields['number'])
        self.pagesLineEdit = QLineEdit(fields['pages'])
        self.crossrefLineEdit = QLineEdit(fields['crossref'])
        self.noteLineEdit = QLineEdit(fields['note'])
        self.monthComboBox = MonthComboBox(fields['month'])
        # FIELD CHANGES CONNECTS
        self.titleLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'title'))
        self.authorLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'author'))
        self.journalLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'journal'))
        self.yearLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'year'))
        self.volumeLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'volume'))
        self.numberLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'number'))
        self.pagesLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'pages'))
        self.crossrefLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'crossref'))
        self.noteLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'note'))
        self.monthComboBox.currentTextChanged.connect(lambda text: self.userFieldChange(text, 'month'))
        # MAIN LAYOUT CREATION
        mainLayout = QGridLayout()
        mainLayout.addWidget(QLabel('Title:'), 0, 0)
        mainLayout.addWidget(self.titleLineEdit, 1, 0, 1, 4)
        mainLayout.addWidget(QLabel('Authors:'), 2, 0)
        mainLayout.addWidget(self.authorLineEdit, 3, 0, 1, 4)
        mainLayout.addWidget(QLabel('Journal:'), 4, 0)
        mainLayout.addWidget(self.journalLineEdit, 5, 0, 1, 4)
        mainLayout.addWidget(QLabel('Year:'), 6, 0)
        mainLayout.addWidget(self.yearLineEdit, 6, 1)
        mainLayout.addWidget(QLabel('Month:'), 6, 2)
        mainLayout.addWidget(self.monthComboBox, 6, 3)
        mainLayout.addWidget(QLabel('Volume:'), 7, 0)
        mainLayout.addWidget(self.volumeLineEdit, 8, 0, 1, 4)
        mainLayout.addWidget(QLabel('Number:'), 9, 0)
        mainLayout.addWidget(self.numberLineEdit, 10, 0, 1, 4)
        mainLayout.addWidget(QLabel('Pages:'), 11, 0)
        mainLayout.addWidget(self.pagesLineEdit, 12, 0, 1, 4)
        mainLayout.addWidget(QLabel('Crossref:'), 13, 0)
        mainLayout.addWidget(self.crossrefLineEdit, 14, 0, 1, 4)
        mainLayout.addWidget(QLabel('Note:'), 15, 0)
        mainLayout.addWidget(self.noteLineEdit, 16, 0, 1, 4)
        self.setLayout(mainLayout)

    def userFieldChange(self, text, field):
        self.fields[field] = text
        self.fieldChanged.emit()


class ConferenceEditor(QWidget):
    fieldChanged = pyqtSignal()

    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path
        self.sourceTag, self.fields = sourceTag, fields
        # FIELDS LINE EDITS
        self.titleLineEdit = QLineEdit(fields['title'])
        self.authorLineEdit = QLineEdit(fields['author'])
        self.bookTitleLineEdit = QLineEdit(fields['booktitle'])
        self.yearLineEdit = QLineEdit(fields['year'])
        self.editorLineEdit = QLineEdit(fields['editor'])
        self.volumeLineEdit = QLineEdit(fields['volume'])
        self.seriesLineEdit = QLineEdit(fields['series'])
        self.pagesLineEdit = QLineEdit(fields['pages'])
        self.addressLineEdit = QLineEdit(fields['address'])
        self.organizationLineEdit = QLineEdit(fields['organization'])
        self.publisherLineEdit = QLineEdit(fields['publisher'])
        self.crossrefLineEdit = QLineEdit(fields['crossref'])
        self.noteLineEdit = QLineEdit(fields['note'])
        self.monthComboBox = MonthComboBox(fields['month'])
        # FIELD CHANGES CONNECTS
        self.titleLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'title'))
        self.authorLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'author'))
        self.bookTitleLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'booktitle'))
        self.yearLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'year'))
        self.editorLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'editor'))
        self.volumeLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'volume'))
        self.seriesLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'series'))
        self.pagesLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'pages'))
        self.addressLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'address'))
        self.organizationLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'organization'))
        self.publisherLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'publisher'))
        self.crossrefLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'crossref'))
        self.noteLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'note'))
        self.monthComboBox.currentTextChanged.connect(lambda text: self.userFieldChange(text, 'month'))
        # MAIN LAYOUT CREATION
        mainLayout = QGridLayout()
        mainLayout.addWidget(QLabel('Title:'), 0, 0)
        mainLayout.addWidget(self.titleLineEdit, 1, 0, 1, 4)
        mainLayout.addWidget(QLabel('Authors:'), 2, 0)
        mainLayout.addWidget(self.authorLineEdit, 3, 0, 1, 4)
        mainLayout.addWidget(QLabel('Book Title:'), 4, 0)
        mainLayout.addWidget(self.bookTitleLineEdit, 5, 0, 1, 4)
        mainLayout.addWidget(QLabel('Year:'), 6, 0)
        mainLayout.addWidget(self.yearLineEdit, 6, 1)
        mainLayout.addWidget(QLabel('Month:'), 6, 2)
        mainLayout.addWidget(self.monthComboBox, 6, 3)
        mainLayout.addWidget(QLabel('Volume:'), 7, 0)
        mainLayout.addWidget(self.volumeLineEdit, 8, 0, 1, 4)
        mainLayout.addWidget(QLabel('Series:'), 9, 0)
        mainLayout.addWidget(self.seriesLineEdit, 10, 0, 1, 4)
        mainLayout.addWidget(QLabel('Pages:'), 11, 0)
        mainLayout.addWidget(self.pagesLineEdit, 12, 0, 1, 4)
        mainLayout.addWidget(QLabel('Organization:'), 13, 0)
        mainLayout.addWidget(self.organizationLineEdit, 14, 0, 1, 4)
        mainLayout.addWidget(QLabel('Publisher:'), 15, 0)
        mainLayout.addWidget(self.publisherLineEdit, 16, 0, 1, 4)
        mainLayout.addWidget(QLabel('Address:'), 17, 0)
        mainLayout.addWidget(self.addressLineEdit, 18, 0, 1, 4)
        mainLayout.addWidget(QLabel('Crossref:'), 19, 0)
        mainLayout.addWidget(self.crossrefLineEdit, 20, 0, 1, 4)
        mainLayout.addWidget(QLabel('Note:'), 21, 0)
        mainLayout.addWidget(self.noteLineEdit, 22, 0, 1, 4)
        self.setLayout(mainLayout)

    def userFieldChange(self, text, field):
        self.fields[field] = text
        self.fieldChanged.emit()


class InProceedingsEditor(QWidget):
    fieldChanged = pyqtSignal()

    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path
        self.sourceTag, self.fields = sourceTag, fields
        # FIELDS LINE EDITS
        self.titleLineEdit = QLineEdit(fields['title'])
        self.authorLineEdit = QLineEdit(fields['author'])
        self.bookTitleLineEdit = QLineEdit(fields['booktitle'])
        self.yearLineEdit = QLineEdit(fields['year'])
        self.editorLineEdit = QLineEdit(fields['editor'])
        self.volumeLineEdit = QLineEdit(fields['volume'])
        self.seriesLineEdit = QLineEdit(fields['series'])
        self.pagesLineEdit = QLineEdit(fields['pages'])
        self.addressLineEdit = QLineEdit(fields['address'])
        self.organizationLineEdit = QLineEdit(fields['organization'])
        self.publisherLineEdit = QLineEdit(fields['publisher'])
        self.crossrefLineEdit = QLineEdit(fields['crossref'])
        self.noteLineEdit = QLineEdit(fields['note'])
        self.monthComboBox = MonthComboBox(fields['month'])
        # FIELD CHANGES CONNECTS
        self.titleLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'title'))
        self.authorLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'author'))
        self.bookTitleLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'booktitle'))
        self.yearLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'year'))
        self.editorLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'editor'))
        self.volumeLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'volume'))
        self.seriesLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'series'))
        self.pagesLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'pages'))
        self.addressLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'address'))
        self.organizationLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'organization'))
        self.publisherLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'publisher'))
        self.crossrefLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'crossref'))
        self.noteLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'note'))
        self.monthComboBox.currentTextChanged.connect(lambda text: self.userFieldChange(text, 'month'))
        # MAIN LAYOUT CREATION
        mainLayout = QGridLayout()
        mainLayout.addWidget(QLabel('Title:'), 0, 0)
        mainLayout.addWidget(self.titleLineEdit, 1, 0, 1, 4)
        mainLayout.addWidget(QLabel('Authors:'), 2, 0)
        mainLayout.addWidget(self.authorLineEdit, 3, 0, 1, 4)
        mainLayout.addWidget(QLabel('Book Title:'), 4, 0)
        mainLayout.addWidget(self.bookTitleLineEdit, 5, 0, 1, 4)
        mainLayout.addWidget(QLabel('Year:'), 6, 0)
        mainLayout.addWidget(self.yearLineEdit, 6, 1)
        mainLayout.addWidget(QLabel('Month:'), 6, 2)
        mainLayout.addWidget(self.monthComboBox, 6, 3)
        mainLayout.addWidget(QLabel('Volume:'), 7, 0)
        mainLayout.addWidget(self.volumeLineEdit, 8, 0, 1, 4)
        mainLayout.addWidget(QLabel('Series:'), 9, 0)
        mainLayout.addWidget(self.seriesLineEdit, 10, 0, 1, 4)
        mainLayout.addWidget(QLabel('Pages:'), 11, 0)
        mainLayout.addWidget(self.pagesLineEdit, 12, 0, 1, 4)
        mainLayout.addWidget(QLabel('Organization:'), 13, 0)
        mainLayout.addWidget(self.organizationLineEdit, 14, 0, 1, 4)
        mainLayout.addWidget(QLabel('Publisher:'), 15, 0)
        mainLayout.addWidget(self.publisherLineEdit, 16, 0, 1, 4)
        mainLayout.addWidget(QLabel('Address:'), 17, 0)
        mainLayout.addWidget(self.addressLineEdit, 18, 0, 1, 4)
        mainLayout.addWidget(QLabel('Crossref:'), 19, 0)
        mainLayout.addWidget(self.crossrefLineEdit, 20, 0, 1, 4)
        mainLayout.addWidget(QLabel('Note:'), 21, 0)
        mainLayout.addWidget(self.noteLineEdit, 22, 0, 1, 4)
        self.setLayout(mainLayout)

    def userFieldChange(self, text, field):
        self.fields[field] = text
        self.fieldChanged.emit()


class MastersThesisEditor(QWidget):
    fieldChanged = pyqtSignal()

    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path
        self.sourceTag, self.fields = sourceTag, fields
        # FIELDS LINE EDITS
        self.titleLineEdit = QLineEdit(fields['title'])
        self.authorLineEdit = QLineEdit(fields['author'])
        self.schoolLineEdit = QLineEdit(fields['school'])
        self.yearLineEdit = QLineEdit(fields['year'])
        self.typeLineEdit = QLineEdit(fields['type'])
        self.addressLineEdit = QLineEdit(fields['address'])
        self.crossrefLineEdit = QLineEdit(fields['crossref'])
        self.noteLineEdit = QLineEdit(fields['note'])
        self.monthComboBox = MonthComboBox(fields['month'])
        # FIELD CHANGES CONNECTS
        self.titleLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'title'))
        self.authorLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'author'))
        self.schoolLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'school'))
        self.yearLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'year'))
        self.typeLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'type'))
        self.addressLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'address'))
        self.crossrefLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'crossref'))
        self.noteLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'note'))
        self.monthComboBox.currentTextChanged.connect(lambda text: self.userFieldChange(text, 'month'))
        # MAIN LAYOUT CREATION
        mainLayout = QGridLayout()
        mainLayout.addWidget(QLabel('Title:'), 0, 0)
        mainLayout.addWidget(self.titleLineEdit, 1, 0, 1, 4)
        mainLayout.addWidget(QLabel('Authors:'), 2, 0)
        mainLayout.addWidget(self.authorLineEdit, 3, 0, 1, 4)
        mainLayout.addWidget(QLabel('School:'), 4, 0)
        mainLayout.addWidget(self.schoolLineEdit, 5, 0, 1, 4)
        mainLayout.addWidget(QLabel('Year:'), 6, 0)
        mainLayout.addWidget(self.yearLineEdit, 6, 1)
        mainLayout.addWidget(QLabel('Month:'), 6, 2)
        mainLayout.addWidget(self.monthComboBox, 6, 3)
        mainLayout.addWidget(QLabel('Type:'), 7, 0)
        mainLayout.addWidget(self.typeLineEdit, 8, 0, 1, 4)
        mainLayout.addWidget(QLabel('Address:'), 9, 0)
        mainLayout.addWidget(self.addressLineEdit, 10, 0, 1, 4)
        mainLayout.addWidget(QLabel('Crossref:'), 11, 0)
        mainLayout.addWidget(self.crossrefLineEdit, 12, 0, 1, 4)
        mainLayout.addWidget(QLabel('Note:'), 13, 0)
        mainLayout.addWidget(self.noteLineEdit, 14, 0, 1, 4)
        self.setLayout(mainLayout)

    def userFieldChange(self, text, field):
        self.fields[field] = text
        self.fieldChanged.emit()


class ProceedingsEditor(QWidget):
    fieldChanged = pyqtSignal()

    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path
        self.sourceTag, self.fields = sourceTag, fields
        # FIELDS LINE EDITS
        self.titleLineEdit = QLineEdit(fields['title'])
        self.yearLineEdit = QLineEdit(fields['year'])
        self.editorLineEdit = QLineEdit(fields['editor'])
        self.volumeLineEdit = QLineEdit(fields['volume'])
        self.seriesLineEdit = QLineEdit(fields['series'])
        self.addressLineEdit = QLineEdit(fields['address'])
        self.organizationLineEdit = QLineEdit(fields['organization'])
        self.publisherLineEdit = QLineEdit(fields['publisher'])
        self.crossrefLineEdit = QLineEdit(fields['crossref'])
        self.noteLineEdit = QLineEdit(fields['note'])
        self.monthComboBox = MonthComboBox(fields['month'])
        # FIELD CHANGES CONNECTS
        self.titleLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'title'))
        self.yearLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'year'))
        self.editorLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'editor'))
        self.volumeLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'volume'))
        self.seriesLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'series'))
        self.addressLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'address'))
        self.organizationLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'organization'))
        self.publisherLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'publisher'))
        self.crossrefLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'crossref'))
        self.noteLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'note'))
        self.monthComboBox.currentTextChanged.connect(lambda text: self.userFieldChange(text, 'month'))
        # MAIN LAYOUT CREATION
        mainLayout = QGridLayout()
        mainLayout.addWidget(QLabel('Title:'), 0, 0)
        mainLayout.addWidget(self.titleLineEdit, 1, 0, 1, 4)
        mainLayout.addWidget(QLabel('Year:'), 2, 0)
        mainLayout.addWidget(self.yearLineEdit, 2, 1)
        mainLayout.addWidget(QLabel('Month:'), 2, 2)
        mainLayout.addWidget(self.monthComboBox, 2, 3)
        mainLayout.addWidget(QLabel('Volume:'), 3, 0)
        mainLayout.addWidget(self.volumeLineEdit, 4, 0, 1, 4)
        mainLayout.addWidget(QLabel('Series:'), 5, 0)
        mainLayout.addWidget(self.seriesLineEdit, 6, 0, 1, 4)
        mainLayout.addWidget(QLabel('Pages:'), 7, 0)
        mainLayout.addWidget(self.pagesLineEdit, 8, 0, 1, 4)
        mainLayout.addWidget(QLabel('Organization:'), 9, 0)
        mainLayout.addWidget(self.organizationLineEdit, 10, 0, 1, 4)
        mainLayout.addWidget(QLabel('Publisher:'), 11, 0)
        mainLayout.addWidget(self.publisherLineEdit, 12, 0, 1, 4)
        mainLayout.addWidget(QLabel('Address:'), 13, 0)
        mainLayout.addWidget(self.addressLineEdit, 14, 0, 1, 4)
        mainLayout.addWidget(QLabel('Crossref:'), 15, 0)
        mainLayout.addWidget(self.crossrefLineEdit, 16, 0, 1, 4)
        mainLayout.addWidget(QLabel('Note:'), 17, 0)
        mainLayout.addWidget(self.noteLineEdit, 18, 0, 1, 4)
        self.setLayout(mainLayout)

    def userFieldChange(self, text, field):
        self.fields[field] = text
        self.fieldChanged.emit()


class PhdThesisEditor(QWidget):
    fieldChanged = pyqtSignal()

    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path
        self.sourceTag, self.fields = sourceTag, fields
        # FIELDS LINE EDITS
        self.titleLineEdit = QLineEdit(fields['title'])
        self.authorLineEdit = QLineEdit(fields['author'])
        self.schoolLineEdit = QLineEdit(fields['school'])
        self.yearLineEdit = QLineEdit(fields['year'])
        self.typeLineEdit = QLineEdit(fields['type'])
        self.addressLineEdit = QLineEdit(fields['address'])
        self.crossrefLineEdit = QLineEdit(fields['crossref'])
        self.noteLineEdit = QLineEdit(fields['note'])
        self.monthComboBox = MonthComboBox(fields['month'])
        # FIELD CHANGES CONNECTS
        self.titleLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'title'))
        self.authorLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'author'))
        self.schoolLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'school'))
        self.yearLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'year'))
        self.typeLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'type'))
        self.addressLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'address'))
        self.crossrefLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'crossref'))
        self.noteLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'note'))
        self.monthComboBox.currentTextChanged.connect(lambda text: self.userFieldChange(text, 'month'))
        # MAIN LAYOUT CREATION
        mainLayout = QGridLayout()
        mainLayout.addWidget(QLabel('Title:'), 0, 0)
        mainLayout.addWidget(self.titleLineEdit, 1, 0, 1, 4)
        mainLayout.addWidget(QLabel('Authors:'), 2, 0)
        mainLayout.addWidget(self.authorLineEdit, 3, 0, 1, 4)
        mainLayout.addWidget(QLabel('School:'), 4, 0)
        mainLayout.addWidget(self.schoolLineEdit, 5, 0, 1, 4)
        mainLayout.addWidget(QLabel('Year:'), 6, 0)
        mainLayout.addWidget(self.yearLineEdit, 6, 1)
        mainLayout.addWidget(QLabel('Month:'), 6, 2)
        mainLayout.addWidget(self.monthComboBox, 6, 3)
        mainLayout.addWidget(QLabel('Type:'), 7, 0)
        mainLayout.addWidget(self.typeLineEdit, 8, 0, 1, 4)
        mainLayout.addWidget(QLabel('Address:'), 9, 0)
        mainLayout.addWidget(self.addressLineEdit, 10, 0, 1, 4)
        mainLayout.addWidget(QLabel('Crossref:'), 11, 0)
        mainLayout.addWidget(self.crossrefLineEdit, 12, 0, 1, 4)
        mainLayout.addWidget(QLabel('Note:'), 13, 0)
        mainLayout.addWidget(self.noteLineEdit, 14, 0, 1, 4)
        self.setLayout(mainLayout)

    def userFieldChange(self, text, field):
        self.fields[field] = text
        self.fieldChanged.emit()


######################## FUNCTIONS ########################
def createArticleEditor(path, sourceTag, fields):
    return ArticleEditor(path, sourceTag, fields)


def createConferenceEditor(path, sourceTag, fields):
    return ConferenceEditor(path, sourceTag, fields)


def createInProceedingsEditor(path, sourceTag, fields):
    return InProceedingsEditor(path, sourceTag, fields)


def createMastersThesisEditor(path, sourceTag, fields):
    return MastersThesisEditor(path, sourceTag, fields)


def createPhdThesisEditor(path, sourceTag, fields):
    return PhdThesisEditor(path, sourceTag, fields)


def createProceedingsEditor(path, sourceTag, fields):
    return ProceedingsEditor(path, sourceTag, fields)



