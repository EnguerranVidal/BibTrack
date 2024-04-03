from src.BibTrack import *
import sys


def main(*args):
    qdarktheme.enable_hi_dpi()
    app = QApplication(sys.argv)
    currentDirectory = os.path.dirname(os.path.realpath(__file__))

    pyStratoGui = BibTrackGui(currentDirectory)
    pyStratoGui.initializeUI()
    pyStratoGui.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
