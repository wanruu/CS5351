import sys
from PySide6.QtWidgets import QApplication, QLabel, QMessageBox
from PySide6.QtCore import QFile
from PySide6.QtGui import QIcon
from PySide6.QtUiTools import QUiLoader

class Window:

    def __init__(self):

        UiFile = QFile("UI.ui")
        UiFile.open(QFile.ReadOnly)
        UiFile.close()

        self.ui = QUiLoader().load(UiFile)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.ui.show()
    app.exec()
