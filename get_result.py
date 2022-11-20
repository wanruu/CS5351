from ft_based import split_code_from_file
import xlwt
f = xlwt.Workbook('encoding = utf-8') #设置工作簿编码
sheet1 = f.add_sheet('sheet1',cell_overwrite_ok=True) #创建sheet工作表
def getline(file_name):
    count = 0
    list = []
    with open(file_name) as lines:
        for line in lines:
            count += 1
            line = line.strip('\n')
            if line[5] == ':':
                list.append(count)
    return list

def get_result(list, test_file):
    list2=split_code_from_file(test_file)
    temp=[]
    for num in list:
        count = 0
        for list2_line in list2[2::]:
            count += 1
            for num2 in list2_line:
                if num == num2 and count not in temp:
                    temp.append(count)

    return temp

def get_errorLine(result, test_file):
    list2 = split_code_from_file(test_file)
    errorBlock = []
    for item in result:
        if item[1] != 0.0:
            errorBlock.append(item[0])

    errorLines = []
    errorLines.append([0])
    for i in errorBlock:
        errorLine = [0]
        for j in list2[i]:
            errorLine.append(j)
        errorLines.append(errorLine)

    return errorLines

def generateExcel(list):
    row = 0
    for i in list:
        column = 0
        for j in i:
            sheet1.write(row, column, j)
            column += 1
        row += 1
    f.save('text.xls')


#result = [(0, 0.0), (1, 0.0), (2, 0.125), (3, 0.125), (4, 0.0), (5, 0.0), (6, 0.0), (7, 0.0), (8, 0.0), (9, 0.0), (10, 0.0), (11, 0.0)]
#print(get_errorLine(result, '/Users/liujiaqi/PycharmProjects/SETest/test.py'))



