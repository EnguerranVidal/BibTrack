import os
import json
import pandas as pd

# ------------------- PyQt Modules -------------------- #
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# --------------------- Sources ----------------------- #
from src.common.utilities.fileSystem import loadSettings
from src.common.widgets.fields import MonthComboBox, EditionComboBox
from src.common.widgets.widgets import SquareIconButton, IconButton


######################## CLASSES ########################
class ManualEditor(QWidget):
    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path
        self.sourceTag = sourceTag
        # FIELDS LINE EDITS
        self.titleLineEdit = QLineEdit(fields['FIELDS']['title'])
        self.authorLineEdit = QLineEdit(fields['FIELDS']['author'])
        self.organizationLineEdit = QLineEdit(fields['FIELDS']['organization'])
        self.addressLineEdit = QLineEdit(fields['FIELDS']['address'])
        self.editionLineEdit = QLineEdit(fields['FIELDS']['edition'])
        self.yearLineEdit = QLineEdit(fields['FIELDS']['year'])
        self.crossrefLineEdit = QLineEdit(fields['FIELDS']['crossref'])
        self.noteLineEdit = QLineEdit(fields['FIELDS']['note'])
        self.monthComboBox = MonthComboBox(fields['FIELDS']['month'])
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


class StandardEditor(QWidget):
    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path
        self.sourceTag = sourceTag
        # FIELDS LINE EDITS
        self.titleLineEdit = QLineEdit(fields['FIELDS']['title'])
        self.authorLineEdit = QLineEdit(fields['FIELDS']['author'])
        self.organizationLineEdit = QLineEdit(fields['FIELDS']['organization'])
        self.institutionLineEdit = QLineEdit(fields['FIELDS']['institution'])
        self.languageLineEdit = QLineEdit(fields['FIELDS']['language'])
        self.howPublishedLineEdit = QLineEdit(fields['FIELDS']['howpublished'])
        self.typeLineEdit = QLineEdit(fields['FIELDS']['type'])
        self.numberLineEdit = QLineEdit(fields['FIELDS']['number'])
        self.revisionLineEdit = QLineEdit(fields['FIELDS']['revision'])
        self.addressLineEdit = QLineEdit(fields['FIELDS']['address'])
        self.urlLineEdit = QLineEdit(fields['FIELDS']['url'])
        self.yearLineEdit = QLineEdit(fields['FIELDS']['year'])
        self.crossrefLineEdit = QLineEdit(fields['FIELDS']['crossref'])
        self.noteLineEdit = QLineEdit(fields['FIELDS']['note'])
        self.monthComboBox = MonthComboBox(fields['FIELDS']['month'])
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


class TechReportEditor(QWidget):
    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path
        self.sourceTag = sourceTag
        # FIELDS LINE EDITS
        self.titleLineEdit = QLineEdit(fields['FIELDS']['title'])
        self.authorLineEdit = QLineEdit(fields['FIELDS']['author'])
        self.institutionLineEdit = QLineEdit(fields['FIELDS']['institution'])
        self.typeLineEdit = QLineEdit(fields['FIELDS']['type'])
        self.numberLineEdit = QLineEdit(fields['FIELDS']['number'])
        self.addressLineEdit = QLineEdit(fields['FIELDS']['address'])
        self.yearLineEdit = QLineEdit(fields['FIELDS']['year'])
        self.crossrefLineEdit = QLineEdit(fields['FIELDS']['crossref'])
        self.noteLineEdit = QLineEdit(fields['FIELDS']['note'])
        self.monthComboBox = MonthComboBox(fields['FIELDS']['month'])
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


######################## FUNCTIONS ########################
def createManualEditor(path, sourceTag, fields):
    return ManualEditor(path, sourceTag, fields)


def createStandardEditor(path, sourceTag, fields):
    return StandardEditor(path, sourceTag, fields)


def createTechReportEditor(path, sourceTag, fields):
    return TechReportEditor(path, sourceTag, fields)
