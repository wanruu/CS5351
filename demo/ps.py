import sys


def mid(x, y, z):
    m = z
    if y < z:
        if x < y:
            m = y
        elif x < z:
            m = y
    else:
        if x > y:
            m = y
        elif x > z:
            m = x
    return m


if __name__ == '__main__':
    a = float(input())
    b = float(input())
    c = float(input())

    d = mid(a, b, c)

    print(d)
