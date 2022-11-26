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
from ft_based import cal_sus, split_code_from_file
from line_based import dstar, ochiai, barinel, Tarantula
from get_result import get_result, get_errorLine, generateExcel
from qt_material import apply_stylesheet

from qt_material import apply_stylesheet
from utils import *


# [1,2,3,4] {5}
# [1] {0}
# [] {}
# [1] {1,2,3,4}
# [199999 200] {201, 200000}

class Window:

    def __init__(self):

        UiFile = QFile("UI.ui")
        # UiFile =
        UiFile.open(QFile.ReadOnly)
        UiFile.close()

        loader = QUiLoader()
        loader.registerCustomWidget(QTextEditWithLineNum)

        self.INPUTFILEPATH = './demo/input.txt'
        self.OUTPUTFILEPATH = './demo/output.txt'
        self.COPYCODEPATH = ''
        self.PYTHONCODEFILENAME = 'sequence'

        self.choosen = []
        self.fileName = None
        self.testCaseFileName = './demo/sequence.txt'
        self.name = None
        self.testCase = []
        self.testCasesInput = []
        self.testCasesOutput = []
        self.testCaseLabel = []
        self.testMatrix = []
        self.line = 0
        self.algorithm = 'default'

        self.colorbar = ['ff0000', 'c43242', 'dc3a38', 'e4734e', 'e58db4']

        self.ui = loader.load(UiFile)
        self.ui.actiondefault.triggered.connect(self.chooseDefault)
        self.ui.actiondstar.triggered.connect(self.chooseDstar)
        self.ui.actionbarinel.triggered.connect(self.chooseBarinel)
        self.ui.actionochiai.triggered.connect(self.chooseOchiai)
        self.ui.actionTarantula.triggered.connect(self.chooseTarantula)
        self.ui.actionopen.triggered.connect(self.openExcelFile)
        self.ui.actionopen_code.triggered.connect(self.openCodeFile)
        self.ui.actionload_test_case.triggered.connect(self.openTestCaseFile)

        self.ui.qtMatrixArea.doubleClicked.connect(self.matrixAreaDoubleClicked)
        # self.ui.pushButton.clicked.connect(self.clickButton)
        self.ui.save.clicked.connect(self.saveTestCaseFile)
        # self.ui.run.clicked.connect(self.getAnswer)
        self.ui.analyse.clicked.connect(self.analyse)

        self.openCodeFile('./demo/sequence.py')
        self.openTestCaseFile('./demo/sequence.txt')

    def saveTestCaseFile(self):
        txt = self.ui.qtElementArea.document().toPlainText()
        with open(self.testCaseFileName, 'w') as F:
            F.write(txt)

    def openTestCaseFile(self, testCaseFileName=None):
        # self.testCase = []
        # self.line = 0

        if not testCaseFileName:
            testCaseFileName, _ = QFileDialog.getOpenFileName(self.ui, 'open test case file',
                                                              './demo',
                                                              'Excel files(*.txt)')

        self.testCaseFileName = testCaseFileName
        print(testCaseFileName)

        # index = -1
        # while (testCaseFileName[index] != '/'):
        #     index -= 1
        # self.name = codeFileName[index:-3]

        if len(testCaseFileName) > 0:
            with open(testCaseFileName, 'r') as F:
                # print("ok")
                testCaseLine = F.read()
                # print(testCaseLine)
                self.ui.qtElementArea.setText(testCaseLine)

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

    def more(self, input_, output_):
        for i in range(len(input_)):
            with open(self.INPUTFILEPATH[:-4] + str(i) + self.INPUTFILEPATH[-4:], 'w') as F:
                # print(input_[i])
                for j in range(len(input_[i])):
                    # print()
                    F.write(str(input_[i][j]) + '\n')

        for i in range(len(output_)):
            # print(self.OUTPUTFILEPATH[:-4] + str(i) + self.OUTPUTFILEPATH[-4:])
            with open(self.OUTPUTFILEPATH[:-4] + str(i) + self.OUTPUTFILEPATH[-4:], 'w') as F:
                for j in range(len(output_[i])):
                    # print(str(output_[i][j]) + '\n')
                    F.write(str(output_[i][j]) + '\n')

    def getlm(self):
        retLabel, matrix = [], []

        # print(len(self.testCasesOutput))
        ayayyayyayay = self.ui.qtCodeArea.document().toPlainText()
        totol_line = gettotallinesnum(ayayyayyayay)
        for i in range(len(self.testCasesOutput)):

            # print(i)
            # print("ok")
            ipath = self.INPUTFILEPATH[:-4] + str(i) + self.INPUTFILEPATH[-4:]
            opath = self.OUTPUTFILEPATH[:-4] + str(i) + self.OUTPUTFILEPATH[-4:]

            code_copy = self.ui.qtCodeArea.document().toPlainText()

            # print(code_copy)
            # print("if __name__ == \'__main__\':\n    sys.stdin = open(\"" + ipath + "\", \"r\")\n",
            #       "   sys.stdout = open(\"" + opath + "\", \"w\")\n")
            code_copy = code_copy.replace("if __name__ == \'__main__\':\n",
                                          "if __name__ == \'__main__\':\n    sys.stdin = open(\"" + ipath + "\", \"r\")\n    sys.stdout = open(\"" + opath + "\", \"w\")\n")

            # print(code_copy)

            num = getmainlinenum(code_copy)

            with open(self.COPYCODEPATH, 'w') as F:
                F.write(code_copy)

            print('？？？？',self.COPYCODEPATH)
            result = os.popen("Python3 -m trace --count -C . " + self.COPYCODEPATH).read()

            print(self.COPYCODEPATH.split('/')[-1][:-8] + '_copy')
            p = getLine(self.COPYCODEPATH.split('/')[-1][:-8] + '_copy')


            okm = []

            for ind in range(len(p)):
                if 3 < p[ind] - num:
                    okm.append(p[ind] - 2)
                elif p[ind] < num:
                    okm.append(p[ind])

            retMatrix = []
            for aaa in range(totol_line):
                if aaa in okm:
                    retMatrix.append(1)
                else:
                    retMatrix.append(0)

            # print(retMatrix)

            matrix.append(retMatrix)
            ans = []
            with open(opath, 'r') as F:
                for line in F.readlines():
                    if len(line) > 1 and line[0] in '1234567890':
                        ans.append(float(line))
                    else:
                        ans.append(line)

            # print('ans:', ans)
            # print('out:', self.testCasesOutput[i])

            if len(ans) != len(self.testCasesOutput[i]):
                retLabel.append(False)
            else:
                ok = True
                for ___ in range(len(self.testCasesOutput[i])):
                    if isinstance(ans[___], float) and isinstance(self.testCasesOutput[i][___], float):
                        if -1e-10 <= ans[___] - self.testCasesOutput[i][___] <= 1e-10:
                            continue
                        else:
                            ok = False

                    elif isinstance(ans[___], str) and isinstance(self.testCasesOutput[i][___], str):
                        if ans[___] == self.testCasesOutput[i][___]:
                            continue
                        else:
                            ok = False
                            break
                    else:
                        ok = False
                        break
                retLabel.append(ok)

                os.remove(ipath)
                os.remove(opath)
        os.remove(self.COPYCODEPATH)

        # print(len(retLabel), len(matrix))
        # print(retLabel, matrix)

        return retLabel, matrix

    def analyse(self):
        # For testing
        # self.testMatrix = [[1,1,0],[1,0,1]]
        # self.testCaseLabel = [1,0]
        testCaseSet = self.ui.qtElementArea.document().toPlainText()

        self.testCasesInput, self.testCasesOutput = getTestCases(testCaseSet)

        self.more(self.testCasesInput, self.testCasesOutput)

        self.testCaseLabel, self.testMatrix = self.getlm()

        # print(self.testCaseLabel, self.testMatrix)

        if not self.testMatrix:
            return
        lines_num = len(self.testMatrix[0])

        # ---- Default Algo ----
        # Process the code in ./demo/branch.py.
        lines_group = [[0, 1, 2]]  # split_code_from_file("./demo/branch.py")
        # Generate testset for default algo.
        testset_default = []
        for idx in range(len(self.testCaseLabel)):
            label = self.testCaseLabel[idx]
            line_covs = self.testMatrix[idx]  # one-hot list
            cov_lines = [j for j in range(len(line_covs)) if line_covs[j] == 1]  # list of line index
            cov_blocks = [j for j in range(len(lines_group)) if
                          set(lines_group[j]) & set(cov_lines)]  # list of block index
            testset_default.append((cov_blocks, label))
        # Run the default algo.
        result_tmp = cal_sus(testset_default, len(lines_group))  # [(block idx, sus)]
        # Generate from block to line
        result_default = [0 for _ in self.testMatrix[0]]
        for block_idx, sus in result_tmp:
            for line in lines_group[block_idx]:
                result_default[line] = max(result_default[line], sus)

        # ---- Other 4 Algos ----
        testset = [(self.testMatrix[idx], self.testCaseLabel[idx]) for idx in range(len(self.testCaseLabel))]
        result_dstar = dstar(testset)
        result_barinel = barinel(testset)
        result_ochiai = ochiai(testset)
        result_tarantula = Tarantula(testset)

        # ---- Format ----
        result_dict = {
            "Default": np.array(result_default, dtype='f'),
            "Dstar": result_dstar,
            "Barinel": result_barinel,
            "Ochiai": result_ochiai,
            "Tarantula": result_tarantula
        }
        headers = result_dict.keys()

        # ---- Visualize ----
        self.ui.qtMatrixArea.setColumnCount(len(self.testMatrix[0]))
        self.ui.qtMatrixArea.setRowCount(len(result_dict))
        self.ui.qtMatrixArea.setHorizontalHeaderLabels([f"LINE {idx + 1}" for idx in range(lines_num)])
        self.ui.qtMatrixArea.setVerticalHeaderLabels(headers)
        self.ui.qtMatrixArea.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        for i, header in enumerate(headers):
            sus = np.around(result_dict.get(header), 2)
            for j in range(lines_num):
                item = QTableWidgetItem(str(sus[j]))
                self.ui.qtMatrixArea.setItem(i, j, item)

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
        print(filename)
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
                                                                              min(len(self.colorbar) - 1,
                                                                                  _ - 1)] + ";",
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
                text[self.choosen[_] + 4] = text[self.choosen[_] + 4].replace(
                    " background-color:#" + self.colorbar[i] + ";",
                    ""
                    , 2)

        html = ""
        for line in text:
            html += line + '\n'

        self.ui.qtCodeArea.setText(html)
        self.choosen = []

    def matrixAreaDoubleClicked(self):
        self.changeBackgroundColorToWhite()

        # Get the sus value for each line.
        row = self.ui.qtMatrixArea.currentIndex().row()
        cols = range(self.ui.qtMatrixArea.columnCount())
        values = [self.ui.qtMatrixArea.item(row, col).text() for col in cols]

        # Update invalid value.
        valid_values = [float(value) for value in values if value != "nan" and value != "inf"]
        min_value, max_value = min(valid_values), max(valid_values)
        new_values = []
        for value in values:
            if value == "nan":
                new_values.append(min_value - 10)
            elif value == "inf":
                new_values.append(max_value + 10)
            else:
                new_values.append(float(value))
        # find index
        full_sort = np.argsort(new_values)
        self.choosen = [0] + list(full_sort[:int(len(values) / 2)] + 1)

        self.changeBackgroundColorToRed()

    def openCodeFile(self, codeFileName=None):

        self.testCase = []
        self.line = 0

        if not codeFileName:
            codeFileName, _ = QFileDialog.getOpenFileName(self.ui, 'open file',
                                                          './demo',
                                                          'Excel files(*.c , *.cpp , *.py)')

        self.fileName = codeFileName
        print(self.fileName)
        # print(self.fileName.split('.')[-2].split('/')[-1])
        self.PYTHONCODEFILENAME = self.fileName.split('.')[-2].split('/')[-1]
        self.COPYCODEPATH = './demo/' + self.PYTHONCODEFILENAME + '_copy.py'

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
