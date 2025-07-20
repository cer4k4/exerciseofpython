# a function give hours and level( bs , master , PHD or other ) and calcute working time in this time
class Employee:
    def __init__(self,level,worktime):
        self.level = level
        self.working_time_in_hours = worktime
    
    def work_hours_callcute(self):
        if self.level == "Bachelor":
            return self.working_time_in_hours * 100
        elif self.level =="Master":
            return self.working_time_in_hours * 500
        elif self.level =="PHD":
            return self.working_time_in_hours * 1000
        else:
            # Not educated
            return self.working_time_in_hours * 80
        
while True:
    print("Choice the level of educated")
    print("1)Bachelor\n2)Master\n3)PHD")
    emp = Employee("",0)
    ilevel = int(input())
    if ilevel == 1:
        emp.level = "Bachelor"
    elif ilevel == 2:
        emp.level = "Master"
    elif ilevel == 3:
        emp.level ="PHD"
    print("Ok give me how much work hours in this mounth")
    ihours = int(input())
    emp.working_time_in_hours = ihours
    print("you're salary is: ",emp.work_hours_callcute(),"\n")
    print("-------------------------------------------------")
    
        