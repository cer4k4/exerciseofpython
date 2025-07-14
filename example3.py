nums = [0,1,1254,5]
x = 1

def giveIndex(x,nums):
    for index in range(len(nums)):
        if x == nums[index]:
            return index
    return -1

found_index = giveIndex(x,nums)
print(found_index)

