import requests
import csv

result = requests.get(url="https://dummyjson.com/products")
if "html" in result.headers.get("Content-Type"):
    print(result.text)
elif "json" in result.headers.get("Content-Type"):
    response = result.json()
    # response = [{
    #     "products":"car",
    #     "a":1,
    #     "b":"s",
    #     "c":["ahmad","hosein"],
    #     "h":{"fmily":"raiegan"},
    #     "j":[{"name":"jjj"}]
    #     }]
    fields = []

    for iterater in response:
        if type(iterater) == dict:
            listkeys = []
            print(iterater)
            keys = iterater.keys()
            for k in keys:
               listkeys.append(k)
            uniquekeys = set(listkeys)
            for u in uniquekeys:
               fields.append(u)

        elif type(response[iterater]) == list:
            listkeys = []
            for counter in range(len(response[iterater])):
                keys = response[iterater][counter].keys()
                for k in keys:
                    listkeys.append(k)
            uniquekeys = set(listkeys)
            for u in uniquekeys:
                fields.append(u)
        else:
            fields.append(iterater)
    


def saveToCSV(response):
    with open('my_data.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        
        for res in response:
            if type(res) == dict:
                writer.writerow(res)
            elif type(response[res]) == list:
                writer.writerows(response[res])
            else:
                single_row = {field: response[res] if field == res else '' for field in fields}
                writer.writerow(single_row)
    
    print("Data successfully written")
    # else:
    #     print("Unsupported content type:", result.headers.get("Content-Type"))