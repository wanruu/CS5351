import pandas as pd
import math

"""
Part 1: Divide code according to heading spaces
"""

def count_heading_spaces(string: str) -> int:
    """判断一行前的空格有多少.

    Args:
        string: a given string.
    Return:
        The number of space in the beginning of the string.
    """
    count = 0
    for char in string:
        if char == " ":
            count += 1
        else:
            return count


def split_code_from_file(filepath: str) -> [[int]]:
    """Read and split code from an file.

    Args:
        filepath: the path of file to be dealt with.
    Return:
        Same as function split_code.
    """
    with open(filepath) as file:
        lines = file.readlines()  # [str]
    return split_code(lines)


def split_code(lines: [str]) -> [[int]]:
    """Split code into several elements according to the indent.
    获取每一行对应的元素的划分，以列表的形式呈现

    Args:
        lines: Each line is a string. Lines represent the whole code.
    Return:
        A list. Each item of the list represents a group of lines (i.e. an element).
    """

    # 1. Initialize result
    result = []
    last_space = -1  # heading space num of last line
    last_node = -1  # index of last section in result

    # 2. 遍历每一行
    for index, line in enumerate(lines):
        # 2.1. Deal with empty line
        if line == "\n" or not line:
            continue

        # 2.2. Get heading space num of current line
        spaces = count_heading_spaces(line)

        # 2.3. Deal with first un-empty line
        if last_space == -1:
            result.append([[index], spaces])
            last_space = spaces
            last_node = 0
            continue

        # 2.4. 如果没有进位
        if spaces == last_space:
            result[last_node][0].append(index)

        # 2.5. 如果比起上一行往前偏移了4个单位
        if spaces == last_space + 4:
            result.append([[index], spaces])
            last_node = len(result) - 1
            last_space = spaces

        # 2.6. 如果某些域结束了，缩进归位
        if spaces < last_space:
            for j in range(len(result)):
                if result[-1-j][1] == spaces:
                    result[-1-j][0].append(index)
                    lastnode = len(result)-1-j
                    last_space = spaces
                    break
    return [item[0] for item in result]


# # 将当前输入包含了哪些行转化为包含了哪些元素，rowlist是一些行的列表，将其转化为元素的列表
# def rowtoele(rowlist, elementlist):
#     coverelelist = []
#     for i in range(len(rowlist)):
#         for j in range(len(elementlist)):
#             if rowlist[i] in elementlist[j]:
#                 if j not in coverelelist:
#                     coverelelist.append(j)
#     return coverelelist


"""
Part 2: 计算可疑度
定义:
1. testcase的格式为([int], int):
    [int]代表该用例覆盖的代码元素索引;
    int代表该用例是否执行成功, 1-成功, 0-失败.
2. testset的格式为[testcase].
"""

# 优化: xlsx文件header乱序
def get_testset(filepath: str) -> [([int], int)]:
    """Get testset from an xlsx file. 读取xlsx文件, 获取test set覆盖图谱.

    Args:
        filepath: The path of the xlsx file.

    Returns:
        testset(a list of testcase)
    """

    df = pd.read_excel(filepath)  # DataFrame
    testset = list(df.to_dict("index").values())  # [{0: x, 1: x, ..., n: x, "Success": x}]

    result = []
    for testcase in testset:
        coverage = [key for key, value in testcase.items() if type(key) == int and value == 1]
        success = testcase.get("Success")
        result.append((coverage, success))
    return result


def manhattan_dist(xa: ([int], int), xb: ([int], int)) -> int:
    """计算两个测试用例之间的曼哈顿距离.

    Args:
        xa: a testcase.
        xb: another testcase.
    Returns:
        manhanttan distance of two testcase.
    """
    dist = 0
    dist += sum([1 for value in xa[0] if value not in xb[0]])
    dist += sum([1 for value in xb[0] if value not in xa[0]])
    return dist


def cal_sus(testset: [([int], int)], element_num: int) -> [(int, int)]:
    """对于一个覆盖图谱，计算并返回元素可疑度排序.

    Args:
        testset: a list of testcase
        element_num: the number of elements in the whole code
    Return:
        A list of tuple (element index, equivocation statistic).
    """

    # 1. 根据测试结果成功与否，将覆盖图谱分为D+与D-
    d1 = [test_case for test_case in test_set if test_case[1] == 1]  # success
    d2 = [test_case for test_case in test_set if test_case[1] == 0]  # fail

    # 2. 可疑度初始化
    sus_list = [0 for i in range(element_num)]

    # 3. 遍历每一个测试样例
    for test_case in test_set:
        # 3.1. 计算该样例与所有正样例和负样例的曼哈顿距离，找到除本身外最近的样例
        dist_d1 = [(manhattan_dist(test_case, test_case_d1), test_case_d1) for test_case_d1 in d1 if test_case_d1 != test_case]
        dist_d2 = [(manhattan_dist(test_case, test_case_d2), test_case_d2) for test_case_d2 in d2 if test_case_d2 != test_case]
        dist_d1.sort(key=lambda x: x[0])
        dist_d2.sort(key=lambda x: x[0])
        closest_d1 = dist_d1[0][1] if dist_d1 else []
        closest_d2 = dist_d2[0][1] if dist_d2 else []

        # 3.2. 遍历每一个元素，对每一个元素更新 (对每一个覆盖特征f)
        for element in test_case[0]:
            # 计算缺陷相关统计量
            diff_d1 = 0 if not closest_d1 or element in closest_d1[0] else 1
            diff_d2 = 0 if not closest_d2 or element in closest_d2[0] else 1
            defect_co_stat = -test_case[1] * (-diff_d1 + diff_d2)
            sus_list[element] += defect_co_stat


    final_list = [(index, value/len(test_set)) for index, value in enumerate(sus_list)]
    # 排序后返回元素的可疑度排序
    # final_list.sort(key=lambda x: x[1], reverse=True)
    return final_list


# test_set = [
# ([0, 1, 2, 5], 0),
# ([0, 4, 5], 1),
# ([0, 1, 2, 5], 1),
# ([0, 1, 3, 5], 0),
# ([0, 1, 2, 5], 0),
# ([0, 1, 3, 5], 1),
# ([0, 4, 5], 1),
# ([0, 1, 2, 5], 0)
# ]
# print(cal_sus(test_set, 6))

