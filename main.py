
from elasticsearch import Elasticsearch

req = {
    "index_names":["A","B","C","D"],
    "fname": "i",
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
            query = {"query": {"match": {feild: val}}}
    
        result = self.es.search(index=index, body=query)
        print(result)
        return result

            
databaseConnection = ConnectionElasticsearch()

databaseConnection.get_documents2(index="a",feild="Lname",val="Karimi")