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
class OnlineEditor(QWidget):
    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path


class MiscEditor(QWidget):
    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path


class UnpublishedEditor(QWidget):
    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path


class UrlEditor(QWidget):
    def __init__(self, path, sourceTag, fields):
        super().__init__()
        self.currentDir = path


######################## FUNCTIONS ########################
def createOnlineEditor(path, sourceTag, fields):
    return OnlineEditor(path, sourceTag, fields)


def createMiscEditor(path, sourceTag, fields):
    return MiscEditor(path, sourceTag, fields)


def createUnpublishedEditor(path, sourceTag, fields):
    return UnpublishedEditor(path, sourceTag, fields)


def createUrlEditor(path, sourceTag, fields):
    return UrlEditor(path, sourceTag, fields)