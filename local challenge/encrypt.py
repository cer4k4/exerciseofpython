import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["local"]
mycol = mydb["ascii"]

giveASCIIcode,giveCharacter = dict(),dict()

for data in mycol.find({},{"_id":0}):
    giveASCIIcode[data["symbol"]] = data["ascii code"]
    giveCharacter[data["ascii code"]] = data["symbol"]

def encrytion(data):
    temp = ""
    for char in data:
        tint = giveASCIIcode[char] * 2
        temp = temp + str(tint) + ","
    return temp

def decrytion(data):
    temp = ""
    word = ""
    for number in data:
        if number != ",":
           temp += number
        else:
            iemp = int(temp) / 2
            word += giveCharacter[iemp]
            temp = ""
    return word

while True:
    print("Do you want encrypt or decrypt")
    word = input()
    encrypted = encrytion(word)
    print("encrypted",encrypted)
    print("decripted",decrytion(encrypted))
    
