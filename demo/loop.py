import sys


def bubbleSort(arr):
    n = len(arr)

    for i in range(n):

        for j in range(1, n - i - 1):

            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


if __name__ == '__main__':
    L = float(input())
    arr = []
    for i in range(int(L)):
        a = float(input())
        arr.append(a)

    bubbleSort(arr)

    for i in arr:
        print(i)
