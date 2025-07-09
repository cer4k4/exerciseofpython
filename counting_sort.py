template = {}
sourclist=[1,5,5,9,5,1,2,6,3,4,6,5,1]
sortedlist=[]

def Min(template):
    return min(template.keys())

def CreateCountDicTemplate(sourclist):
    for x in sourclist:
        try:
            template[x] += 1
        except:
            template[x] = 1
    return template

def CreateSortList(template):
    while template:
        min_key = Min(template)
        for _ in range(template[min_key]):
            sortedlist.append(min_key)
        del template[min_key]
    print('sortedlist\n',sortedlist)

print('sourcelist\n',sourclist,'\n')        
print('template\n',CreateCountDicTemplate(sourclist),'\n')
CreateSortList(template)


        