import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from gui import MainWindow
from mne_pipeline_hd.gui.gui_utils import StderrStream, StdoutStream

ismac = sys.platform.startswith("darwin")
iswin = sys.platform.startswith("win32")
islin = not ismac and not iswin


def main():
    app_name = 'Neurophysiologie-Praktikum'

    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    app.setApplicationName(app_name)

    try:
        app.setAttribute(Qt.AA_DisableWindowContextHelpButton, True)
    except AttributeError:
        print('pyqt-Version is < 5.12')

    if ismac:
        app.setAttribute(Qt.AA_DontShowIconsInMenus, True)
        # Workaround for MAC menu-bar-focusing issue
        app.setAttribute(Qt.AA_DontUseNativeMenuBar, True)

    # Open Main-Window
    mw = MainWindow()

    # Redirect stdout to capture it later in GUI
    sys.stdout = StdoutStream()
    # Redirect stderr to capture the output by tdqm
    sys.stderr = StderrStream()

    # For Spyder to make console accessible again
    app.lastWindowClosed.connect(app.quit)

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
