nums = [0,1,1254,5]
x = 1000
found_index = -1
for index,number in enumerate(nums):
    if x == number:
        found_index = index
print(found_index)