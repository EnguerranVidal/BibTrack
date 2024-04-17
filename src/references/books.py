import os
import json
import pandas as pd

# ------------------- PyQt Modules -------------------- #
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# --------------------- Sources ----------------------- #
from src.common.utilities.fileSystem import loadSettings
from src.common.widgets.widgets import SquareIconButton, IconButton



######################## CLASSES ########################
class BookEditor(QWidget):
    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path


class BookletEditor(QWidget):
    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path


class InBookEditor(QWidget):
    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path


class InCollectionEditor(QWidget):
    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path


######################## FUNCTIONS ########################
def createBookEditor(path, sourceTag, fields):
    return BookEditor(path, sourceTag, fields)


def createBookletEditor(path, sourceTag, fields):
    return BookletEditor(path, sourceTag, fields)


def createInBookEditor(path, sourceTag, fields):
    return InBookEditor(path, sourceTag, fields)


def createInCollectionEditor(path, sourceTag, fields):
    return InCollectionEditor(path, sourceTag, fields)
