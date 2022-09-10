import sys
from PySide6.QtWidgets import QApplication, QLabel, QMessageBox, QGridLayout
from PySide6.QtCore import QFile
from PySide6.QtGui import QIcon
from PySide6.QtUiTools import QUiLoader
from QTextWithLineNum import QTextEditWithLineNum

class Window:

    def __init__(self):

        UiFile = QFile("UI.ui")
        UiFile.open(QFile.ReadOnly)
        UiFile.close()

        self.ui = QUiLoader().load(UiFile)

        self.ui.qtCodeArea = QTextEditWithLineNum(self.ui.qtCodeArea)
        self.ui.qtElementArea = QTextEditWithLineNum(self.ui.qtElementArea)
        # self.ui.qtMatrixArea = QTextEditWithLineNum(self.ui.qtElementArea)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.ui.show()
    app.exec()
