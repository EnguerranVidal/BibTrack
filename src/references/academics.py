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
class ArticleEditor(QWidget):
    def __init__(self, path):
        super().__init__()
        self.currentDir = path
        self.fields = None
        self.generated = False

    def initialize(self, fields):
        self.fields = fields


class ConferenceEditor(QWidget):
    def __init__(self, path):
        super().__init__()
        self.currentDir = path
        self.fields = None
        self.generated = False

    def initialize(self, fields):
        self.fields = fields


class InProceedingsEditor(QWidget):
    def __init__(self, path):
        super().__init__()
        self.currentDir = path
        self.fields = None
        self.generated = False

    def initialize(self, fields):
        self.fields = fields


class MastersThesisEditor(QWidget):
    def __init__(self, path):
        super().__init__()
        self.currentDir = path
        self.fields = None
        self.generated = False

    def initialize(self, fields):
        self.fields = fields


class ProceedingsEditor(QWidget):
    def __init__(self, path):
        super().__init__()
        self.currentDir = path
        self.fields = None
        self.generated = False

    def initialize(self, fields):
        self.fields = fields


class PhdThesisEditor(QWidget):
    def __init__(self, path):
        super().__init__()
        self.currentDir = path
        self.fields = None
        self.generated = False

    def initialize(self, fields):
        self.fields = fields


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



