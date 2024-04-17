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
    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path
        self.sourceTag = sourceTag
        # FIELDS LINE EDITS
        self.titleLineEdit = QLineEdit(fields['FIELDS']['title'])
        self.authorLineEdit = QLineEdit(fields['FIELDS']['author'])
        self.journalLineEdit = QLineEdit(fields['FIELDS']['journal'])
        self.yearLineEdit = QLineEdit(fields['FIELDS']['year'])
        self.volumeLineEdit = QLineEdit(fields['FIELDS']['volume'])
        self.numberLineEdit = QLineEdit(fields['FIELDS']['number'])
        self.pagesLineEdit = QLineEdit(fields['FIELDS']['pages'])
        self.crossrefLineEdit = QLineEdit(fields['FIELDS']['crossref'])
        self.noteLineEdit = QLineEdit(fields['FIELDS']['note'])
        self.monthComboBox = MonthComboBox(fields['FIELDS']['month'])
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


class ConferenceEditor(QWidget):
    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path
        self.sourceTag = sourceTag
        # FIELDS LINE EDITS
        self.titleLineEdit = QLineEdit(fields['FIELDS']['title'])
        self.authorLineEdit = QLineEdit(fields['FIELDS']['author'])
        self.bookTitleLineEdit = QLineEdit(fields['FIELDS']['booktitle'])
        self.yearLineEdit = QLineEdit(fields['FIELDS']['year'])
        self.editorLineEdit = QLineEdit(fields['FIELDS']['editor'])
        self.volumeLineEdit = QLineEdit(fields['FIELDS']['volume'])
        self.seriesLineEdit = QLineEdit(fields['FIELDS']['series'])
        self.pagesLineEdit = QLineEdit(fields['FIELDS']['pages'])
        self.addressLineEdit = QLineEdit(fields['FIELDS']['address'])
        self.organizationLineEdit = QLineEdit(fields['FIELDS']['organization'])
        self.publisherLineEdit = QLineEdit(fields['FIELDS']['publisher'])
        self.crossrefLineEdit = QLineEdit(fields['FIELDS']['crossref'])
        self.noteLineEdit = QLineEdit(fields['FIELDS']['note'])
        self.monthComboBox = MonthComboBox(fields['FIELDS']['month'])
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


class InProceedingsEditor(QWidget):
    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path


class MastersThesisEditor(QWidget):
    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path


class ProceedingsEditor(QWidget):
    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path


class PhdThesisEditor(QWidget):
    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path


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



