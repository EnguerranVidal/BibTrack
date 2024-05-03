import os
import json
import pandas as pd

# ------------------- PyQt Modules -------------------- #
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# --------------------- Sources ----------------------- #
from src.common.utilities.fileSystem import loadSettings
from src.common.widgets.widgets import MonthComboBox


######################## CLASSES ########################
class ManualEditor(QWidget):
    fieldChanged = pyqtSignal()

    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path
        self.sourceTag, self.fields = sourceTag, fields
        # FIELDS LINE EDITS
        self.titleLineEdit = QLineEdit(fields['title'])
        self.authorLineEdit = QLineEdit(fields['author'])
        self.organizationLineEdit = QLineEdit(fields['organization'])
        self.addressLineEdit = QLineEdit(fields['address'])
        self.editionLineEdit = QLineEdit(fields['edition'])
        self.yearLineEdit = QLineEdit(fields['year'])
        self.crossrefLineEdit = QLineEdit(fields['crossref'])
        self.noteLineEdit = QLineEdit(fields['note'])
        self.monthComboBox = MonthComboBox(fields['month'])
        # FIELD CHANGES CONNECTS
        self.titleLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'title'))
        self.authorLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'author'))
        self.organizationLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'organization'))
        self.yearLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'year'))
        self.addressLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'address'))
        self.crossrefLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'crossref'))
        self.noteLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'note'))
        self.monthComboBox.currentTextChanged.connect(lambda text: self.userFieldChange(text, 'month'))
        self.editionComboBox.currentTextChanged.connect(lambda text: self.userFieldChange(text, 'edition'))
        # MAIN LAYOUT CREATION
        mainLayout = QGridLayout()
        mainLayout.addWidget(QLabel('Title:'), 0, 0)
        mainLayout.addWidget(self.titleLineEdit, 1, 0, 1, 4)
        mainLayout.addWidget(QLabel('Authors:'), 2, 0)
        mainLayout.addWidget(self.authorLineEdit, 3, 0, 1, 4)
        mainLayout.addWidget(QLabel('Organization:'), 4, 0)
        mainLayout.addWidget(self.organizationLineEdit, 5, 0, 1, 4)
        mainLayout.addWidget(QLabel('Year:'), 6, 0)
        mainLayout.addWidget(self.yearLineEdit, 6, 1)
        mainLayout.addWidget(QLabel('Month:'), 6, 2)
        mainLayout.addWidget(self.monthComboBox, 6, 3)
        mainLayout.addWidget(QLabel('Address:'), 7, 0)
        mainLayout.addWidget(self.addressLineEdit, 8, 0, 1, 4)
        mainLayout.addWidget(QLabel('Edition:'), 9, 0)
        mainLayout.addWidget(self.editionLineEdit, 10, 0, 1, 4)
        mainLayout.addWidget(QLabel('Crossref:'), 11, 0)
        mainLayout.addWidget(self.crossrefLineEdit, 12, 0, 1, 4)
        mainLayout.addWidget(QLabel('Note:'), 13, 0)
        mainLayout.addWidget(self.noteLineEdit, 14, 0, 1, 4)
        self.setLayout(mainLayout)

    def userFieldChange(self, text, field):
        self.fields[field] = text
        self.fieldChanged.emit()


class StandardEditor(QWidget):
    fieldChanged = pyqtSignal()

    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path
        self.sourceTag, self.fields = sourceTag, fields
        # FIELDS LINE EDITS
        self.titleLineEdit = QLineEdit(fields['title'])
        self.authorLineEdit = QLineEdit(fields['author'])
        self.organizationLineEdit = QLineEdit(fields['organization'])
        self.institutionLineEdit = QLineEdit(fields['institution'])
        self.languageLineEdit = QLineEdit(fields['language'])
        self.howPublishedLineEdit = QLineEdit(fields['howpublished'])
        self.typeLineEdit = QLineEdit(fields['type'])
        self.numberLineEdit = QLineEdit(fields['number'])
        self.revisionLineEdit = QLineEdit(fields['revision'])
        self.addressLineEdit = QLineEdit(fields['address'])
        self.urlLineEdit = QLineEdit(fields['url'])
        self.yearLineEdit = QLineEdit(fields['year'])
        self.crossrefLineEdit = QLineEdit(fields['crossref'])
        self.noteLineEdit = QLineEdit(fields['note'])
        self.monthComboBox = MonthComboBox(fields['month'])
        # FIELD CHANGES CONNECTS
        self.titleLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'title'))
        self.authorLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'author'))
        self.organizationLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'organization'))
        self.institutionLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'institution'))
        self.languageLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'language'))
        self.howPublishedLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'howpublished'))
        self.typeLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'type'))
        self.numberLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'number'))
        self.revisionLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'revision'))
        self.addressLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'address'))
        self.urlLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'url'))
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
        mainLayout.addWidget(QLabel('Organization:'), 4, 0)
        mainLayout.addWidget(self.organizationLineEdit, 5, 0, 1, 4)
        mainLayout.addWidget(QLabel('Institution:'), 6, 0)
        mainLayout.addWidget(self.institutionLineEdit, 7, 0, 1, 4)
        mainLayout.addWidget(QLabel('Language:'), 8, 0)
        mainLayout.addWidget(self.languageLineEdit, 9, 0, 1, 4)
        mainLayout.addWidget(QLabel('Howpublished:'), 10, 0)
        mainLayout.addWidget(self.howPublishedLineEdit, 11, 0, 1, 4)
        mainLayout.addWidget(QLabel('Type:'), 12, 0)
        mainLayout.addWidget(self.typeLineEdit, 13, 0, 1, 4)
        mainLayout.addWidget(QLabel('Number:'), 14, 0)
        mainLayout.addWidget(self.numberLineEdit, 15, 0, 1, 4)
        mainLayout.addWidget(QLabel('Revision:'), 16, 0)
        mainLayout.addWidget(self.revisionLineEdit, 17, 0, 1, 4)
        mainLayout.addWidget(QLabel('Address:'), 18, 0)
        mainLayout.addWidget(self.addressLineEdit, 19, 0, 1, 4)
        mainLayout.addWidget(QLabel('Year:'), 20, 0)
        mainLayout.addWidget(self.yearLineEdit, 20, 1)
        mainLayout.addWidget(QLabel('Month:'), 20, 2)
        mainLayout.addWidget(self.monthComboBox, 20, 3)
        mainLayout.addWidget(QLabel('Url:'), 21, 0)
        mainLayout.addWidget(self.urlLineEdit, 22, 0, 1, 4)
        mainLayout.addWidget(QLabel('Crossref:'), 23, 0)
        mainLayout.addWidget(self.crossrefLineEdit, 24, 0, 1, 4)
        mainLayout.addWidget(QLabel('Note:'), 25, 0)
        mainLayout.addWidget(self.noteLineEdit, 26, 0, 1, 4)
        self.setLayout(mainLayout)

    def userFieldChange(self, text, field):
        self.fields[field] = text
        self.fieldChanged.emit()


class TechReportEditor(QWidget):
    fieldChanged = pyqtSignal()

    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path
        self.sourceTag, self.fields = sourceTag, fields
        # FIELDS LINE EDITS
        self.titleLineEdit = QLineEdit(fields['title'])
        self.authorLineEdit = QLineEdit(fields['author'])
        self.institutionLineEdit = QLineEdit(fields['institution'])
        self.typeLineEdit = QLineEdit(fields['type'])
        self.numberLineEdit = QLineEdit(fields['number'])
        self.addressLineEdit = QLineEdit(fields['address'])
        self.yearLineEdit = QLineEdit(fields['year'])
        self.crossrefLineEdit = QLineEdit(fields['crossref'])
        self.noteLineEdit = QLineEdit(fields['note'])
        self.monthComboBox = MonthComboBox(fields['month'])
        # FIELD CHANGES CONNECTS
        self.titleLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'title'))
        self.authorLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'author'))
        self.institutionLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'institution'))
        self.typeLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'type'))
        self.numberLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'number'))
        self.addressLineEdit.textChanged.connect(lambda text: self.userFieldChange(text, 'address'))
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
        mainLayout.addWidget(QLabel('Institution:'), 4, 0)
        mainLayout.addWidget(self.institutionLineEdit, 5, 0, 1, 4)
        mainLayout.addWidget(QLabel('Year:'), 6, 0)
        mainLayout.addWidget(self.yearLineEdit, 6, 1)
        mainLayout.addWidget(QLabel('Month:'), 6, 2)
        mainLayout.addWidget(self.monthComboBox, 6, 3)
        mainLayout.addWidget(QLabel('Type:'), 7, 0)
        mainLayout.addWidget(self.typeLineEdit, 8, 0, 1, 4)
        mainLayout.addWidget(QLabel('Number:'), 9, 0)
        mainLayout.addWidget(self.numberLineEdit, 10, 0, 1, 4)
        mainLayout.addWidget(QLabel('Address:'), 11, 0)
        mainLayout.addWidget(self.addressLineEdit, 12, 0, 1, 4)
        mainLayout.addWidget(QLabel('Crossref:'), 13, 0)
        mainLayout.addWidget(self.crossrefLineEdit, 14, 0, 1, 4)
        mainLayout.addWidget(QLabel('Note:'), 15, 0)
        mainLayout.addWidget(self.noteLineEdit, 16, 0, 1, 4)
        self.setLayout(mainLayout)

    def userFieldChange(self, text, field):
        self.fields[field] = text
        self.fieldChanged.emit()


######################## FUNCTIONS ########################
def createManualEditor(path, sourceTag, fields):
    return ManualEditor(path, sourceTag, fields)


def createStandardEditor(path, sourceTag, fields):
    return StandardEditor(path, sourceTag, fields)


def createTechReportEditor(path, sourceTag, fields):
    return TechReportEditor(path, sourceTag, fields)
