# Exercise 4: Remove first n characters from a string
def remove_chars(word,n):
    newWord=""
    for index,value in enumerate(word):
        if index >= n:
            print(newWord+value,index)
    return newWord
while True:
    print("Enter You're word")
    word = input()
    print("How many do you want delete character")
    deletechar = int(input())
    if deletechar >= len(word):
        print("word or deletechar number is not true")
    else:
        remove_chars(word,deletechar)