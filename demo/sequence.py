import sys


def addFourNumbers(a, b, c, d):
    s = 0
    s += a
    s += b
    s += c
    # s += d
    s += b
    return s


if __name__ == '__main__':
    a = float(input())
    b = float(input())
    c = float(input())
    d = float(input())

    s = addFourNumbers(a, b, c, d)

    print(s)
