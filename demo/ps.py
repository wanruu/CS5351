def quick_sort(data):

    if len(data) >= 2:
        mid = data[len(data) // 2]
        left, right = [], []
        data.remove(mid)
        for num in data:
            if num >= mid:
                right.append(num)
            else:
                left.append(num)
        return quick_sort(left) + [mid] + quick_sort(right)
    else:
        return data


if __name__ == '__main__':
    num_ = eval(input())
    data = []
    for i in range(num_):
        data.append(input())
    sorted_data = quick_sort(data)
    for i in sorted_data:
        print(i)
