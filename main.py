from elasticsearch import Elasticsearch
from collections import deque

req = {
    "index_names":["a","b","c","d"],
    "Lname": "i",
}


class ConnectionElasticsearch:
    def __init__(self):
        self.es = Elasticsearch('http://172.16.150.124:9200', basic_auth=("elastic","asdf1212Zxcv"))
        #self.es = Elasticsearch(f"http://{"172.16.150.124"}:{"9200"}",headers={"Accept": "application/vnd.elasticsearch+json; compatible-with=8"},http_auth=("elastic", "asdf1212Zxcv"))

    def get_data_by_filter(self, index, filter,val):
        try:
            query = {
                "query": {
                    "term": {
                        filter: {
                            "value": val
                        }
                    }
                }
            }
            result = self.es.search(index=index,body=query)
            return result
        except NotFoundError:
            self.create_index_if_not_exists(index)
            return {"hits": {"hits": []}}

    def create_index_if_not_exists(self, index):
        if not self.es.indices.exists(index=index):
            mapping = {
                "mappings": {
                    "properties": {
                        "phone_number": {"type": "keyword"},
                        "email": {"type": "keyword"},
                        "name": {"type": "text"},
                        "created_at": {"type": "date"}
                    }
                }
            }
            self.es.indices.create(index=index, body=mapping)


    def insert_document(self, index, doc_id,body):
        try:
            result = self.es.index(index=index, id=doc_id, body=body)
            return result
        except Exception as e:
            print(f"Elasticsearch index error: {e}")
            return None

    
    def count_of_index(self, index, field, mindate, maxdate):

        query = {
            "query": {
                "range": {
                    field: {
                        "gte": mindate,
                        "lte": maxdate
                    }
                }
            },
            "aggs": {
                "logins_per_day": {
                    "date_histogram": {
                        "field": field,
                        "interval": "day",
                        "min_doc_count": 0,
                        "extended_bounds": {
                            "min": mindate,
                            "max": maxdate
                        }
                    }
                }
            }
        }
        result = self.es.search(index=index, body=query)
        return result['aggregations']['logins_per_day']['buckets']

    def update_document(self,index,id,doc):
        return self.es.index(index=index,id=id,body=doc)
    
    def get_documents(self,index,feild,val,page,size):
        if feild is None:
            query = {
                "from":page,
                "size":size
            }
            result = self.es.search(index=index,body=query)
            return result["hits"]["hits"]
        if type(val) == int:
            query = {
                "from":page,
                "size":size,
                "query": {
                    "match":{
                        feild:val
                    }
                }
            }
            result = self.es.search(index=index,body=query)
            return result["hits"]["hits"]
        if type(val) == str:
            query = {
                "from":page,
                "size":size,
                "query": {
                    "regexp":{
                        feild: f".*{val}.*"
                    }
                }
            }
            result = self.es.search(index=index,body=query)
            return result["hits"]["hits"]
        
    def delete_document(self,index,id):
        try:
            result = self.es.delete(index=index,id=id)
            return result["result"]
        except Exception as e:
            print(f"Elasticsearch index error: {e}")
            return e.__dict__["body"]["result"]
            
    def get_documents2(self, index, feild=None, val=None):
        if feild is None:
            query = {"query": {"match_all": {}}}
        else:
            query = {"query": {"regexp": {feild: f"{".*"+val+".*"}"}}}
    
        result = self.es.search(index=index, body=query)
        return result
    
    def get_documents3(self, index, feild=None, val=None):
        query = {"query": {"match": {feild: val}}}
        result = self.es.search(index=index, body=query)
        return result









    def get_fileds_of_index(self,index,field_name):
        mappings = self.es.indices.get_mapping(index=index)
        indices_with_field = []
        new_fileds_founded = []
        for index, mapping_data in mappings.items():
            properties = mapping_data.get("mappings", {}).get("properties", {})
            if field_name in properties:
                resp = self.es.search(
                    index=index,
                    size=1,
                    query={
                        "exists": {"field": field_name}
                    }
                )
                if resp["hits"]["total"]["value"] > 0:
                    indices_with_field.append(index)
                    for foundnewfild in list(properties):
                        if field_name != foundnewfild:
                            if foundnewfild in properties:
                                resp = self.es.search(
                                index=index,
                                size=1,
                                query={
                                    "exists": {"field": foundnewfild}
                                }
                            )
                            if resp["hits"]["total"]["value"] > 0:
                                new_fileds_founded.append(foundnewfild)
        return  indices_with_field,new_fileds_founded
    
databaseConnection = ConnectionElasticsearch()
#databaseConnection.get_documents2(index="a",feild="Fname",val="i")
findfeilds = dict()
newfindfeilds = dict()
s = list(req.keys())


def search_filed_in_index(indexlist,filed,newfiledflag,foundinindex):
    if newfiledflag is False:
        for index in indexlist:
            indexFound,new_found_fileds = databaseConnection.get_fileds_of_index(index,filed)
            if len(indexFound) != 0:
                for i in indexFound:
                    findfeilds.update({filed:True,i:True})
            if len(new_found_fileds) != 0:
                    for n in new_found_fileds:
                        newfindfeilds.update({n:True,index:True})
        return
    # for index in indexlist:
    #     if index != foundinindex:
    #         indexFound,new_found_fileds = databaseConnection.get_fileds_of_index(index,filed)
    #         if len(indexFound) != 0:
    #             for i in indexFound:
    #                 findfeilds.update({filed:True,i:True})
    #             if len(new_found_fileds) != 0:
    #                     for n in new_found_fileds:
    #                         newfindfeilds.update({n:True,index:True})
    # return

# search_filed_in_index(req.get("index_names"),"Fname",False,"")
# print("Filed",findfeilds,"New Filed",newfindfeilds)
# s = list(newfindfeilds.keys())
# print(s)
# search_filed_in_index(req.get("index_names"),s[0],True,s[1])
# print("Filed",findfeilds,"New Filed",newfindfeilds)


# def getNewFilds(indexes,fild):
#     for index in indexes:
#         newlistindexs,listfilds = databaseConnection.get_fileds_of_index(field_name=fild,index=index)
#         if len(newlistindexs) != 0:
#             print(newlistindexs,listfilds) # [a] [Lname]
#             for n in indexes:              # [a,b,c,d]
#                 if n not in newlistindexs: # a != [a]
#                     for l in listfilds:    # Lname
#                         newlistindexs1,listfilds1 = databaseConnection.get_fileds_of_index(field_name=l,index=n) # [Lname] [b] --> [b] [city] && [Lname] []
#                         if len(newlistindexs1) != 0:
#                             print(newlistindexs1,listfilds1)
#                             for nn in indexes:
#                                 if nn not in newlistindexs1:
#                                     for ll in listfilds1:
#                                         newlistindexs2,listfilds2 = databaseConnection.get_fileds_of_index(field_name=ll,index=nn)
#                                         if len(newlistindexs2) != 0:
#                                             print(newlistindexs2,listfilds2)


# getNewFilds(req.get("index_names"),"Fname")


# def getNewFields(indexes, field, depth=0, max_depth=3):
#     if depth > max_depth:  
#         return    
#     for index in indexes:
#         new_indexes, fields = databaseConnection.get_fileds_of_index(field_name=field, index=index)
#         if not new_indexes:
#             continue

#         print(new_indexes, fields)

#         for f in fields:
#             for n in indexes:
#                 if n not in new_indexes:
#                     getNewFields([n], f, depth + 1, max_depth)


# getNewFields(req.get("index_names"), "city")


# def getNewFields(indexes, field, relations, depth=0, max_depth=5):
#     if depth > max_depth:
#         return
    
#     for index in indexes:
#         new_indexes, fields = databaseConnection.get_fileds_of_index(field_name=field, index=index)
#         if not new_indexes:
#             continue


#         if index not in relations:
#             relations[index] = set()
#         relations[index].update(fields)

#         print(new_indexes, fields)


#         for f in fields:
#             for n in indexes:
#                 if n not in new_indexes:
#                     getNewFields([n], f, relations, depth + 1, max_depth)

# visited_fields = set()
# relations = {}
# for f in ["Lname","city"]:
#     getNewFields(req.get("index_names"), f, relations)
#     print("Fname:", relations)

#######################################################################################
# def getNewFields(indexes, field, relations, depth=0, max_depth=5):
#     if depth > max_depth:
#         return
    
#     for index in indexes:
#         new_indexes, fields = databaseConnection.get_fileds_of_index(field_name=field, index=index)


#         if not new_indexes:
#             if index not in relations:
#                 relations[index] = {}
#             continue
#         if index not in relations:
#             relations[index] = {}
#         for f in fields:
#             relations[index][f] = "found"
#         #print(new_indexes, fields)
#         for f in fields:
#             for n in indexes:
#                 if n not in new_indexes:
#                     getNewFields([n], f, relations, depth + 1, max_depth)

# visited_fields = set({"Fname"})
# relations = {}


# def itrate(copyofvisited):
#     for f in copyofvisited:
#         getNewFields(req.get("index_names"), f, relations)
#         for index in req.get("index_names"):
#             newfileds = relations.get(index)
#             for n in newfileds:
#                 visited_fields.add(n)
#     return

# start = len(visited_fields)
# itrate(visited_fields.copy())
# end = len(visited_fields)
# if start != end:
#     itrate(visited_fields.copy())

# for l in visited_fields:
#     getNewFields(req.get("index_names"), l, relations)

# database = relations

# for d in database:
#     for s in database.get(d).keys():
#         print(d,s)
########################################################################################################
# def chain_search_steps(steps, value, visited=None, current_result=None, final_results=None):
#     if visited is None:
#         visited = set()
#     if current_result is None:
#         current_result = {}
#     if final_results is None:
#         final_results = []

#     if not steps:
#         final_results.append(current_result)
#         return final_results

#     index_name, field_name = steps[0]
#     result = databaseConnection.get_documents2(index=index_name, feild=field_name, val=value)
#     hits = result.get("hits", {}).get("hits", [])

#     for doc in hits:
#         doc_id = (index_name, doc["_id"])
#         if doc_id in visited:
#             continue
#         visited.add(doc_id)

#         # اطلاعات فعلی را اضافه کن
#         new_result = current_result.copy()
#         new_result.update(doc["_source"])

#         # تعیین مقدار مرحله بعدی
#         if len(steps) > 1:
#             next_index, next_field = steps[1]

#             # برای مرحله بعد، مقدار مناسب را از doc["_source"] می‌گیریم
#             if next_field in doc["_source"]:
#                 next_value = doc["_source"][next_field]
#             elif "city" in doc["_source"]:
#                 next_value = doc["_source"]["city"]
#             elif "Lname" in doc["_source"]:
#                 next_value = doc["_source"]["Lname"]
#             else:
#                 next_value = None

#             if next_value is not None:
#                 chain_search_steps(steps[1:], next_value, visited, new_result, final_results)
#         else:
#             # آخرین مرحله
#             final_results.append(new_result)

#     return final_results


# search_steps = [
#     ("a", "Fname"),
#     ("b", "Lname"),
#     ("c", "Lname"),  # یا city بسته به نیاز
#     ("d", "city")    # برای گرفتن city_code
# ]

# results = chain_search_steps(search_steps, "i")

# for r in results:
#     print(r)


#print("Visited:", visited_fields)

# def get_new_fields(indexes, start_field):
#     visited_fields = set()   # جلوگیری از بررسی دوباره یک فیلد
#     visited_indices = set()  # جلوگیری از بررسی دوباره یک ایندکس
#     queue = deque([(indexes, start_field)])  # صف کارها (ایندکس‌ها + فیلد فعلی)

#     while queue:
#         current_indexes, field = queue.popleft()

#         # اگه این فیلد رو قبلاً بررسی کردیم، ادامه نده
#         if field in visited_fields:
#             continue
#         visited_fields.add(field)

#         for idx in current_indexes:
#             # گرفتن ایندکس‌هایی که این فیلد رو دارن + فیلدهای جدید
#             indices_with_field, new_fields_found = databaseConnection.get_fileds_of_index(index=idx, field_name=field)

#             if indices_with_field:
#                 print(f"Index: {indices_with_field} -> New Fields: {new_fields_found}")
#                 visited_indices.update(indices_with_field)

#                 # فیلدهای جدید رو به صف اضافه کن
#                 for nf in new_fields_found:
#                     if nf not in visited_fields:
#                         queue.append((indexes, nf))
#     print(visited_indices)
#     print(visited_fields)
# # استفاده
# get_new_fields(req.get("index_names"), "Fname")



# visited_fields = set()
# indexwithfileds = dict()
# def get_new_fields(indexes, field):
#     if field in visited_fields:
#         return
#     visited_fields.add(field)
#     for idx in indexes:
#         indices_with_field, new_fields_found = databaseConnection.get_fileds_of_index(index=idx, field_name=field)
#         if indices_with_field:
#      #       print(indices_with_field, new_fields_found)
#             if type(indexwithfileds.get(idx)) != None:
#                 old = list(indexwithfileds.get(idx))
#                 old.append(new_fields_found)
#                 indexwithfileds.update({idx:old})
#                 for nf in new_fields_found:
#                     get_new_fields(indexes, nf)


# get_new_fields(req.get("index_names"), "Fname")
# print(indexwithfileds)


oldfeild = "Fname"
resultFname = databaseConnection.get_documents2(index="a",feild=oldfeild,val="i")
hitsFname = resultFname.get("hits", {}).get("hits", [])
for k in hitsFname:
    newfild = k["_source"].keys()
    for n in newfild:
        if n != oldfeild:
            resultLastName = databaseConnection.get_documents3(index="b",feild=n,val=k["_source"].get(n))
            hitsLname = resultLastName.get("hits", {}).get("hits", [])
            if len(hitsLname) == 0:
                resultCLastName = databaseConnection.get_documents3(index="c",feild=n,val=k["_source"].get(n))
                hitsCLname = resultLastName.get("hits", {}).get("hits", [])
                print(hitsCLname)    
            else:
                print(hitsLname)
            oldfeild = n # oldfeild = Lname
            for kl in hitsLname:
                newklfild = kl["_source"].keys() # Lname & city
                for nl in newklfild:
                    if nl != oldfeild:
                        resultCity = databaseConnection.get_documents3(index="c",feild=nl,val=kl["_source"].get(nl))
                        hitsCity = resultCity.get("hits", {}).get("hits", [])
                        for kc in hitsCity:
                            newkcfild = kc["_source"].keys()
                            for ck in newkcfild:
                                if ck != oldfeild:
                                    resultCityCode = databaseConnection.get_documents3(index="d",feild=ck,val=kc["_source"].get(ck))
                                    hitsCityCode = resultCityCode.get("hits", {}).get("hits", [])
                                    print(kc["_index"],kc["_source"],hitsCityCode)
                                    oldfeild = ck
                resultCityCode2 = databaseConnection.get_documents3(index="d",feild="city",val=kl["_source"].get("city"))
                hitsCityCode2 = resultCityCode2.get("hits", {}).get("hits", [])
                print(k["_index"],k["_source"],kl["_index"],kl["_source"],kc["_index"],kc["_source"],hitsCityCode2)



    # def get_documents2(self, index, feild=None, val=None):
    #     if feild is None:
    #         query = {"query": {"match_all": {}}}
    #     else:
    #         query = {"query": {"regexp": {feild: f"{".*"+val+".*"}"}}}
    
    #     result = self.es.search(index=index, body=query)
    #     return result




