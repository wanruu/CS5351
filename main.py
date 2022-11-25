import sys
from PySide6.QtWidgets import QApplication, QLabel, QMessageBox, QGridLayout, QFileDialog, QTableWidgetItem, QTextEdit, \
    QHeaderView
from PySide6.QtCore import QFile
from PySide6.QtGui import QIcon
from PySide6.QtUiTools import QUiLoader
from QTextWithLineNum import QTextEditWithLineNum
import pandas as pd
import numpy as np
import os
from getnum import getLine
from ft_based import cal_sus
from get_result import get_result, get_errorLine, generateExcel
from qt_material import apply_stylesheet

from qt_material import apply_stylesheet
from utils import *


class Window:

    def __init__(self):

        UiFile = QFile("UI.ui")
        # UiFile =
        UiFile.open(QFile.ReadOnly)
        UiFile.close()

        loader = QUiLoader()
        loader.registerCustomWidget(QTextEditWithLineNum)

        self.choosen = []
        self.fileName = None
        self.name = None
        self.testCase = []
        self.testCasesInput = []
        self.testCasesOutput = []
        self.line = 0
        self.algorithm = 'default'

        self.colorbar = ['ff0000', 'c43242', 'dc3a38', 'e4734e', 'eda15d']

        self.ui = loader.load(UiFile)
        self.ui.actiondefault.triggered.connect(self.chooseDefault)
        self.ui.actiondstar.triggered.connect(self.chooseDstar)
        self.ui.actionbarinel.triggered.connect(self.chooseBarinel)
        self.ui.actionochiai.triggered.connect(self.chooseOchiai)
        self.ui.actionTarantula.triggered.connect(self.chooseTarantula)
        self.ui.actionopen.triggered.connect(self.openExcelFile)
        self.ui.actionopen_code.triggered.connect(self.openCodeFile)
        self.ui.qtMatrixArea.doubleClicked.connect(self.matrixAreaDoubleClicked)
        self.ui.pushButton.clicked.connect(self.clickButton)
        self.ui.pushButton_2.clicked.connect(self.getText)
        self.ui.run.clicked.connect(self.getAnswer)
        self.ui.analyse.clicked.connect(self.analyse)

        self.openCodeFile('./demo/ps.py')

    def chooseDefault(self):
        self.algorithm = 'default'

    def chooseDstar(self):
        self.algorithm = 'dstar'

    def chooseBarinel(self):
        self.algorithm = 'barinel'

    def chooseOchiai(self):
        self.algorithm = 'ochiai'

    def chooseTarantula(self):
        self.algorithm = 'Tarantula'

    def analyse(self):
        print("ok")

        text = self.ui.qtElementArea.document().toPlainText()

        self.testCasesInput, self.testCasesOutput = getTestCases(text)

        print(self.testCasesInput, self.testCasesOutput)

        if self.algorithm == 'default':
            print("ok!")
            pass
        elif self.algorithm == 'dstar':
            print("ok!!")
            pass
        elif self.algorithm == 'barinel':
            print("ok!!!")
            pass
        elif self.algorithm == 'ochiai':
            print("ok!!!!")
            pass
        elif self.algorithm == 'Tarantula':
            print("ok!!!!!")
            pass

    def getText(self):

        text = self.ui.qtCodeArea.document().toPlainText().split('\n')

        filename = self.getFileName()

        with open(filename, 'w') as f:
            for line in text:
                f.writelines(line)
                f.writelines('\n')
        f.close()

    def getFileName(self):

        return self.fileName

    def clickButton(self):

        curPath = os.path.abspath(os.path.dirname(__file__))
        rootPath = os.path.split(curPath)[0]
        sys.path.append(rootPath)
        filename = self.getFileName()
        result = os.popen("Python3 -m trace --count -C . " + filename).read()
        answer = self.ui.qtElementArea.document().toPlainText()
        # print(result)
        # print(type(result))
        # print(answer)
        # print(type(answer))
        testLine = getLine(self.name)
        test_ = get_result(testLine, filename)

        for i in test_:
            if self.line < i:
                self.line = i

        label = 1
        if result != answer:
            label = 0

        test_case = (test_, label)
        self.testCase.append(test_case)

    def getAnswer(self):

        result = cal_sus(self.testCase, self.line)

        errorLines = get_errorLine(result, self.fileName)

        generateExcel(errorLines)

        self.openExcelFile('text.xls')

    def changeBackgroundColorToRed(self):
        label = self.choosen[0]

        text = self.ui.qtCodeArea.document().toHtml().split('\n')

        # color =  #
        for _ in range(1, len(self.choosen)):
            text[self.choosen[_] + 4] = text[self.choosen[_] + 4].replace("margin-top:0px;",
                                                                          "margin-top:0px; background-color:#" +
                                                                          self.colorbar[
                                                                              min(len(self.colorbar) - 1, _ - 1)] + ";",
                                                                          1)

        html = ""
        for line in text:
            html += line + '\n'

        self.ui.qtCodeArea.setText(html)

    def changeBackgroundColorToWhite(self):

        text = self.ui.qtCodeArea.document().toHtml().split('\n')

        for _ in range(1, len(self.choosen)):
            # color = #ff0000
            for i in range(len(self.colorbar)):
                text[self.choosen[_] + 4] = text[self.choosen[_] + 4].replace(" background-color:#"+self.colorbar[i]+";",
                                                                              ""
                                                                              , 2)

        html = ""
        for line in text:
            html += line + '\n'

        self.ui.qtCodeArea.setText(html)
        self.choosen = []

    def matrixAreaDoubleClicked(self):

        self.changeBackgroundColorToWhite()

        row = self.ui.qtMatrixArea.currentIndex().row()
        for i in range(self.ui.qtMatrixArea.columnCount()):
            if self.ui.qtMatrixArea.item(row, i).text() == 'nan':
                break
            self.choosen.append(int(self.ui.qtMatrixArea.item(row, i).text()))

        self.changeBackgroundColorToRed()

    def openCodeFile(self, codeFileName=None):

        self.testCase = []
        self.line = 0

        if not codeFileName:
            codeFileName, _ = QFileDialog.getOpenFileName(self.ui, 'open file',
                                                          './demo',
                                                          'Excel files(*.c , *.cpp , *.py)')

        self.fileName = codeFileName

        index = -1
        while (codeFileName[index] != '/'):
            index -= 1
        self.name = codeFileName[index:-3]

        if len(codeFileName) > 0:
            with open(codeFileName, 'r') as F:
                codeLine = F.read()
                self.ui.qtCodeArea.setText(codeLine)

    def openExcelFile(self, ExcelFileName=None):

        if not ExcelFileName:
            ExcelFileName, _ = QFileDialog.getOpenFileName(self.ui, 'open file',
                                                           './demo', 'Excel files(*.xlsx , *.xls)')

        if len(ExcelFileName) > 0:
            input_table = pd.read_excel(ExcelFileName, header=None)
            input_table = input_table.astype("int")
            # print(input_table)
            input_table_rows = input_table.shape[0]
            Line = ['test ' + str(i + 1) for i in range(input_table_rows)]
            input_table_colunms = input_table.shape[1]

            sloc = ['state']

            for i in range(input_table_colunms - 1):
                sloc.append('code line ' + str(i + 1))

            # input_table = pd.DataFrame(input_table, columns=sloc, index=Line)
            # print(input_table)
            # input_table_header = input_table.columns.values.tolist()

            self.ui.qtMatrixArea.setColumnCount(input_table_colunms)
            self.ui.qtMatrixArea.setRowCount(input_table_rows)

            self.ui.qtMatrixArea.setHorizontalHeaderLabels(sloc)
            self.ui.qtMatrixArea.setVerticalHeaderLabels(Line)
            self.ui.qtMatrixArea.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
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
    apply_stylesheet(app, theme='dark_lightgreen.xml')
    window.ui.show()
    app.exec()
