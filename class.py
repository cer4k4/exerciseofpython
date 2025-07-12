class Person:
    def __init__(self,name,age):
        self.name = name
        self.age = age

    def showInfo(self):
        print("Name:",self.name,"\nAge:",self.age)

p = Person("ali",26)
print(p.showInfo())