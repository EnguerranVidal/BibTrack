######################## IMPORTS ########################
import json
import os
import re
import time

import numpy as np
from ecom.datatypes import TypeInfo

# ------------------- PyQt Modules -------------------- #
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *

# --------------------- Sources ----------------------- #
from src.common.utilities.fileSystem import loadSettings, saveSettings


######################## CLASSES ########################
class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About")
        # ABOUT TEXT EDIT
        aboutText = """
        <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>About BibTrack</title>
    </head>
    <body>
        <h1>About BibTrack</h1>
        <p>
            BibTrack is a powerful and intuitive bibliography management tool designed to streamline the organization of sources for your academic pursuits, whether it's a PhD thesis, research paper, or any documentation project. With its user-friendly interface and robust features, BibTrack simplifies the process of managing and tracking your sources, allowing you to focus more on your research and less on administrative tasks.
        </p>
        <h2>Key Features:</h2>
        <ul>
            <li><strong>Effortless Source Management:</strong> Easily add, edit, and categorize your sources, including texts, books, articles, websites, and more. BibTrack provides a centralized hub for all your references, ensuring easy access and retrieval whenever you need them.</li>
            <li><strong>Comprehensive Metadata:</strong> Capture essential metadata for each source, including title, author(s), publication year, keywords, description, and notes. This detailed information enables you to quickly locate and reference your sources with precision.</li>
            <li><strong>BibTeX Export Compatibility:</strong> Seamlessly export your bibliography in BibTeX format, ensuring compatibility with popular LaTeX editors and reference management software. BibTrack empowers you to integrate your sources seamlessly into your academic documents, enhancing the efficiency and accuracy of your writing process.</li>
            <li><strong>Progress Tracking:</strong> Stay organized and on track with BibTrack's progress tracking feature. Monitor your reading progress, set completion goals, and track your overall progress towards completing your sources. BibTrack helps you stay accountable and motivated throughout your research journey.</li>
        </ul>
        <p>
            BibTrack is proudly crafted by <a href='https://github.com/EnguerranVidal'>Enguerran Vidal</a>. Whether you're a seasoned academic or a budding researcher, BibTrack is your trusted companion for managing your bibliography with ease and efficiency. Experience the convenience and productivity of BibTrack today and elevate your research to new heights.
        </p>
    </body>
    </html>
        """
        testEdit = ExternalLinkTextEdit()
        testEdit.setReadOnly(True)
        testEdit.setTextInteractionFlags(Qt.TextBrowserInteraction)
        testEdit.setHtml(aboutText)
        testEdit.setFixedWidth(400)
        testEdit.setFixedHeight(500)
        doneButt = QPushButton("Done")
        doneButt.clicked.connect(self.accept)
        # MAIN LAYOUT
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(testEdit)
        self.layout.addWidget(doneButt)


class ExternalLinkTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super(QTextEdit, self).__init__(parent)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            anchor = self.anchorAt(event.pos())
            if anchor:
                QDesktopServices.openUrl(QUrl(anchor))
            else:
                super().mousePressEvent(event)
        else:
            super().mousePressEvent(event)