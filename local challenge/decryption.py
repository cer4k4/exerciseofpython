import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["local"]
mycol = mydb["ascii"]
giveCharacter = dict()


# Checker for that character Is number
def isnumber(char):
    try:
        int(char)
        return char
    except:
        pass


# Decprit data with seprate "," and after that devide to 2 and give to character with ascii code
def decrytion(data):
    temp = ""
    word = ""
    data += ","
    for char in data:
        if char != ",":
            number = isnumber(char)
            if number:
                temp += str(number)
        else:
            iemp = int(temp) / 2
            word += giveCharacter[iemp]
            temp = ""
    return word


for data in mycol.find({}, {"_id": 0}):
    giveCharacter[data["ascii code"]] = data["symbol"]

while True:
    print("Enter you're string to decrypt")
    word = input()
    print("decripted ===>", decrytion(word), "<===", "\n")
