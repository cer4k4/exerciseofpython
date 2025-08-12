import random
import string
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["local"]
mycol = mydb["ascii"]
giveASCIIcode = dict()


def encrytion(data):
    temp = ""
    for char in data:
        ascii = giveASCIIcode[char] * 2
        for itrator in str(ascii):
            temp = temp + itrator + \
                ''.join([random.choice(string.ascii_letters)
                        for _ in range(10)])
        temp += ","
    return temp[:-1]


for data in mycol.find({}, {"_id": 0}):
    giveASCIIcode[data["symbol"]] = data["ascii code"]
# Give ascii code and product to 2

while True:
    print("Enter you're word to encrypt")
    word = input()
    encrypted = encrytion(word)
    print("encrypted ===>", encrypted, "\n")
