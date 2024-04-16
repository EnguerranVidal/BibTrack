import os
import json
import pandas as pd

# ------------------- PyQt Modules -------------------- #
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# --------------------- Sources ----------------------- #
from src.common.utilities.fileSystem import loadSettings
from src.common.widgets.Widgets import MonthComboBox


######################## CLASSES ########################
class ArticleEditor(QWidget):
    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path
        self.monthComboBox = MonthComboBox(fields['FIELDS']['month'])

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.monthComboBox, 0, 0)
        self.setLayout(mainLayout)


class ConferenceEditor(QWidget):
    returnClicked = pyqtSignal()

    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path


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



