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
class ManualEditor(QWidget):
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


class StandardEditor(QWidget):
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


class TechReportEditor(QWidget):
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
def createManualEditor(path):
    return ManualEditor(path)


def createStandardEditor(path):
    return StandardEditor(path)


def createTechReportEditor(path):
    return TechReportEditor(path)
