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
    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path


class StandardEditor(QWidget):
    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path


class TechReportEditor(QWidget):
    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path


######################## FUNCTIONS ########################
def createManualEditor(path, sourceTag, fields):
    return ManualEditor(path, sourceTag, fields)


def createStandardEditor(path, sourceTag, fields):
    return StandardEditor(path, sourceTag, fields)


def createTechReportEditor(path, sourceTag, fields):
    return TechReportEditor(path, sourceTag, fields)
