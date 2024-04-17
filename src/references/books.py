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
class BookEditor(QWidget):
    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path
        self.sourceTag = sourceTag
        # FIELDS LINE EDITS
        self.titleLineEdit = QLineEdit(fields['FIELDS']['title'])
        self.authorLineEdit = QLineEdit(fields['FIELDS']['author'])
        self.publisherLineEdit = QLineEdit(fields['FIELDS']['publisher'])
        self.yearLineEdit = QLineEdit(fields['FIELDS']['year'])
        self.volumeLineEdit = QLineEdit(fields['FIELDS']['volume'])
        self.seriesLineEdit = QLineEdit(fields['FIELDS']['series'])
        self.addressLineEdit = QLineEdit(fields['FIELDS']['address'])
        self.crossrefLineEdit = QLineEdit(fields['FIELDS']['crossref'])
        self.noteLineEdit = QLineEdit(fields['FIELDS']['note'])
        self.editionComboBox = EditionComboBox(fields['FIELDS']['edition'])
        self.monthComboBox = MonthComboBox(fields['FIELDS']['month'])
        # MAIN LAYOUT CREATION
        mainLayout = QGridLayout()
        mainLayout.addWidget(QLabel('Title:'), 0, 0)
        mainLayout.addWidget(self.titleLineEdit, 1, 0, 1, 4)
        mainLayout.addWidget(QLabel('Authors:'), 2, 0)
        mainLayout.addWidget(self.authorLineEdit, 3, 0, 1, 4)
        mainLayout.addWidget(QLabel('Publisher:'), 4, 0)
        mainLayout.addWidget(self.publisherLineEdit, 5, 0, 1, 4)
        mainLayout.addWidget(QLabel('Year:'), 6, 0)
        mainLayout.addWidget(self.yearLineEdit, 6, 1)
        mainLayout.addWidget(QLabel('Month:'), 6, 2)
        mainLayout.addWidget(self.monthComboBox, 6, 3)
        mainLayout.addWidget(QLabel('Volume:'), 7, 0)
        mainLayout.addWidget(self.volumeLineEdit, 8, 0, 1, 4)
        mainLayout.addWidget(QLabel('Series:'), 9, 0)
        mainLayout.addWidget(self.seriesLineEdit, 10, 0, 1, 4)
        mainLayout.addWidget(QLabel('Address:'), 11, 0)
        mainLayout.addWidget(self.addressLineEdit, 12, 0, 1, 4)
        mainLayout.addWidget(QLabel('Edition:'), 13, 0)
        mainLayout.addWidget(self.editionComboBox, 13, 1)
        mainLayout.addWidget(QLabel('Crossref:'), 14, 0)
        mainLayout.addWidget(self.crossrefLineEdit, 15, 0, 1, 4)
        mainLayout.addWidget(QLabel('Note:'), 16, 0)
        mainLayout.addWidget(self.noteLineEdit, 17, 0, 1, 4)
        self.setLayout(mainLayout)


class BookletEditor(QWidget):
    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path
        self.sourceTag = sourceTag
        # FIELDS LINE EDITS
        self.titleLineEdit = QLineEdit(fields['FIELDS']['title'])
        self.authorLineEdit = QLineEdit(fields['FIELDS']['author'])
        self.howPublishedLineEdit = QLineEdit(fields['FIELDS']['howpublished'])
        self.yearLineEdit = QLineEdit(fields['FIELDS']['year'])
        self.addressLineEdit = QLineEdit(fields['FIELDS']['address'])
        self.crossrefLineEdit = QLineEdit(fields['FIELDS']['crossref'])
        self.noteLineEdit = QLineEdit(fields['FIELDS']['note'])
        self.monthComboBox = MonthComboBox(fields['FIELDS']['month'])
        # MAIN LAYOUT CREATION
        mainLayout = QGridLayout()
        mainLayout.addWidget(QLabel('Title:'), 0, 0)
        mainLayout.addWidget(self.titleLineEdit, 1, 0, 1, 4)
        mainLayout.addWidget(QLabel('Authors:'), 2, 0)
        mainLayout.addWidget(self.authorLineEdit, 3, 0, 1, 4)
        mainLayout.addWidget(QLabel('How Published:'), 4, 0)
        mainLayout.addWidget(self.howPublishedLineEdit, 5, 0, 1, 4)
        mainLayout.addWidget(QLabel('Year:'), 6, 0)
        mainLayout.addWidget(self.yearLineEdit, 6, 1)
        mainLayout.addWidget(QLabel('Month:'), 6, 2)
        mainLayout.addWidget(self.monthComboBox, 6, 3)
        mainLayout.addWidget(QLabel('Address:'), 7, 0)
        mainLayout.addWidget(self.addressLineEdit, 8, 0, 1, 4)
        mainLayout.addWidget(QLabel('Crossref:'), 9, 0)
        mainLayout.addWidget(self.crossrefLineEdit, 10, 0, 1, 4)
        mainLayout.addWidget(QLabel('Note:'), 11, 0)
        mainLayout.addWidget(self.noteLineEdit, 12, 0, 1, 4)
        self.setLayout(mainLayout)


class InBookEditor(QWidget):
    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path
        self.sourceTag = sourceTag
        # FIELDS LINE EDITS
        self.titleLineEdit = QLineEdit(fields['FIELDS']['title'])
        self.authorLineEdit = QLineEdit(fields['FIELDS']['author'])
        self.chapterLineEdit = QLineEdit(fields['FIELDS']['chapter'])
        self.publisherLineEdit = QLineEdit(fields['FIELDS']['publisher'])
        self.yearLineEdit = QLineEdit(fields['FIELDS']['year'])
        self.addressLineEdit = QLineEdit(fields['FIELDS']['address'])
        self.volumeLineEdit = QLineEdit(fields['FIELDS']['volume'])
        self.seriesLineEdit = QLineEdit(fields['FIELDS']['series'])
        self.typeLineEdit = QLineEdit(fields['FIELDS']['type'])
        self.addressLineEdit = QLineEdit(fields['FIELDS']['address'])
        self.crossrefLineEdit = QLineEdit(fields['FIELDS']['crossref'])
        self.noteLineEdit = QLineEdit(fields['FIELDS']['note'])
        self.editionComboBox = EditionComboBox(fields['FIELDS']['edition'])
        self.monthComboBox = MonthComboBox(fields['FIELDS']['month'])
        # MAIN LAYOUT CREATION
        mainLayout = QGridLayout()
        mainLayout.addWidget(QLabel('Title:'), 0, 0)
        mainLayout.addWidget(self.titleLineEdit, 1, 0, 1, 4)
        mainLayout.addWidget(QLabel('Authors:'), 2, 0)
        mainLayout.addWidget(self.authorLineEdit, 3, 0, 1, 4)
        mainLayout.addWidget(QLabel('Chapter:'), 4, 0)
        mainLayout.addWidget(self.chapterLineEdit, 5, 0, 1, 4)
        mainLayout.addWidget(QLabel('Publisher:'), 6, 0)
        mainLayout.addWidget(self.publisherLineEdit, 7, 0, 1, 4)
        mainLayout.addWidget(QLabel('Year:'), 8, 0)
        mainLayout.addWidget(self.yearLineEdit, 8, 1)
        mainLayout.addWidget(QLabel('Month:'), 8, 2)
        mainLayout.addWidget(self.monthComboBox, 8, 3)
        mainLayout.addWidget(QLabel('Volume:'), 9, 0)
        mainLayout.addWidget(self.volumeLineEdit, 10, 0, 1, 4)
        mainLayout.addWidget(QLabel('Series:'), 11, 0)
        mainLayout.addWidget(self.seriesLineEdit, 12, 0, 1, 4)
        mainLayout.addWidget(QLabel('Type:'), 13, 0)
        mainLayout.addWidget(self.typeLineEdit, 14, 0, 1, 4)
        mainLayout.addWidget(QLabel('Address:'), 15, 0)
        mainLayout.addWidget(self.addressLineEdit, 16, 0, 1, 4)
        mainLayout.addWidget(QLabel('Edition:'), 17, 0)
        mainLayout.addWidget(self.editionComboBox, 17, 1)
        mainLayout.addWidget(QLabel('Crossref:'), 18, 0)
        mainLayout.addWidget(self.crossrefLineEdit, 19, 0, 1, 4)
        mainLayout.addWidget(QLabel('Note:'), 20, 0)
        mainLayout.addWidget(self.noteLineEdit, 21, 0, 1, 4)
        self.setLayout(mainLayout)


class InCollectionEditor(QWidget):
    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path
        self.sourceTag = sourceTag
        # FIELDS LINE EDITS
        self.titleLineEdit = QLineEdit(fields['FIELDS']['title'])
        self.authorLineEdit = QLineEdit(fields['FIELDS']['author'])
        self.bookTitleLineEdit = QLineEdit(fields['FIELDS']['booktitle'])
        self.publisherLineEdit = QLineEdit(fields['FIELDS']['publisher'])
        self.yearLineEdit = QLineEdit(fields['FIELDS']['year'])
        self.editorLineEdit = QLineEdit(fields['FIELDS']['editor'])
        self.volumeLineEdit = QLineEdit(fields['FIELDS']['volume'])
        self.seriesLineEdit = QLineEdit(fields['FIELDS']['series'])
        self.typeLineEdit = QLineEdit(fields['FIELDS']['type'])
        self.chapterLineEdit = QLineEdit(fields['FIELDS']['chapter'])
        self.pagesLineEdit = QLineEdit(fields['FIELDS']['pages'])
        self.addressLineEdit = QLineEdit(fields['FIELDS']['address'])
        self.organizationLineEdit = QLineEdit(fields['FIELDS']['organization'])
        self.crossrefLineEdit = QLineEdit(fields['FIELDS']['crossref'])
        self.noteLineEdit = QLineEdit(fields['FIELDS']['note'])
        self.editionComboBox = EditionComboBox(fields['FIELDS']['edition'])
        self.monthComboBox = MonthComboBox(fields['FIELDS']['month'])
        # MAIN LAYOUT CREATION
        mainLayout = QGridLayout()
        mainLayout.addWidget(QLabel('Title:'), 0, 0)
        mainLayout.addWidget(self.titleLineEdit, 1, 0, 1, 4)
        mainLayout.addWidget(QLabel('Authors:'), 2, 0)
        mainLayout.addWidget(self.authorLineEdit, 3, 0, 1, 4)
        mainLayout.addWidget(QLabel('Book Title:'), 4, 0)
        mainLayout.addWidget(self.bookTitleLineEdit, 5, 0, 1, 4)
        mainLayout.addWidget(QLabel('Publisher:'), 6, 0)
        mainLayout.addWidget(self.publisherLineEdit, 7, 0, 1, 4)
        mainLayout.addWidget(QLabel('Year:'), 8, 0)
        mainLayout.addWidget(self.yearLineEdit, 8, 1)
        mainLayout.addWidget(QLabel('Month:'), 8, 2)
        mainLayout.addWidget(self.monthComboBox, 8, 3)
        mainLayout.addWidget(QLabel('Editor:'), 9, 0)
        mainLayout.addWidget(self.editorLineEdit, 10, 0, 1, 4)
        mainLayout.addWidget(QLabel('Volume:'), 11, 0)
        mainLayout.addWidget(self.volumeLineEdit, 12, 0, 1, 4)
        mainLayout.addWidget(QLabel('Series:'), 13, 0)
        mainLayout.addWidget(self.seriesLineEdit, 14, 0, 1, 4)
        mainLayout.addWidget(QLabel('Type:'), 15, 0)
        mainLayout.addWidget(self.typeLineEdit, 16, 0, 1, 4)
        mainLayout.addWidget(QLabel('Chapter:'), 15, 0)
        mainLayout.addWidget(self.chapterLineEdit, 16, 0, 1, 4)
        mainLayout.addWidget(QLabel('Pages:'), 17, 0)
        mainLayout.addWidget(self.pagesLineEdit, 18, 0, 1, 4)
        mainLayout.addWidget(QLabel('Address:'), 17, 0)
        mainLayout.addWidget(self.addressLineEdit, 18, 0, 1, 4)
        mainLayout.addWidget(QLabel('Organization:'), 17, 0)
        mainLayout.addWidget(self.organizationLineEdit, 18, 0, 1, 4)
        mainLayout.addWidget(QLabel('Edition:'), 19, 0)
        mainLayout.addWidget(self.editionComboBox, 19, 1)
        mainLayout.addWidget(QLabel('Crossref:'), 20, 0)
        mainLayout.addWidget(self.crossrefLineEdit, 21, 0, 1, 4)
        mainLayout.addWidget(QLabel('Note:'), 22, 0)
        mainLayout.addWidget(self.noteLineEdit, 23, 0, 1, 4)
        self.setLayout(mainLayout)


######################## FUNCTIONS ########################
def createBookEditor(path, sourceTag, fields):
    return BookEditor(path, sourceTag, fields)


def createBookletEditor(path, sourceTag, fields):
    return BookletEditor(path, sourceTag, fields)


def createInBookEditor(path, sourceTag, fields):
    return InBookEditor(path, sourceTag, fields)


def createInCollectionEditor(path, sourceTag, fields):
    return InCollectionEditor(path, sourceTag, fields)
