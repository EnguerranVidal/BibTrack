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
class OnlineEditor(QWidget):
    def __init__(self, path):
        super().__init__()
        self.currentDir = path
        self.fields = None
        self.generated = False

    def initialize(self, fields):
        self.fields = fields


class MiscEditor(QWidget):
    def __init__(self, path):
        super().__init__()
        self.currentDir = path
        self.fields = None
        self.generated = False

    def initialize(self, fields):
        self.fields = fields


class UnpublishedEditor(QWidget):
    def __init__(self, path):
        super().__init__()
        self.currentDir = path
        self.fields = None
        self.generated = False

    def initialize(self, fields):
        self.fields = fields


class UrlEditor(QWidget):
    def __init__(self, path):
        super().__init__()
        self.currentDir = path
        self.fields = None
        self.generated = False

    def initialize(self, fields):
        self.fields = fields


######################## FUNCTIONS ########################
def createOnlineEditor(path):
    return OnlineEditor(path)


def createMiscEditor(path):
    return MiscEditor(path)


def createUnpublishedEditor(path):
    return UnpublishedEditor(path)


def createUrlEditor(path):
    return UrlEditor(path)