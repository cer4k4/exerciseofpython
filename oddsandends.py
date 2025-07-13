from dataclasses import dataclass

@dataclass
class Employee:
    name: str
    dept: str
    salary: int



aka = Employee('ali','karimi',6000000)

print(aka)
