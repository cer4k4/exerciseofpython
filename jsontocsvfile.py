import json
import csv


jsreq = '{"name":"ali","family":"karimi","age":26,"address":"tehran,dollab"}'

y = json.dumps(jsreq)

y = json.loads(jsreq)

print(type(y))



with open('my_data.csv',w,newline='') as file:
    csvfieldsName = ['name','family','age','address']
    writer = csv.DictWriter(file,)
    writer.writeheader()
    writer.writerows(y)