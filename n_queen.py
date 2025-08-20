import random

masterList = []
number = 4
def create_master_and_queen(number:int,masterList:list):
    if number == 0:
        return
    sublist = []
    masterList.append(sublist)
    create_master_and_queen(number-1,masterList)

create_master_and_queen(4,masterList)


def createhomes(input,number):
    for l,value in enumerate(input):
        if type(value) == list:
            for c in range(number):
                if len(value) < number:
                    value.append(" ")
            

def put_first_queen(index:int, list1:list, masterList:list[list]):
    col = index - 1
    list1[col] = "Q"
    
    for row, m in enumerate(masterList):
        if row == 0:
            for c in range(len(m)):
                if c != col:
                    m[c] = "*"   
        else:
            m[col] = "*"
            left = col - row
            if 0 <= left < len(m):
                m[left] = "*"
            right = col + row
            if 0 <= right < len(m):
                m[right] = "*"




dice_roll = random.randint(1, number)
createhomes(masterList,number)


put_first_queen(dice_roll,masterList[0],masterList)

listnullvalue = dict()
def givenullhouse(masterList:list):
    for il,list in enumerate(masterList):
        nulls = []
        for index,val in enumerate(list):
            if val == " ":
                nulls.append(index)
        listnullvalue.update({il:nulls})
givenullhouse(masterList)


for n in listnullvalue:
    if listnullvalue.get(n):
        if len(listnullvalue.get(n)) > 1:
            for s in listnullvalue.get(n):
                print(s,n)
        else:
            val = listnullvalue.get(n)
            print(val[0])
            




def beautifulPrint():
    for list in masterList:
        print(list)


beautifulPrint()
print(listnullvalue)
#print("master",masterList)



