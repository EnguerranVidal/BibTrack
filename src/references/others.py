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
class OnlineEditor(QWidget):
    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path
        self.sourceTag = sourceTag
        # FIELDS LINE EDITS
        self.titleLineEdit = QLineEdit(fields['FIELDS']['title'])
        self.authorLineEdit = QLineEdit(fields['FIELDS']['author'])
        self.yearLineEdit = QLineEdit(fields['FIELDS']['year'])
        self.monthComboBox = MonthComboBox(fields['FIELDS']['month'])
        self.urlLineEdit = QLineEdit(fields['FIELDS']['url'])
        self.noteLineEdit = QLineEdit(fields['FIELDS']['note'])
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


class MiscEditor(QWidget):
    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path
        self.sourceTag = sourceTag
        # FIELDS LINE EDITS
        self.titleLineEdit = QLineEdit(fields['FIELDS']['title'])
        self.authorLineEdit = QLineEdit(fields['FIELDS']['author'])
        self.yearLineEdit = QLineEdit(fields['FIELDS']['year'])
        self.monthComboBox = MonthComboBox(fields['FIELDS']['month'])
        self.howPublishedLineEdit = QLineEdit(fields['FIELDS']['howpublished'])
        self.crossrefLineEdit = QLineEdit(fields['FIELDS']['crossref'])
        self.noteLineEdit = QLineEdit(fields['FIELDS']['note'])
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


class UnpublishedEditor(QWidget):
    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path
        self.sourceTag = sourceTag
        # FIELDS LINE EDITS
        self.titleLineEdit = QLineEdit(fields['FIELDS']['title'])
        self.authorLineEdit = QLineEdit(fields['FIELDS']['author'])
        self.yearLineEdit = QLineEdit(fields['FIELDS']['year'])
        self.monthComboBox = MonthComboBox(fields['FIELDS']['month'])
        self.crossrefLineEdit = QLineEdit(fields['FIELDS']['crossref'])
        self.noteLineEdit = QLineEdit(fields['FIELDS']['note'])
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


class UrlEditor(QWidget):
    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path
        self.sourceTag = sourceTag
        # FIELDS LINE EDITS
        self.authorLineEdit = QLineEdit(fields['FIELDS']['author'])
        self.seriesLineEdit = QLineEdit(fields['FIELDS']['series'])
        self.yearLineEdit = QLineEdit(fields['FIELDS']['year'])
        self.monthComboBox = MonthComboBox(fields['FIELDS']['month'])
        self.editionComboBox = EditionComboBox(fields['FIELDS']['edition'])
        self.crossrefLineEdit = QLineEdit(fields['FIELDS']['crossref'])
        self.noteLineEdit = QLineEdit(fields['FIELDS']['note'])
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


######################## FUNCTIONS ########################
def createOnlineEditor(path, sourceTag, fields):
    return OnlineEditor(path, sourceTag, fields)


def createMiscEditor(path, sourceTag, fields):
    return MiscEditor(path, sourceTag, fields)


def createUnpublishedEditor(path, sourceTag, fields):
    return UnpublishedEditor(path, sourceTag, fields)


def createUrlEditor(path, sourceTag, fields):
    return UrlEditor(path, sourceTag, fields)