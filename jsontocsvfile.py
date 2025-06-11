import json
import csv
import requests
from fastapi import FastAPI
from pydantic import BaseModel

class User(BaseModel):
    name: str
    family: str
    age: int
    address: str

app = FastAPI()


@app.post("/user")
async def registerUser(user: User):
    userDict = {
        'name':user.name,
        'family':user.family,
        'age':user.age,
        'address':user.address
    }

    return {"message": "user registered"}


#jsreq = [{'name':'ali','family':'karimi','age':26,'address':'tehran,dollab'}]

def saveToCSVfile(user):
    with open('my_data.csv','w') as file:
        csvfieldsName = ['name','family','age','address']
        writer = csv.DictWriter(file,fieldnames=csvfieldsName)
        writer.writeheader()
        writer.writerows(jsreq)




@app.post("/test")
async def test():
    result = requests.get(url="https://dummyjson.com/products")
    return result