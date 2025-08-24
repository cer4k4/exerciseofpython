import random
print("input you're number")
masterList = []

number = int(input())

    

if number >=4:
    print("khar.... khoroji dare")
    def create_master_and_queen(number:int, masterList:list):
        if number == 0:
            return
        sublist = []
        masterList.append(sublist)
        create_master_and_queen(number-1, masterList)
    
    def createhomes(input, number):
        for l, value in enumerate(input):
            if type(value) == list:
                for c in range(number):
                    if len(value) < number:
                        value.append(" ")
    
    def mark_attacks(row, col, masterList):
        n = len(masterList)
        for c in range(n):
            if c != col and masterList[row][c] == " ":
                masterList[row][c] = "*"
        for r in range(row+1, n):
            # همان ستون
            if masterList[r][col] == " ":
                masterList[r][col] = "*"
            # قطر چپ
            left = col - (r - row)
            if 0 <= left < n and masterList[r][left] == " ":
                masterList[r][left] = "*"
            # قطر راست
            right = col + (r - row)
            if 0 <= right < n and masterList[r][right] == " ":
                masterList[r][right] = "*"
    
    def is_safe(masterList, row, col):
        return masterList[row][col] == " "
    
    def solve_nqueens(masterList, row=0):
        n = len(masterList)
        if row == n:
            return True  # همه ملکه‌ها گذاشته شدن
        
        cols = list(range(n))
        random.shuffle(cols)  # ستون‌ها رو رندوم می‌کنیم
        
        for col in cols:
            if is_safe(masterList, row, col):
                # کپی از صفحه می‌گیریم (برای بک‌ترکینگ)
                snapshot = [r.copy() for r in masterList]
                
                masterList[row][col] = "Q"
                mark_attacks(row, col, masterList)
                
                if solve_nqueens(masterList, row+1):
                    return True
                
                # بک‌ترک: برگردیم به حالت قبلی
                for r in range(n):
                    masterList[r] = snapshot[r]
        
        return False
    
    def beautifulPrint():
        for row in masterList:
            print(row)
        print()
    
    # ----------- اجرای برنامه ----------
    masterList.clear()
    create_master_and_queen(number, masterList)
    createhomes(masterList, number)
    
    solve_nqueens(masterList, 0)
    print("inam khoroji")
    beautifulPrint()
elif number <= 0:
    print("khar.... add bozorg tar vared kon")
else:
    print("khar.... zir 4 khoroji nadare")