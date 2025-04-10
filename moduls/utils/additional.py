def print_table(data, width):
    cols = len(data[0])

    data_new = []
    for i in range(cols):
        a = []
        for row in data:
            line = row[i]
            a.append(line)
        max_len = len(max(a, key=lambda x: len(x)))
        len_col = max_len + width
        for i in range(len(a)):
            a[i] = a[i] + (len_col - len(a[i])) * ' '
        data_new.append(a)

    transposed_data_new = [list(sublist) for sublist in zip(*data_new)]
    data_done = [''.join(x) for x in transposed_data_new]
    return data_done


if __name__ == "__main__":
    data = [['<b>ID</b>','<b>Время</b>'],
            ['5', '00:03:88'],
            ['7', '00:05:30'],
            ['99', '00:06:83']]

    print(print_table(data, 2))