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


######################## CLASSES ########################
class OnlineEditor(QWidget):
    fieldChanged = pyqtSignal()

    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path
        self.sourceTag, self.fields = sourceTag, fields
        # FIELDS LINE EDITS
        self.titleLineEdit = QLineEdit(fields['title'])
        self.authorLineEdit = QLineEdit(fields['author'])
        self.yearLineEdit = QLineEdit(fields['year'])
        self.monthComboBox = MonthComboBox(fields['month'])
        self.urlLineEdit = QLineEdit(fields['url'])
        self.noteLineEdit = QLineEdit(fields['note'])
        # FIELD CHANGES CONNECTS
        self.titleLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'title'))
        self.authorLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'author'))
        self.yearLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'year'))
        self.noteLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'note'))
        self.monthComboBox.currentTextChanged.connect(lambda text: self.userFieldChange(text, 'month'))
        self.urlLineEdit.currentTextChanged.connect(lambda text: self.userFieldChange(text, 'url'))
        # MAIN LAYOUT CREATION
        mainLayout = QGridLayout()
        mainLayout.addWidget(QLabel('Title:'), 0, 0)
        mainLayout.addWidget(self.titleLineEdit, 1, 0, 1, 4)
        mainLayout.addWidget(QLabel('Authors:'), 2, 0)
        mainLayout.addWidget(self.authorLineEdit, 3, 0, 1, 4)
        mainLayout.addWidget(QLabel('Year:'), 4, 0)
        mainLayout.addWidget(self.yearLineEdit, 4, 1)
        mainLayout.addWidget(QLabel('Month:'), 4, 2)
        mainLayout.addWidget(self.monthComboBox, 4, 3)
        mainLayout.addWidget(QLabel('Url:'), 5, 0)
        mainLayout.addWidget(self.urlLineEdit, 6, 0, 1, 4)
        mainLayout.addWidget(QLabel('Note:'), 7, 0)
        mainLayout.addWidget(self.noteLineEdit, 8, 0, 1, 4)
        self.setLayout(mainLayout)

    def userFieldChange(self, text, field):
        self.fields[field] = text
        self.fieldChanged.emit()


class MiscEditor(QWidget):
    fieldChanged = pyqtSignal()

    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path
        self.sourceTag, self.fields = sourceTag, fields
        # FIELDS LINE EDITS
        self.titleLineEdit = QLineEdit(fields['title'])
        self.authorLineEdit = QLineEdit(fields['author'])
        self.yearLineEdit = QLineEdit(fields['year'])
        self.monthComboBox = MonthComboBox(fields['month'])
        self.howPublishedLineEdit = QLineEdit(fields['howpublished'])
        self.crossrefLineEdit = QLineEdit(fields['crossref'])
        self.noteLineEdit = QLineEdit(fields['note'])
        # FIELD CHANGES CONNECTS
        self.titleLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'title'))
        self.authorLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'author'))
        self.yearLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'year'))
        self.howPublishedLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'howpublished'))
        self.crossrefLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'crossref'))
        self.noteLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'note'))
        self.monthComboBox.currentTextChanged.connect(lambda text: self.userFieldChange(text, 'month'))
        # MAIN LAYOUT CREATION
        mainLayout = QGridLayout()
        mainLayout.addWidget(QLabel('Title:'), 0, 0)
        mainLayout.addWidget(self.titleLineEdit, 1, 0, 1, 4)
        mainLayout.addWidget(QLabel('Authors:'), 2, 0)
        mainLayout.addWidget(self.authorLineEdit, 3, 0, 1, 4)
        mainLayout.addWidget(QLabel('Year:'), 4, 0)
        mainLayout.addWidget(self.yearLineEdit, 4, 1)
        mainLayout.addWidget(QLabel('Month:'), 4, 2)
        mainLayout.addWidget(self.monthComboBox, 4, 3)
        mainLayout.addWidget(QLabel('How Published:'), 5, 0)
        mainLayout.addWidget(self.howPublishedLineEdit, 6, 0, 1, 4)
        mainLayout.addWidget(QLabel('Crossref:'), 7, 0)
        mainLayout.addWidget(self.crossrefLineEdit, 8, 0, 1, 4)
        mainLayout.addWidget(QLabel('Note:'), 9, 0)
        mainLayout.addWidget(self.noteLineEdit, 10, 0, 1, 4)
        self.setLayout(mainLayout)

    def userFieldChange(self, text, field):
        self.fields[field] = text
        self.fieldChanged.emit()


class UnpublishedEditor(QWidget):
    fieldChanged = pyqtSignal()

    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path
        self.sourceTag, self.fields = sourceTag, fields
        # FIELDS LINE EDITS
        self.titleLineEdit = QLineEdit(fields['title'])
        self.authorLineEdit = QLineEdit(fields['author'])
        self.yearLineEdit = QLineEdit(fields['year'])
        self.monthComboBox = MonthComboBox(fields['month'])
        self.crossrefLineEdit = QLineEdit(fields['crossref'])
        self.noteLineEdit = QLineEdit(fields['note'])
        # FIELD CHANGES CONNECTS
        self.titleLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'title'))
        self.authorLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'author'))
        self.yearLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'year'))
        self.crossrefLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'crossref'))
        self.noteLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'note'))
        self.monthComboBox.currentTextChanged.connect(lambda text: self.userFieldChange(text, 'month'))
        # MAIN LAYOUT CREATION
        mainLayout = QGridLayout()
        mainLayout.addWidget(QLabel('Title:'), 0, 0)
        mainLayout.addWidget(self.titleLineEdit, 1, 0, 1, 4)
        mainLayout.addWidget(QLabel('Authors:'), 2, 0)
        mainLayout.addWidget(self.authorLineEdit, 3, 0, 1, 4)
        mainLayout.addWidget(QLabel('Year:'), 4, 0)
        mainLayout.addWidget(self.yearLineEdit, 4, 1)
        mainLayout.addWidget(QLabel('Month:'), 4, 2)
        mainLayout.addWidget(self.monthComboBox, 4, 3)
        mainLayout.addWidget(QLabel('Crossref:'), 5, 0)
        mainLayout.addWidget(self.crossrefLineEdit, 6, 0, 1, 4)
        mainLayout.addWidget(QLabel('Note:'), 7, 0)
        mainLayout.addWidget(self.noteLineEdit, 8, 0, 1, 4)
        self.setLayout(mainLayout)

    def userFieldChange(self, text, field):
        self.fields[field] = text
        self.fieldChanged.emit()


class UrlEditor(QWidget):
    fieldChanged = pyqtSignal()

    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path
        self.sourceTag, self.fields = sourceTag, fields
        # FIELDS LINE EDITS
        self.authorLineEdit = QLineEdit(fields['author'])
        self.seriesLineEdit = QLineEdit(fields['series'])
        self.yearLineEdit = QLineEdit(fields['year'])
        self.monthComboBox = MonthComboBox(fields['month'])
        self.editionComboBox = EditionComboBox(fields['edition'])
        self.crossrefLineEdit = QLineEdit(fields['crossref'])
        self.noteLineEdit = QLineEdit(fields['note'])
        # FIELD CHANGES CONNECTS
        self.authorLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'author'))
        self.yearLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'year'))
        self.seriesLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'series'))
        self.crossrefLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'crossref'))
        self.noteLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'note'))
        self.monthComboBox.currentTextChanged.connect(lambda text: self.userFieldChange(text, 'month'))
        self.editionComboBox.currentTextChanged.connect(lambda text: self.userFieldChange(text, 'edition'))
        # MAIN LAYOUT CREATION
        mainLayout = QGridLayout()
        mainLayout.addWidget(QLabel('Authors:'), 0, 0)
        mainLayout.addWidget(self.authorLineEdit, 1, 0, 1, 4)
        mainLayout.addWidget(QLabel('Series:'), 2, 0)
        mainLayout.addWidget(self.authorLineEdit, 3, 0, 1, 4)
        mainLayout.addWidget(QLabel('Year:'), 4, 0)
        mainLayout.addWidget(self.yearLineEdit, 4, 1)
        mainLayout.addWidget(QLabel('Month:'), 4, 2)
        mainLayout.addWidget(self.monthComboBox, 4, 3)
        mainLayout.addWidget(QLabel('Edition:'), 5, 0)
        mainLayout.addWidget(self.editionComboBox, 5, 1)
        mainLayout.addWidget(QLabel('Crossref:'), 6, 0)
        mainLayout.addWidget(self.crossrefLineEdit, 7, 0, 1, 4)
        self.setLayout(mainLayout)

    def userFieldChange(self, text, field):
        self.fields[field] = text
        self.fieldChanged.emit()


######################## FUNCTIONS ########################
def createOnlineEditor(path, sourceTag, fields):
    return OnlineEditor(path, sourceTag, fields)


def createMiscEditor(path, sourceTag, fields):
    return MiscEditor(path, sourceTag, fields)


def createUnpublishedEditor(path, sourceTag, fields):
    return UnpublishedEditor(path, sourceTag, fields)


def createUrlEditor(path, sourceTag, fields):
    return UrlEditor(path, sourceTag, fields)