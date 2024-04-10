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
class BookEditor(QWidget):
    def __init__(self, path):
        super().__init__()
        self.currentDir = path
        self.fields = None
        self.generated = False

    def initialize(self, fields):
        self.fields = fields


class BookletEditor(QWidget):
    def __init__(self, path):
        super().__init__()
        self.currentDir = path
        self.fields = None
        self.generated = False

    def initialize(self, fields):
        self.fields = fields


class InBookEditor(QWidget):
    def __init__(self, path):
        super().__init__()
        self.currentDir = path
        self.fields = None
        self.generated = False

    def initialize(self, fields):
        self.fields = fields

class InCollectionEditor(QWidget):
    def __init__(self, path):
        super().__init__()
        self.currentDir = path
        self.fields = None
        self.generated = False

    def initialize(self, fields):
        self.fields = fields


######################## FUNCTIONS ########################
def createBookEditor(path):
    return BookEditor(path)


def createBookletEditor(path):
    return BookletEditor(path)


def createInBookEditor(path):
    return InBookEditor(path)


def createInCollectionEditor(path):
    return InCollectionEditor(path)
