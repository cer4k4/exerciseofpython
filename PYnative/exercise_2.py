while True:
    number = int(input())
    nums = range(number)
    print(f"Printing current and previous number sum in a range({number})")
    for index,num in enumerate(nums):
            if index != 0:
                print("Current Number",index,"Previous Number",index-1,"Sum:",nums[index]+nums[index-1])
            else:
                print("Current Number",index,"Previous Number",index,"Sum:",nums[index])