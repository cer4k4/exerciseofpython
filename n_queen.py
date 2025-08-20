import random
# def create_chees(num):
#     list = []
#     for n in range(num):
#         sublist = []
#         for index,value in enumerate(range(num)):
#             sublist.append("x")
#             if len(sublist) != num:
#                 sublist.insert(index+1,".")
#         list.append(sublist)
#     return list

# def negetive_itrate_list(index,list):
#     list[index] = "."

# number = int(input())
# result = create_chees(number)
# for r in result:
#     print(r)  





#num = int(input())
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
                    value.append("")
            
def put_first_queen(index:int,list1:list,masterList:list[list]):
    list1[index]="Q"
    for numberlist,m in enumerate(masterList):
        for indexdata,val in enumerate(m):
            if val != "Q":
                m[indexdata]="*"





dice_roll = random.randint(1, number)
createhomes(masterList,number)

put_first_queen(dice_roll,masterList[0],masterList)


def BeautifulPrint(masterList:list):
    for list in masterList:
        print(list)

BeautifulPrint(masterList)


#print("master",masterList)
