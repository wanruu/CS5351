import re
import numpy as np
# import csv
# print("length",len(data))
def getLine(name):
    index = 1
    numlist = []
    z = r"    \d"
    file_path = r'.'+name+'.cover'
    data = []
    # #读取
    with open(file_path, encoding='utf-8', ) as txtfile:
        line = txtfile.readlines()
        for i, rows in enumerate(line):
            data.append(rows)
    txtfile.close()
    for j in data:
        a=re.findall(z,j)
        if a:
            #print((a[0])[4])
            # findall返回一个个独立只含有一个元素的元组，取每个元组的第一个，
            # 每个元组都是前面四个空格加一个数字的形式，再取第五个数字元素
            numlist.append(index)
        index += 1

    return numlist
#结果：['1', '1', '1', '1', '4', '3', '3', '1', '1', '1']