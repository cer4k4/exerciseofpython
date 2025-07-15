while True:
    word = input()
    for x in range(len(word)):
        if x % 2 == 0:
            print(word[x])
    print("\n")