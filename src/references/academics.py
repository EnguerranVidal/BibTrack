import os
import json
import pandas as pd

# ------------------- PyQt Modules -------------------- #
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# --------------------- Sources ----------------------- #
from src.common.utilities.fileSystem import loadSettings
from src.common.widgets.Widgets import SquareIconButton, IconButton, GeneralFieldsEditor


######################## CLASSES ########################
class ArticleEditor(QWidget):
    def __init__(self, path):
        super().__init__()
        self.currentDir = path
        self.generalFieldsEditor = None
        self.sourceTag, self.fields = None, None
        self.generated = False

    def initialize(self, sourceTag, fields):
        self.sourceTag, self.fields = sourceTag, fields
        self.generated = True
        self.generalFieldsEditor = GeneralFieldsEditor(sourceTag, fields)
        mainLayout = QGridLayout(self)
        mainLayout.addWidget(self.generalFieldsEditor, 0, 0)
        self.setLayout(mainLayout)


class ConferenceEditor(QWidget):
    def __init__(self, path):
        super().__init__()
        self.currentDir = path
        self.generalFieldsEditor = None
        self.sourceTag, self.fields = None, None
        self.generated = False

    def initialize(self, sourceTag, fields):
        self.sourceTag, self.fields = sourceTag, fields
        self.generated = True
        self.generalFieldsEditor = GeneralFieldsEditor(sourceTag, fields)
        mainLayout = QGridLayout(self)
        mainLayout.addWidget(self.generalFieldsEditor, 0, 0)
        self.setLayout(mainLayout)


class InProceedingsEditor(QWidget):
    def __init__(self, path):
        super().__init__()
        self.currentDir = path
        self.generalFieldsEditor = None
        self.sourceTag, self.fields = None, None
        self.generated = False

    def initialize(self, sourceTag, fields):
        self.sourceTag, self.fields = sourceTag, fields
        self.generated = True
        self.generalFieldsEditor = GeneralFieldsEditor(sourceTag, fields)
        mainLayout = QGridLayout(self)
        mainLayout.addWidget(self.generalFieldsEditor, 0, 0)
        self.setLayout(mainLayout)


class MastersThesisEditor(QWidget):
    def __init__(self, path):
        super().__init__()
        self.currentDir = path
        self.generalFieldsEditor = None
        self.sourceTag, self.fields = None, None
        self.generated = False

    def initialize(self, sourceTag, fields):
        self.sourceTag, self.fields = sourceTag, fields
        self.generated = True
        self.generalFieldsEditor = GeneralFieldsEditor(sourceTag, fields)
        mainLayout = QGridLayout(self)
        mainLayout.addWidget(self.generalFieldsEditor, 0, 0)
        self.setLayout(mainLayout)


class ProceedingsEditor(QWidget):
    def __init__(self, path):
        super().__init__()
        self.currentDir = path
        self.generalFieldsEditor = None
        self.sourceTag, self.fields = None, None
        self.generated = False

    def initialize(self, sourceTag, fields):
        self.sourceTag, self.fields = sourceTag, fields
        self.generated = True
        self.generalFieldsEditor = GeneralFieldsEditor(sourceTag, fields)
        mainLayout = QGridLayout(self)
        mainLayout.addWidget(self.generalFieldsEditor, 0, 0)
        self.setLayout(mainLayout)


class PhdThesisEditor(QWidget):
    def __init__(self, path):
        super().__init__()
        self.currentDir = path
        self.generalFieldsEditor = None
        self.sourceTag, self.fields = None, None
        self.generated = False

    def initialize(self, sourceTag, fields):
        self.sourceTag, self.fields = sourceTag, fields
        self.generated = True
        self.generalFieldsEditor = GeneralFieldsEditor(sourceTag, fields)
        mainLayout = QGridLayout(self)
        mainLayout.addWidget(self.generalFieldsEditor, 0, 0)
        self.setLayout(mainLayout)


######################## FUNCTIONS ########################
def createArticleEditor(path):
    return ArticleEditor(path)


def createConferenceEditor(path):
    return ConferenceEditor(path)


def createInProceedingsEditor(path):
    return InProceedingsEditor(path)


def createMastersThesisEditor(path):
    return MastersThesisEditor(path)


def createPhdThesisEditor(path):
    return PhdThesisEditor(path)


def createProceedingsEditor(path):
    return ProceedingsEditor(path)


