######################## IMPORTS ########################
import os
import time
from functools import partial

import qdarktheme

# ------------------- PyQt Modules -------------------- #
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# --------------------- Sources ----------------------- #
from src.common.utilities.fileSystem import loadSettings, saveSettings
from src.common.widgets.Widgets import AboutDialog
from src.references.general import NewBibTrackWindow, BibEditor


######################## CLASSES ########################
class BibTrackGui(QMainWindow):
    def __init__(self, path):
        super().__init__()
        self.currentDir = path
        self.hide()
        self.bibTracksPath = os.path.join(self.currentDir, "bibtracks")
        self.setGeometry(200, 200, 1000, 500)
        self.setWindowTitle('BibTrack')
        self.settings = loadSettings("settings")
        if self.settings['DARK_THEME']:
            qdarktheme.setup_theme('dark', additional_qss="QToolTip {color: black;}")
        else:
            qdarktheme.setup_theme('light')
        self.icons = {}
        self.bibEditor = None
        if self.settings['CURRENT_BIB_TRACK']:
            self.bibEditor = BibEditor(self.settings['CURRENT_BIB_TRACK'])
            self.setCentralWidget(self.bibEditor)
            self.bibEditor.tracker.saveState()

    def initializeUI(self):
        self._checkEnvironment()
        self._createIcons()
        self._createActions()
        self._createMenuBar()
        self._createToolBars()
        self._populateFileMenu()

    def _checkEnvironment(self):
        if not os.path.exists(self.bibTracksPath):
            os.mkdir(self.bibTracksPath)

    def _createIcons(self):
        themeFolder = 'dark-theme' if self.settings['DARK_THEME'] else 'light-theme'
        iconPath = os.path.join(self.currentDir, f'src/icons/{themeFolder}')
        self.icons['NEW_WINDOW'] = QIcon(os.path.join(iconPath, 'icons8-new-window-96.png'))
        self.icons['OPEN_IN_BROWSER'] = QIcon(os.path.join(iconPath, 'icons8-open-in-browser-96.png'))
        self.icons['SAVE'] = QIcon(os.path.join(iconPath, 'icons8-save-96.png'))
        self.icons['CLOSE_WINDOW'] = QIcon(os.path.join(iconPath, 'icons8-close-window-96.png'))
        self.icons['DOWNLOAD'] = QIcon(os.path.join(iconPath, 'icons8-download-96.png'))
        self.icons['ADD_NEW'] = QIcon(os.path.join(iconPath, 'icons8-add-new-96.png'))
        self.icons['GITHUB'] = QIcon(os.path.join(iconPath, 'icons8-github-96.png'))
        self.icons['HELP'] = QIcon(os.path.join(iconPath, 'icons8-help-96.png'))

    def _createActions(self):
        ########### FILE ###########
        # New Bibliography
        self.newBiblioAct = QAction('&New Biblio', self)
        self.newBiblioAct.setStatusTip('Create New Bibliography')
        self.newBiblioAct.setIcon(self.icons['NEW_WINDOW'])
        self.newBiblioAct.setShortcut('Ctrl+N')
        self.newBiblioAct.triggered.connect(self.newBiblioTrack)
        # Open Bibliography
        self.openBiblioAct = QAction('&Open Biblio', self)
        self.openBiblioAct.setStatusTip('Open Bibliography')
        self.openBiblioAct.setIcon(self.icons['OPEN_IN_BROWSER'])
        self.openBiblioAct.setShortcut('Ctrl+N')
        self.openBiblioAct.triggered.connect(self.openBiblioTrack)
        # Save Bibliography
        self.saveBiblioAct = QAction('&Save', self)
        self.saveBiblioAct.setStatusTip('Save Bibliography')
        self.saveBiblioAct.setIcon(self.icons['SAVE'])
        self.saveBiblioAct.setShortcut('Ctrl+S')
        self.saveBiblioAct.triggered.connect(self.saveBibTrack)
        # Save As Bibliography
        self.saveAsBiblioAct = QAction('&Save As', self)
        self.saveAsBiblioAct.setStatusTip('Save Bibliography As...')
        self.saveAsBiblioAct.triggered.connect(self.saveAsBibTrack)
        # Import BibTeX
        self.importBibtexAct = QAction('&Import BibTeX', self)
        self.importBibtexAct.setStatusTip('Import BibTeX')
        self.importBibtexAct.setIcon(self.icons['DOWNLOAD'])
        self.importBibtexAct.triggered.connect(self.importBibtex)
        # Export BibTeX
        self.exportBibtexAct = QAction('&Export to BibTeX', self)
        self.exportBibtexAct.setStatusTip('Export to BibTeX')
        self.exportBibtexAct.triggered.connect(self.exportToBibtex)
        # Exit
        self.exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        self.exitAct.setShortcut('Ctrl+Q')
        self.exitAct.setIcon(self.icons['CLOSE_WINDOW'])
        self.exitAct.setStatusTip('Exit application')
        self.exitAct.triggered.connect(self.close)
        ########### HELP ###########
        # Visit GitHub Page
        self.githubAct = QAction('&Visit GitHub', self)
        self.githubAct.setIcon(self.icons['GITHUB'])
        self.githubAct.setStatusTip('Visit GitHub Page')
        self.githubAct.triggered.connect(self.openGithub)

        ########### HELP ###########
        # Visit GitHub Page
        self.githubAct = QAction('&Visit GitHub', self)
        self.githubAct.setIcon(self.icons['GITHUB'])
        self.githubAct.setStatusTip('Visit GitHub Page')
        self.githubAct.triggered.connect(self.openGithub)
        # Open About Page
        self.aboutAct = QAction('&About', self)
        self.aboutAct.setIcon(self.icons['HELP'])
        self.aboutAct.setStatusTip('About This Software')
        self.aboutAct.triggered.connect(self.openAbout)

    def _createMenuBar(self):
        self.menubar = self.menuBar()

        ###  FILE MENU  ###
        self.fileMenu = self.menubar.addMenu('&File')
        self.fileMenu.addAction(self.newBiblioAct)
        self.fileMenu.addAction(self.openBiblioAct)
        self.recentMenu = QMenu('&Recent', self)
        self.recentMenu.aboutToShow.connect(self._populateRecentMenu)

        self.fileMenu.addMenu(self.recentMenu)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.saveBiblioAct)
        self.fileMenu.addAction(self.saveAsBiblioAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.importBibtexAct)
        self.fileMenu.addAction(self.exportBibtexAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)
        self.fileMenu.aboutToShow.connect(self._populateFileMenu)
        ###  SOURCES MENU  ###
        self.sourcesMenu = self.menubar.addMenu('&Sources')

        ###  HELP MENU  ###
        self.helpMenu = self.menubar.addMenu('&Help')
        self.helpMenu.addAction(self.githubAct)
        self.helpMenu.addAction(self.aboutAct)

    def _createToolBars(self):
        pass

    def _manageToolBars(self, index):
        pass

    def _populateFileMenu(self):
        if len(self.settings['OPENED_RECENTLY']) == 0:
            self.recentMenu.setDisabled(True)
        else:
            self.recentMenu.setDisabled(False)
        if self.bibEditor is not None and self.bibEditor.tracker.unsavedChanges():
            self.saveBiblioAct.setDisabled(False)
            self.saveAsBiblioAct.setDisabled(False)
            self.exportBibtexAct.setDisabled(False)
        elif self.bibEditor is not None:
            self.saveBiblioAct.setDisabled(True)
            self.saveAsBiblioAct.setDisabled(False)
            self.exportBibtexAct.setDisabled(False)
        else:
            self.saveBiblioAct.setDisabled(True)
            self.saveAsBiblioAct.setDisabled(True)
            self.exportBibtexAct.setDisabled(True)

    def _populateRecentMenu(self):
        self.recentMenu.clear()
        actions = []
        filenames = [os.path.basename(path) for path in self.settings['OPENED_RECENTLY']]
        for filename in filenames:
            action = QAction(filename, self)
            action.triggered.connect(partial(self.openRecentBibTrack, filename))
            actions.append(action)
        self.recentMenu.addActions(actions)

    def newBiblioTrack(self):
        fullPaths = [os.path.join(self.bibTracksPath, entry) for entry in os.listdir(self.bibTracksPath)]
        bibTracks = [os.path.basename(directory) for directory in fullPaths if os.path.isdir(directory)]
        dialog = NewBibTrackWindow(bibTracks=bibTracks)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            name = dialog.nameLineEdit.text()
            if self.bibEditor is not None and self.bibEditor.tracker.unsavedChanges():
                reply = QMessageBox.question(self, 'Unsaved Changes',
                                             'There are unsaved changes. Do you want to save before creating a new BibTrack?',
                                             QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
                if reply == QMessageBox.Save:
                    self.bibEditor.tracker.saveState()
                elif reply == QMessageBox.Cancel:
                    self._populateFileMenu()
                    return
            newBibTrackPath = os.path.join(self.bibTracksPath, name)
            self.bibEditor = BibEditor(newBibTrackPath)
            self.setCentralWidget(self.bibEditor)
            self.bibEditor.tracker.saveState()
            self.addToRecent(newBibTrackPath)
            self.settings['CURRENT_BIB_TRACK'] = newBibTrackPath
            saveSettings(self.settings, 'settings')
        self._populateFileMenu()

    def openBiblioTrack(self):
        if os.path.exists(self.bibTracksPath):
            path = QFileDialog.getExistingDirectory(self, "Select Directory", self.bibTracksPath)
        else:
            path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if os.path.abspath(path) not in [os.path.abspath(self.bibTracksPath), os.path.abspath(self.currentDir)]:
            if self.bibEditor is not None and self.bibEditor.tracker.unsavedChanges():
                reply = QMessageBox.question(self, 'Unsaved Changes',
                                             'There are unsaved changes. Do you want to save before opening?',
                                             QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
                if reply == QMessageBox.Save:
                    self.bibEditor.tracker.saveState()
                elif reply == QMessageBox.Cancel:
                    return
            self.bibEditor = BibEditor(path)
            self.bibEditor.tracker.saveState()
            self.setCentralWidget(self.bibEditor)
            self.addToRecent(path)
            self.settings['CURRENT_BIB_TRACK'] = path
            saveSettings(self.settings, 'settings')
        self._populateFileMenu()

    def openRecentBibTrack(self, folderName):
        filenames = [os.path.basename(path) for path in self.settings['OPENED_RECENTLY']]
        path = self.settings['OPENED_RECENTLY'][filenames.index(folderName)]
        if os.path.exists(path):
            self.bibEditor = BibEditor(path)
            self.bibEditor.tracker.saveState()
            self.setCentralWidget(self.bibEditor)
            self.addToRecent(path)
            self.settings['CURRENT_BIB_TRACK'] = path
            saveSettings(self.settings, 'settings')
        self._populateFileMenu()

    def addToRecent(self, path):
        self.settings['OPENED_RECENTLY'].insert(0, path)
        openedRecently = []
        for i in range(len(self.settings['OPENED_RECENTLY'])):
            if self.settings['OPENED_RECENTLY'][i] not in openedRecently:
                openedRecently.append(self.settings['OPENED_RECENTLY'][i])
        self.settings['OPENED_RECENTLY'] = openedRecently
        if len(self.settings['OPENED_RECENTLY']) == 5:
            self.settings['OPENED_RECENTLY'].pop()
        saveSettings(self.settings, 'settings')

    def saveBibTrack(self):
        self.bibEditor.tracker.saveState()
        self._populateFileMenu()

    def saveAsBibTrack(self):
        if os.path.exists(self.bibTracksPath):
            path = QFileDialog.getExistingDirectory(self, "Select Directory", self.bibTracksPath)
        else:
            path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if os.path.abspath(path) not in [os.path.abspath(self.bibTracksPath), os.path.abspath(self.currentDir)]:
            self.bibEditor.tracker.saveState(path)
            self.addToRecent(path)
            self.settings['CURRENT_BIB_TRACK'] = path
            saveSettings(self.settings, 'settings')
        self._populateFileMenu()

    def importBibtex(self):
        pass

    def exportToBibtex(self):
        pass

    def toggleDarkMode(self):
        self.settings['DARK_THEME'] = not self.settings['DARK_THEME']
        saveSettings(self.settings, 'settings')
        themeText = 'Light Theme' if self.settings['DARK_THEME'] else 'Dark Theme'
        self.darkModeAct.setText(f'&{themeText}')
        self.darkModeAct.setStatusTip(f' Applying {themeText}')
        self._setTheme()

    def _setTheme(self):
        if self.settings['DARK_THEME']:
            qdarktheme.setup_theme('dark', additional_qss="QToolTip {color: black;}")
        else:
            qdarktheme.setup_theme('light')
        # UPDATING ICONS
        self._createIcons()
        self.newBiblioAct.setIcon(self.icons['NEW_WINDOW'])
        self.openBiblioAct.setIcon(self.icons['OPEN_IN_BROWSER'])
        self.saveBiblioAct.setIcon(self.icons['SAVE'])
        self.exitAct.setIcon(self.icons['CLOSE_WINDOW'])
        self.importBibtexAct.setIcon(self.icons['DOWNLOAD'])
        self.githubAct.setIcon(self.icons['GITHUB'])
        self.aboutAct.setIcon(self.icons['HELP'])

    @staticmethod
    def openGithub():
        import webbrowser
        webbrowser.open("https://github.com/EnguerranVidal/BibTrack")

    @staticmethod
    def openAbout():
        dialog = AboutDialog()
        dialog.exec_()

    def closeEvent(self, event):
        buttons = QMessageBox.Yes | QMessageBox.No
        reply = QMessageBox.question(self, 'Exit', "Are you sure to quit?", buttons, QMessageBox.No)
        if reply == QMessageBox.Yes:
            time.sleep(0.5)
            self.settings['MAXIMIZED'] = 1 if self.isMaximized() else 0
            saveSettings(self.settings, 'settings')
            for window in QApplication.topLevelWidgets():
                window.close()
            event.accept()
        else:
            event.ignore()
