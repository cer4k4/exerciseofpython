while True:
    print("\nnumber1 = ")
    a = int(input())

    print("number2 = ")
    b = int(input())

    def productNumbers(a,b):
        if (a * b) >= 1000:
            return a+b
        return a * b

    print("\nThe result is ",productNumbers(a,b))
    print("--------------------------------")