categories = {
    "pelak":{"count":1,"time":888,"data":[{"_id":12,"number":"2655455"},{"_id":12,"number":"2655455"}]},
    "numbers":{"count":5,"time":1223,"data":[{"_id":12223,"phone":"0999812654"},{"_id":4555,"phone":"0938554488"}]},
    "national_code":{"count":2,"time":1000,"data":[{"_id":13,"number":"265545"},{"_id":1445,"number":"41555"},]},
}

val = input("Enter your time: ")

for c in categories:
  if int(val) <= categories[c]["time"]:
    print("\n")
    print(c,"\ndata of category",c,"  ---->  ",categories[c]["data"])