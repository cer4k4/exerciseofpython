my_array = [0, 1, 1, 2]


def test_old(a):
    if a == 0:
        return 0
    elif a == 1:
        return 1
    elif a == 2:
        return 1
    else:
        return test_old(a-1)+test_old(a-2)


def test(n):
    if n > 3:
        for index in range(4, n+1):
            my_array.append(my_array[index-1] + my_array[index-2])
    return my_array[n]


print("start test old")
print(test_old(40))
print("end test old")
print("start test new")
print(test(40))
print("end test new")
