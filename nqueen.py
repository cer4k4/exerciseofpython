import random


number = int()


class NQueen():
    def __init__(self, number):
        self.master_list = list()
        self.number = number
        if self.number >= 4:
            print("khar.... khoroji dare")
        elif self.number <= 0:
            print("khar.... add bozorg tar vared kon")
        else:
            print("khar.... zir 4 khoroji nadare")

    def create_master_and_queen(self, number: int, master_list: list):
        if number == 0:                                                     
            return                                                          
        sub_list = []                                                       
        master_list.append(sub_list)                                   
        self.create_master_and_queen(number-1, master_list)

    def create_homes(self, master_list, number):
        for sub_list in master_list:
            if type(sub_list) == list:
                for _ in range(number):
                    if len(sub_list) < number:
                        sub_list.append(" ")

    def mark_attacks(self, row, col, master_list):
        n = len(master_list)
        for c in range(n):
            if c != col and master_list[row][c] == " ":
                master_list[row][c] = "-"
        for r in range(row+1, n):
            # itrate column
            if master_list[r][col] == " ":
                master_list[r][col] = "-"
            # left
            left = col - (r - row)

            if 0 <= left < n and master_list[r][left] == " ":
                master_list[r][left] = "-"
            # right
            right = col + (r - row)
            if 0 <= right < n and master_list[r][right] == " ":
                master_list[r][right] = "-"
        #self.beautiful_print(master_list)
        #print(n,row)


    def is_safe(self, master_list, row, col):
        return master_list[row][col] == " "

    def solve_nqueens(self, master_list, row=0):
        n = len(master_list)
        if row == n:
            return True  # Put ♛
        cols = list(range(n))
        random.shuffle(cols)
        for col in cols:
            if self.is_safe(master_list, row, col):
                snapshot = [r.copy() for r in master_list]
                master_list[row][col] = "♛"
                self.mark_attacks(row, col, master_list)
                if self.solve_nqueens(master_list, row+1):
                    return True
                for r in range(n):
                    master_list[r] = snapshot[r]
        print("      Not True     ")
        self.beautiful_print(master_list)
        return False

    def beautiful_print(self, master_list):
        for row in master_list:
            print(row)
    def solve(self):
        self.master_list.clear()
        try:
            self.create_master_and_queen(number=self.number, master_list=self.master_list)
            self.create_homes(number=self.number, master_list=self.master_list)
            self.solve_nqueens(master_list=self.master_list, row=0)
            self.beautiful_print(master_list=self.master_list)
        except Exception as error_msg:
            print("error message: ", str(error_msg))

n_queen_obj = NQueen(number=number)
n_queen_obj.solve()
