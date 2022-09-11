import sys
from PySide6.QtWidgets import QApplication, QLabel, QMessageBox, QGridLayout, QFileDialog, QTableWidgetItem
from PySide6.QtCore import QFile
from PySide6.QtGui import QIcon
from PySide6.QtUiTools import QUiLoader
from QTextWithLineNum import QTextEditWithLineNum
import pandas as pd
import numpy as np


class Window:

    def __init__(self):

        UiFile = QFile("UI.ui")
        UiFile.open(QFile.ReadOnly)
        UiFile.close()

        loader = QUiLoader()
        loader.registerCustomWidget(QTextEditWithLineNum)

        self.ui = loader.load(UiFile)
        self.ui.actionopen.triggered.connect(self.openExcelFile)
        self.ui.actionopen_code.triggered.connect(self.openCodeFile)


    def openCodeFile(self):
        codeFileName, _ = QFileDialog.getOpenFileName(self.ui, 'open file',
                                                       '/Users/yunqizhao/PycharmProjects/CityU/demo',
                                                       'Excel files(*.c, *.cpp, *.py)')

        if len(codeFileName) > 0:
            with open(codeFileName, 'r') as F:
                codeLine = F.read()
                self.ui.qtCodeArea.setText(codeLine)


    def openExcelFile(self):
        ExcelFileName, _ = QFileDialog.getOpenFileName(self.ui, 'open file',
                                                    '/Users/yunqizhao/PycharmProjects/CityU/demo', 'Excel files(*.xlsx, *.xls)')

        if len(ExcelFileName) > 0:
            input_table = pd.read_excel(ExcelFileName)
            print(input_table)
            input_table_rows = input_table.shape[0]
            input_table_colunms = input_table.shape[1]
            # input_table_header = input_table.columns.values.tolist()
            self.ui.qtMatrixArea.setColumnCount(input_table_colunms)
            self.ui.qtMatrixArea.setRowCount(input_table_rows)
            # self.ui.qtMatrixArea.setHorizontalHeaderLabels(input_table_header)

            for i in range(input_table_rows):
                input_table_rows_values = input_table.iloc[[i]]
                input_table_rows_values_array = np.array(input_table_rows_values)
                input_table_rows_values_list = input_table_rows_values_array.tolist()[0]
                for j in range(input_table_colunms):
                    input_table_items_list = input_table_rows_values_list[j]
                    input_table_items = str(input_table_items_list)
                    newItem = QTableWidgetItem(input_table_items)
                    # newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.ui.qtMatrixArea.setItem(i, j, newItem)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.ui.show()
    app.exec()
