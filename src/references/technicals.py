import os
import json
import pandas as pd

# ------------------- PyQt Modules -------------------- #
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# --------------------- Sources ----------------------- #
from src.common.utilities.fileSystem import loadSettings
from src.common.widgets.Widgets import SquareIconButton, IconButton


######################## CLASSES ########################
class ManualEditor(QWidget):
    def __init__(self, path):
        super().__init__()
        self.currentDir = path
        self.fields = None
        self.generated = False

    def initialize(self, fields):
        self.fields = fields


class StandardEditor(QWidget):
    def __init__(self, path):
        super().__init__()
        self.currentDir = path
        self.fields = None
        self.generated = False

    def initialize(self, fields):
        self.fields = fields


class TechReportEditor(QWidget):
    def __init__(self, path):
        super().__init__()
        self.currentDir = path
        self.fields = None
        self.generated = False

    def initialize(self, fields):
        self.fields = fields


######################## FUNCTIONS ########################
def createManualEditor(path):
    return ManualEditor(path)


def createStandardEditor(path):
    return StandardEditor(path)


def createTechReportEditor(path):
    return TechReportEditor(path)
