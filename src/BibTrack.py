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
from src.common.widgets.widgets import AboutDialog, NoBibTrackDisplay
from src.references.general import NewBibTrackWindow, BibEditor, NewSourceWindow, BibTexExportDialog


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
        self.noBibTrackDisplay = NoBibTrackDisplay()
        self.noBibTrackDisplay.createNew.connect(self.newBiblioTrack)
        self.noBibTrackDisplay.openExisting.connect(self.openBiblioTrack)
        self.mainDisplay = QStackedWidget()
        self.mainDisplay.addWidget(self.noBibTrackDisplay)
        self.setCentralWidget(self.mainDisplay)
        # OPENING BIB EDITOR
        if self.settings['CURRENT_BIB_TRACK'] and os.path.exists(self.settings['CURRENT_BIB_TRACK']):
            self.bibEditor = BibEditor(self.currentDir, self.settings['CURRENT_BIB_TRACK'])
            self.setWindowTitle(f"BibTrack ({os.path.basename(self.settings['CURRENT_BIB_TRACK'])})")
            # self.bibEditor.tracker.saveState()
            self.mainDisplay.addWidget(self.bibEditor)
            self.mainDisplay.setCurrentIndex(1)
        elif self.settings['CURRENT_BIB_TRACK']:
            if self.settings['CURRENT_BIB_TRACK'] in self.settings['OPENED_RECENTLY']:
                try:
                    self.settings['OPENED_RECENTLY'].remove(self.settings['CURRENT_BIB_TRACK'])
                except ValueError:
                    print(f"BibTrack {self.settings['CURRENT_BIB_TRACK']} not found in the opened recently.")
            self.settings['CURRENT_BIB_TRACK'] = ''
            self.mainDisplay.setCurrentIndex(0)
        saveSettings(self.settings, 'settings')
        # STATUS BAR CREATION & DATETIME LABEL
        self.datetime = QDateTime.currentDateTime()
        self.dateLabel = QLabel(self.datetime.toString('dd.MM.yyyy  hh:mm:ss'))
        self.dateLabel.setStyleSheet('border: 0;')
        self.statusBar().addPermanentWidget(self.dateLabel)
        self.statusBar().showMessage('Ready')
        self.statusDateTimer = QTimer()
        self.statusDateTimer.timeout.connect(self.updateStatus)
        self.statusDateTimer.start(1000)

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
        self.openBiblioAct.setShortcut('Ctrl+O')
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
        # Close Bibliography
        self.closeBiblioAct = QAction('&Close', self)
        self.closeBiblioAct.setStatusTip('Close Bibliography')
        self.closeBiblioAct.setIcon(self.icons['CLOSE_WINDOW'])
        self.closeBiblioAct.triggered.connect(self.closeBibTrack)
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
        self.exitAct.setStatusTip('Exit application')
        self.exitAct.triggered.connect(self.close)
        ########### HELP ###########
        # Add Article
        self.newArticleAct = QAction('&Article', self)
        self.newArticleAct.setStatusTip('Add New Article')
        self.newArticleAct.triggered.connect(self.addNewArticle)
        # Add Book
        self.newBookAct = QAction('&Book', self)
        self.newBookAct.setStatusTip('Add New Book')
        self.newBookAct.triggered.connect(self.addNewBook)
        # Add Booklet
        self.newBookletAct = QAction('&Booklet', self)
        self.newBookletAct.setStatusTip('Add New Booklet')
        self.newBookletAct.triggered.connect(self.addNewBooklet)
        # Add Conference
        self.newConferenceAct = QAction('&Conference', self)
        self.newConferenceAct.setStatusTip('Add New Conference')
        self.newConferenceAct.triggered.connect(self.addNewConference)
        # Add InBook
        self.newInBookAct = QAction('&InBook', self)
        self.newInBookAct.setStatusTip('Add New InBook')
        self.newInBookAct.triggered.connect(self.addNewInBook)
        # Add InCollection
        self.newInCollectionAct = QAction('&Collection', self)
        self.newInCollectionAct.setStatusTip('Add New InCollection')
        self.newInCollectionAct.triggered.connect(self.addNewInCollection)
        # Add InProceedings
        self.newInProceedingsAct = QAction('&InProceedings', self)
        self.newInProceedingsAct.setStatusTip('Add New InProceedings')
        self.newInProceedingsAct.triggered.connect(self.addNewInProceedings)
        # Add Manual
        self.newManualAct = QAction('&Manual', self)
        self.newManualAct.setStatusTip('Add New Manual')
        self.newManualAct.triggered.connect(self.addNewManual)
        # Add Book
        self.newMasterThesisAct = QAction('&Masters Thesis', self)
        self.newMasterThesisAct.setStatusTip('Add New Masters Thesis')
        self.newMasterThesisAct.triggered.connect(self.addNewMasterThesis)
        # Add Misc
        self.newMiscAct = QAction('&Misc', self)
        self.newMiscAct.setStatusTip('Add New Misc')
        self.newMiscAct.triggered.connect(self.addNewMisc)
        # Add Online
        self.newOnlineAct = QAction('&Online', self)
        self.newOnlineAct.setStatusTip('Add New Online')
        self.newOnlineAct.triggered.connect(self.addNewOnline)
        # Add PhD Thesis
        self.newPhdThesisAct = QAction('&PhD Thesis', self)
        self.newPhdThesisAct.setStatusTip('Add New PhD Thesis')
        self.newPhdThesisAct.triggered.connect(self.addNewPhdThesis)
        # Add Proceedings
        self.newProceedingsAct = QAction('&Proceedings', self)
        self.newProceedingsAct.setStatusTip('Add New Proceedings')
        self.newProceedingsAct.triggered.connect(self.addNewProceedings)
        # Add Standard
        self.newStandardAct = QAction('&Standard', self)
        self.newStandardAct.setStatusTip('Add New Standard')
        self.newStandardAct.triggered.connect(self.addNewStandard)
        # Add Tech Report
        self.newTechReportAct = QAction('&Tech Report', self)
        self.newTechReportAct.setStatusTip('Add New Tech Report')
        self.newTechReportAct.triggered.connect(self.addNewTechReport)
        # Add Unpublished
        self.newUnpublishedAct = QAction('&Unpublished', self)
        self.newUnpublishedAct.setStatusTip('Add New Unpublished')
        self.newUnpublishedAct.triggered.connect(self.addNewUnpublished)
        # Add Url
        self.newUrlAct = QAction('&URL', self)
        self.newUrlAct.setStatusTip('Add New URL')
        self.newUrlAct.triggered.connect(self.addNewUrl)
        # Remove Sources
        self.removeSourcesAct = QAction('&Delete Source', self)
        self.removeSourcesAct.setStatusTip('Delete Selected Source')
        self.removeSourcesAct.triggered.connect(self.deleteSelectedSource)

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
        self.fileMenu.addAction(self.closeBiblioAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.importBibtexAct)
        self.fileMenu.addAction(self.exportBibtexAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)
        self.fileMenu.aboutToShow.connect(self._populateFileMenu)

        ###  EDIT MENU  ###
        self.editMenu = self.menubar.addMenu('&Edit')

        ###  SOURCES MENU  ###
        self.sourcesMenu = self.menubar.addMenu('&Sources')
        self.addSourcesMenu = QMenu('&Add Source', self)
        self.addSourcesMenu.addAction(self.newArticleAct)
        self.addSourcesMenu.addAction(self.newBookAct)
        self.addSourcesMenu.addAction(self.newConferenceAct)
        self.addSourcesMenu.addAction(self.newOnlineAct)
        self.addSourcesMenu.addAction(self.newPhdThesisAct)
        self.otherSourcesMenu = QMenu('&Other', self)
        self.otherSourcesMenu.addAction(self.newBookletAct)
        self.otherSourcesMenu.addAction(self.newInBookAct)
        self.otherSourcesMenu.addAction(self.newInCollectionAct)
        self.otherSourcesMenu.addAction(self.newInProceedingsAct)
        self.otherSourcesMenu.addAction(self.newManualAct)
        self.otherSourcesMenu.addAction(self.newMasterThesisAct)
        self.otherSourcesMenu.addAction(self.newMiscAct)
        self.otherSourcesMenu.addAction(self.newProceedingsAct)
        self.otherSourcesMenu.addAction(self.newStandardAct)
        self.otherSourcesMenu.addAction(self.newTechReportAct)
        self.otherSourcesMenu.addAction(self.newUnpublishedAct)
        self.otherSourcesMenu.addAction(self.newUrlAct)
        self.addSourcesMenu.addSeparator()
        self.addSourcesMenu.addMenu(self.otherSourcesMenu)
        self.sourcesMenu.addMenu(self.addSourcesMenu)
        self.sourcesMenu.addAction(self.removeSourcesAct)
        self.sourcesMenu.aboutToShow.connect(self._populateSourcesMenu)

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
            self.closeBiblioAct.setDisabled(False)
            self.exportBibtexAct.setDisabled(False)
        elif self.bibEditor is not None:
            self.saveBiblioAct.setDisabled(True)
            self.saveAsBiblioAct.setDisabled(False)
            self.closeBiblioAct.setDisabled(False)
            self.exportBibtexAct.setDisabled(False)
        else:
            self.saveBiblioAct.setDisabled(True)
            self.saveAsBiblioAct.setDisabled(True)
            self.closeBiblioAct.setDisabled(True)
            self.exportBibtexAct.setDisabled(True)

    def _populateRecentMenu(self):
        self.recentMenu.clear()
        actions = []
        self.settings = loadSettings('settings')
        filenames = [os.path.basename(path) for path in self.settings['OPENED_RECENTLY']]
        for filename in filenames:
            action = QAction(filename, self)
            action.triggered.connect(partial(self.openRecentBibTrack, filename))
            actions.append(action)
        self.recentMenu.addActions(actions)

    def _populateSourcesMenu(self):
        if self.bibEditor is not None:
            selectedSources = self.bibEditor.sourcesTable.selectedItems()
            self.removeSourcesAct.setDisabled(not len(selectedSources) > 0)
            # ADDING SOURCES ACTIONS ENABLING
            self.newArticleAct.setDisabled(False)
            self.newBookAct.setDisabled(False)
            self.newBookletAct.setDisabled(False)
            self.newConferenceAct.setDisabled(False)
            self.newInBookAct.setDisabled(False)
            self.newInCollectionAct.setDisabled(False)
            self.newInProceedingsAct.setDisabled(False)
            self.newManualAct.setDisabled(False)
            self.newMasterThesisAct.setDisabled(False)
            self.newMiscAct.setDisabled(False)
            self.newOnlineAct.setDisabled(False)
            self.newPhdThesisAct.setDisabled(False)
            self.newProceedingsAct.setDisabled(False)
            self.newStandardAct.setDisabled(False)
            self.newTechReportAct.setDisabled(False)
            self.newUnpublishedAct.setDisabled(False)
            self.newUrlAct.setDisabled(False)
        else:
            self.removeSourcesAct.setDisabled(True)
            # ADDING SOURCES ACTIONS DISABLING
            self.newArticleAct.setDisabled(True)
            self.newBookAct.setDisabled(True)
            self.newBookletAct.setDisabled(True)
            self.newConferenceAct.setDisabled(True)
            self.newInBookAct.setDisabled(True)
            self.newInCollectionAct.setDisabled(True)
            self.newInProceedingsAct.setDisabled(True)
            self.newManualAct.setDisabled(True)
            self.newMasterThesisAct.setDisabled(True)
            self.newMiscAct.setDisabled(True)
            self.newOnlineAct.setDisabled(True)
            self.newPhdThesisAct.setDisabled(True)
            self.newProceedingsAct.setDisabled(True)
            self.newStandardAct.setDisabled(True)
            self.newTechReportAct.setDisabled(True)
            self.newUnpublishedAct.setDisabled(True)
            self.newUrlAct.setDisabled(True)

    def newBiblioTrack(self):
        self.settings = loadSettings('settings')
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
            self.bibEditor = BibEditor(self.currentDir, newBibTrackPath)
            self.mainDisplay.addWidget(self.bibEditor)
            self.mainDisplay.setCurrentIndex(1)
            self.bibEditor.tracker.saveState()
            self.addToRecent(newBibTrackPath)
            self.settings['CURRENT_BIB_TRACK'] = newBibTrackPath
            self.setWindowTitle(f"BibTrack ({os.path.basename(self.settings['CURRENT_BIB_TRACK'])})")
        saveSettings(self.settings, 'settings')
        self._populateFileMenu()

    def openBiblioTrack(self):
        self.settings = loadSettings('settings')
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
            self.bibEditor = BibEditor(self.currentDir, path)
            self.bibEditor.tracker.saveState()
            self.mainDisplay.addWidget(self.bibEditor)
            self.mainDisplay.setCurrentIndex(1)
            self.addToRecent(path)
            self.settings['CURRENT_BIB_TRACK'] = path
            self.setWindowTitle(f"BibTrack ({os.path.basename(self.settings['CURRENT_BIB_TRACK'])})")
        saveSettings(self.settings, 'settings')
        self._populateFileMenu()

    def openRecentBibTrack(self, folderName):
        self.settings = loadSettings('settings')
        filenames = [os.path.basename(path) for path in self.settings['OPENED_RECENTLY']]
        path = self.settings['OPENED_RECENTLY'][filenames.index(folderName)]
        if os.path.exists(path):
            if self.bibEditor is not None and self.bibEditor.tracker.unsavedChanges():
                reply = QMessageBox.question(self, 'Unsaved Changes',
                                             'There are unsaved changes. Do you want to save before opening?',
                                             QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
                if reply == QMessageBox.Save:
                    self.bibEditor.tracker.saveState()
                elif reply == QMessageBox.Cancel:
                    return
            self.bibEditor = BibEditor(self.currentDir, path)
            self.bibEditor.tracker.saveState()
            self.mainDisplay.addWidget(self.bibEditor)
            self.mainDisplay.setCurrentIndex(1)
            self.addToRecent(path)
            self.settings['CURRENT_BIB_TRACK'] = path
            self.setWindowTitle(f"BibTrack ({os.path.basename(self.settings['CURRENT_BIB_TRACK'])})")
        saveSettings(self.settings, 'settings')
        self._populateFileMenu()

    def addToRecent(self, path):
        self.settings = loadSettings('settings')
        if path in self.settings['OPENED_RECENTLY']:
            self.settings['OPENED_RECENTLY'].pop(self.settings['OPENED_RECENTLY'].index(path))
        self.settings['OPENED_RECENTLY'].insert(0, path)
        if len(self.settings['OPENED_RECENTLY']) == 5:
            self.settings['OPENED_RECENTLY'] = self.settings['OPENED_RECENTLY'][:4]
        saveSettings(self.settings, 'settings')

    def saveBibTrack(self):
        self.bibEditor.tracker.saveState()
        self._populateFileMenu()

    def saveAsBibTrack(self):
        self.settings = loadSettings('settings')
        if os.path.exists(self.bibTracksPath):
            path = QFileDialog.getExistingDirectory(self, "Select Directory", self.bibTracksPath)
        else:
            path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if os.path.abspath(path) not in [os.path.abspath(self.bibTracksPath), os.path.abspath(self.currentDir)]:
            self.bibEditor.tracker.saveState(path)
            self.addToRecent(path)
            self.settings['CURRENT_BIB_TRACK'] = path
            self.setWindowTitle(f"BibTrack ({os.path.basename(self.settings['CURRENT_BIB_TRACK'])})")
        saveSettings(self.settings, 'settings')
        self._populateFileMenu()

    def closeBibTrack(self):
        self.settings = loadSettings('settings')
        self.mainDisplay.removeWidget(self.bibEditor)
        self.bibEditor = None
        self.settings['CURRENT_BIB_TRACK'] = ''
        saveSettings(self.settings, 'settings')

    def importBibtex(self):
        pass

    def exportToBibtex(self):
        exportDialog = BibTexExportDialog()
        result = exportDialog.exec_()
        if result == QDialog.Accepted:
            self.bibEditor.tracker.generateBibTexFile(exportDialog.refPath)

    def addNewArticle(self):
        sourceTagList = list(self.bibEditor.tracker.sources.keys())
        dialog = NewSourceWindow(sourceType='Article', sourceTags=sourceTagList)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            tag = dialog.nameLineEdit.text()
            fields = {'author': '', 'title': '', 'journal': '', 'year': '', 'volume': '', 'number': '', 'pages': '',
                      'month': '', 'crossref': '', 'note': ''}
            source = {'SELECTED': False, 'TYPE': 'ARTICLE', 'FIELDS': fields, 'DESCRIPTION': '',
                      'PDF': '', 'URL': '', 'ACCESS': 'NONE', 'KEYWORDS': []}
            self.bibEditor.tracker.addSource(tag, source)
            self.bibEditor.addRow(tag, source)

    def addNewBook(self):
        sourceTagList = list(self.bibEditor.tracker.sources.keys())
        dialog = NewSourceWindow(sourceType='Book', sourceTags=sourceTagList)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            tag = dialog.nameLineEdit.text()
            fields = {'author': '', 'title': '', 'publisher': '', 'year': '', 'volume': '', 'series': '', 'address': '',
                      'edition': '', 'month': '', 'crossref': '', 'note': ''}
            source = {'SELECTED': False, 'TYPE': 'BOOK', 'FIELDS': fields, 'DESCRIPTION': '',
                      'PDF': '', 'URL': '', 'ACCESS': 'NONE', 'KEYWORDS': []}
            self.bibEditor.tracker.addSource(tag, source)
            self.bibEditor.addRow(tag, source)

    def addNewBooklet(self):
        sourceTagList = list(self.bibEditor.tracker.sources.keys())
        dialog = NewSourceWindow(sourceType='Booklet', sourceTags=sourceTagList)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            tag = dialog.nameLineEdit.text()
            fields = {'author': '', 'title': '', 'howpublished': '', 'address': '', 'month': '', 'year': '',
                      'crossref': '', 'note': ''}
            source = {'SELECTED': False, 'TYPE': 'BOOKLET', 'FIELDS': fields, 'DESCRIPTION': '',
                      'PDF': '', 'URL': '', 'ACCESS': 'NONE', 'KEYWORDS': []}
            self.bibEditor.tracker.addSource(tag, source)
            self.bibEditor.addRow(tag, source)

    def addNewConference(self):
        sourceTagList = list(self.bibEditor.tracker.sources.keys())
        dialog = NewSourceWindow(sourceType='Conference', sourceTags=sourceTagList)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            tag = dialog.nameLineEdit.text()
            fields = {'author': '', 'title': '', 'booktitle': '', 'year': '', 'editor': '', 'volume': '', 'series': '',
                      'pages': '', 'address': '', 'month': '', 'organization': '', 'publisher': '',
                      'crossref': '', 'note': ''}
            source = {'SELECTED': False, 'TYPE': 'CONFERENCE', 'FIELDS': fields, 'DESCRIPTION': '',
                      'PDF': '', 'URL': '', 'ACCESS': 'NONE', 'KEYWORDS': []}
            self.bibEditor.tracker.addSource(tag, source)
            self.bibEditor.addRow(tag, source)

    def addNewInBook(self):
        sourceTagList = list(self.bibEditor.tracker.sources.keys())
        dialog = NewSourceWindow(sourceType='In Book', sourceTags=sourceTagList)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            tag = dialog.nameLineEdit.text()
            fields = {'author': '', 'title': '', 'chapter': '', 'publisher': '', 'year': '', 'volume': '', 'series': '',
                      'type': '', 'address': '', 'edition': '', 'month': '', 'crossref': '', 'note': ''}
            source = {'SELECTED': False, 'TYPE': 'INBOOK', 'FIELDS': fields, 'DESCRIPTION': '',
                      'PDF': '', 'URL': '', 'ACCESS': 'NONE', 'KEYWORDS': []}
            self.bibEditor.tracker.addSource(tag, source)
            self.bibEditor.addRow(tag, source)

    def addNewInCollection(self):
        sourceTagList = list(self.bibEditor.tracker.sources.keys())
        dialog = NewSourceWindow(sourceType='In Collection', sourceTags=sourceTagList)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            tag = dialog.nameLineEdit.text()
            fields = {'author': '', 'title': '', 'booktitle': '', 'publisher': '', 'year': '', 'editor': '',
                      'volume': '', 'series': '', 'type': '', 'chapter': '', 'pages': '', 'address': '', 'edition': '',
                      'organization': '', 'month': '', 'crossref': '', 'note': ''}
            source = {'SELECTED': False, 'TYPE': 'INCOLLECTION', 'FIELDS': fields, 'DESCRIPTION': '',
                      'PDF': '', 'URL': '', 'ACCESS': 'NONE', 'KEYWORDS': []}
            self.bibEditor.tracker.addSource(tag, source)
            self.bibEditor.addRow(tag, source)

    def addNewInProceedings(self):
        sourceTagList = list(self.bibEditor.tracker.sources.keys())
        dialog = NewSourceWindow(sourceType='In Proceedings', sourceTags=sourceTagList)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            tag = dialog.nameLineEdit.text()
            fields = {'author': '', 'title': '', 'booktitle': '', 'year': '', 'editor': '', 'volume': '', 'series': '',
                      'pages': '', 'address': '', 'month': '', 'organization': '', 'publisher': '',
                      'crossref': '', 'note': ''}
            source = {'SELECTED': False, 'TYPE': 'INPROCEEDINGS', 'FIELDS': fields, 'DESCRIPTION': '',
                      'PDF': '', 'URL': '', 'ACCESS': 'NONE', 'KEYWORDS': []}
            self.bibEditor.tracker.addSource(tag, source)
            self.bibEditor.addRow(tag, source)

    def addNewManual(self):
        sourceTagList = list(self.bibEditor.tracker.sources.keys())
        dialog = NewSourceWindow(sourceType='Manual', sourceTags=sourceTagList)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            tag = dialog.nameLineEdit.text()
            fields = {'title': '', 'author': '', 'organization': '', 'address': '', 'edition': '', 'month': '',
                      'year': '', 'crossref': '', 'note': ''}
            source = {'SELECTED': False, 'TYPE': 'MANUAL', 'FIELDS': fields, 'DESCRIPTION': '',
                      'PDF': '', 'URL': '', 'ACCESS': 'NONE', 'KEYWORDS': []}
            self.bibEditor.tracker.addSource(tag, source)
            self.bibEditor.addRow(tag, source)

    def addNewMasterThesis(self):
        sourceTagList = list(self.bibEditor.tracker.sources.keys())
        dialog = NewSourceWindow(sourceType='Masters Thesis', sourceTags=sourceTagList)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            tag = dialog.nameLineEdit.text()
            fields = {'title': '', 'author': '', 'school': '', 'year': '', 'type': '', 'address': '',
                      'month': '', 'crossref': '', 'note': ''}
            source = {'SELECTED': False, 'TYPE': 'MASTERSTHESIS', 'FIELDS': fields, 'DESCRIPTION': '',
                      'PDF': '', 'URL': '', 'ACCESS': 'NONE', 'KEYWORDS': []}
            self.bibEditor.tracker.addSource(tag, source)
            self.bibEditor.addRow(tag, source)

    def addNewMisc(self):
        sourceTagList = list(self.bibEditor.tracker.sources.keys())
        dialog = NewSourceWindow(sourceType='Misc Source', sourceTags=sourceTagList)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            tag = dialog.nameLineEdit.text()
            fields = {'title': '', 'author': '', 'howpublished': '', 'month': '', 'year': '',
                      'crossref': '', 'note': ''}
            source = {'SELECTED': False, 'TYPE': 'MISC', 'FIELDS': fields, 'DESCRIPTION': '',
                      'PDF': '', 'URL': '', 'ACCESS': 'NONE', 'KEYWORDS': []}
            self.bibEditor.tracker.addSource(tag, source)
            self.bibEditor.addRow(tag, source)

    def addNewOnline(self):
        sourceTagList = list(self.bibEditor.tracker.sources.keys())
        dialog = NewSourceWindow(sourceType='Online Source', sourceTags=sourceTagList)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            tag = dialog.nameLineEdit.text()
            fields = {'title': '', 'author': '', 'month': '', 'year': '', 'url': '', 'note': ''}
            source = {'SELECTED': False, 'TYPE': 'ONLINE', 'FIELDS': fields, 'DESCRIPTION': '',
                      'PDF': '', 'URL': '', 'ACCESS': 'NONE', 'KEYWORDS': []}
            self.bibEditor.tracker.addSource(tag, source)
            self.bibEditor.addRow(tag, source)

    def addNewPhdThesis(self):
        sourceTagList = list(self.bibEditor.tracker.sources.keys())
        dialog = NewSourceWindow(sourceType='PhD Thesis', sourceTags=sourceTagList)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            tag = dialog.nameLineEdit.text()
            fields = {'title': '', 'author': '', 'school': '', 'year': '', 'type': '', 'month': '', 'address': '',
                      'crossref': '', 'note': ''}
            source = {'SELECTED': False, 'TYPE': 'PHDTHESIS', 'FIELDS': fields, 'DESCRIPTION': '',
                      'PDF': '', 'URL': '', 'ACCESS': 'NONE', 'KEYWORDS': []}
            self.bibEditor.tracker.addSource(tag, source)
            self.bibEditor.addRow(tag, source)

    def addNewProceedings(self):
        sourceTagList = list(self.bibEditor.tracker.sources.keys())
        dialog = NewSourceWindow(sourceType='Proceeding', sourceTags=sourceTagList)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            tag = dialog.nameLineEdit.text()
            fields = {'title': '', 'year': '', 'editor': '', 'volume': '', 'series': '', 'address': '', 'month': '',
                      'publisher': '', 'organization': '', 'crossref': '', 'note': ''}
            source = {'SELECTED': False, 'TYPE': 'PROCEEDINGS', 'FIELDS': fields, 'DESCRIPTION': '',
                      'PDF': '', 'URL': '', 'ACCESS': 'NONE', 'KEYWORDS': []}
            self.bibEditor.tracker.addSource(tag, source)
            self.bibEditor.addRow(tag, source)

    def addNewStandard(self):
        sourceTagList = list(self.bibEditor.tracker.sources.keys())
        dialog = NewSourceWindow(sourceType='Standard', sourceTags=sourceTagList)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            tag = dialog.nameLineEdit.text()
            fields = {'title': '', 'organization': '', 'institution': '', 'author': '', 'language': '',
                      'howpublished': '', 'type': '', 'number': '', 'revision': '', 'address': '', 'year': '',
                      'month': '', 'url': '', 'crossref': '', 'note': ''}
            source = {'SELECTED': False, 'TYPE': 'STANDARD', 'FIELDS': fields, 'DESCRIPTION': '',
                      'PDF': '', 'URL': '', 'ACCESS': 'NONE', 'KEYWORDS': []}
            self.bibEditor.tracker.addSource(tag, source)
            self.bibEditor.addRow(tag, source)

    def addNewTechReport(self):
        sourceTagList = list(self.bibEditor.tracker.sources.keys())
        dialog = NewSourceWindow(sourceType='Tech Report', sourceTags=sourceTagList)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            tag = dialog.nameLineEdit.text()
            fields = {'author': '', 'title': '', 'institution': '', 'year': '', 'type': '', 'number': '',
                      'address': '', 'month': '', 'crossref': '', 'note': ''}
            source = {'SELECTED': False, 'TYPE': 'TECHREPORT', 'FIELDS': fields, 'DESCRIPTION': '',
                      'PDF': '', 'URL': '', 'ACCESS': 'NONE', 'KEYWORDS': []}
            self.bibEditor.tracker.addSource(tag, source)
            self.bibEditor.addRow(tag, source)

    def addNewUnpublished(self):
        sourceTagList = list(self.bibEditor.tracker.sources.keys())
        dialog = NewSourceWindow(sourceType='Unpublished Source', sourceTags=sourceTagList)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            tag = dialog.nameLineEdit.text()
            fields = {'author': '', 'title': '', 'month': '', 'year': '', 'crossref': '', 'note': ''}
            source = {'SELECTED': False, 'TYPE': 'UNPUBLISHED', 'FIELDS': fields, 'DESCRIPTION': '',
                      'PDF': '', 'URL': '', 'ACCESS': 'NONE', 'KEYWORDS': []}
            self.bibEditor.tracker.addSource(tag, source)
            self.bibEditor.addRow(tag, source)

    def addNewUrl(self):
        sourceTagList = list(self.bibEditor.tracker.sources.keys())
        dialog = NewSourceWindow(sourceType='URL', sourceTags=sourceTagList)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            tag = dialog.nameLineEdit.text()
            fields = {'author': '', 'year': '', 'series': '', 'edition': '', 'month': '', 'crossref': ''}
            source = {'SELECTED': False, 'TYPE': 'UNPUBLISHED', 'FIELDS': fields, 'DESCRIPTION': '',
                      'PDF': '', 'URL': '', 'ACCESS': 'NONE', 'KEYWORDS': []}
            self.bibEditor.tracker.addSource(tag, source)
            self.bibEditor.addRow(tag, source)

    def deleteSelectedSource(self):
        self.bibEditor.deleteSelectedRows()

    def toggleDarkMode(self):
        self.settings = loadSettings('settings')
        self.settings['DARK_THEME'] = not self.settings['DARK_THEME']
        themeText = 'Light Theme' if self.settings['DARK_THEME'] else 'Dark Theme'
        self.darkModeAct.setText(f'&{themeText}')
        self.darkModeAct.setStatusTip(f' Applying {themeText}')
        saveSettings(self.settings, 'settings')
        self._setTheme()

    def _setTheme(self):
        self.settings = loadSettings('settings')
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

    def updateStatus(self):
        self.datetime = QDateTime.currentDateTime()
        formattedDate = self.datetime.toString('dd.MM.yyyy  hh:mm:ss')
        self.dateLabel.setText(formattedDate)

    def closeEvent(self, event):
        if self.bibEditor is not None and self.bibEditor.tracker.unsavedChanges():
            reply = QMessageBox.question(self, 'Unsaved Changes',
                                         'There are unsaved changes. Do you want to save ?',
                                         QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            if reply == QMessageBox.Save:
                self.bibEditor.tracker.saveState()
                time.sleep(0.5)
                self.settings = loadSettings('settings')
                self.settings['MAXIMIZED'] = 1 if self.isMaximized() else 0
                saveSettings(self.settings, 'settings')
                for window in QApplication.topLevelWidgets():
                    window.close()
                event.accept()
            elif reply == QMessageBox.Cancel:
                event.ignore()
            else:
                time.sleep(0.5)
                self.settings = loadSettings('settings')
                self.settings['MAXIMIZED'] = 1 if self.isMaximized() else 0
                saveSettings(self.settings, 'settings')
                for window in QApplication.topLevelWidgets():
                    window.close()
                event.accept()
        else:
            buttons = QMessageBox.Yes | QMessageBox.No
            reply = QMessageBox.question(self, 'Exit', "Are you sure to quit?", buttons, QMessageBox.No)
            if reply == QMessageBox.Yes:
                time.sleep(0.5)
                self.settings = loadSettings('settings')
                self.settings['MAXIMIZED'] = 1 if self.isMaximized() else 0
                saveSettings(self.settings, 'settings')
                for window in QApplication.topLevelWidgets():
                    window.close()
                event.accept()
            else:
                event.ignore()
