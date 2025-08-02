import urllib3
from config import configer
#from datetime import datetime, timedelta
from elasticsearch import Elasticsearch,ElasticsearchWarning
from elasticsearch.exceptions import NotFoundError
import warnings
from datetime import datetime

warnings.filterwarnings("ignore", category=ElasticsearchWarning)

urllib3.disable_warnings()

class ConnectionElasticsearch(object):
    def __init__(self):
        myConfig = configer.Configer()

        # Get connection parameters from config file
        es_port = myConfig.get("es", "port")
        es_user = myConfig.get("es", "user")
        es_pass = myConfig.get("es", "pass")
        es_connection = myConfig.get("es", "host")
        es_host_ip = myConfig.get("es", "host_ip")

        # ElasticSearch
        if myConfig.get('es', 'host_mode') == "company":
            self.es = Elasticsearch(es_connection, use_ssl=False, ca_certs=False, http_auth=(
                es_user, es_pass), verify_certs=False)
        elif myConfig.get('es', 'host_mode') == "infra_access":
            pass
        elif myConfig.get('es', 'host_mode') == "ip":
            self.es = Elasticsearch(f"http://{es_host_ip}:{es_port}",headers={"Accept": "application/vnd.elasticsearch+json; compatible-with=8"}) 

        #   self.es = Elasticsearch([{'host': myConfig.get("es", "host_ip"), 'port': int(es_port)}],http_auth=(es_user,es_pass))
        #   self.es = Elasticsearch(es_connection, use_ssl=False, ca_certs=False, http_auth=(
        #         es_user, es_pass), verify_certs=False)
            self.request_timeout = int(myConfig.get("es", "request_timeout"))
            self.current_index = None

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
        
    # def count_of_index(self,index,feild,mindate,maxdate):
    #         query = {
    #             "range": {
    #                 feild: {
    #                     "gte":mindate,
    #                     "lte":maxdate
    #                 }
    #             }
    #         }
    #         result = self.es.count(index=index,query=query)
    #         return result
        
    # def count_of_index(self, index, field, mindate, maxdate):
    #     query = {
    #         "query": {
    #             "range": {
    #                 field: {
    #                     "gte": mindate,
    #                     "lte": maxdate
    #                 }
    #             }
    #         },
    #         "aggs": {
    #             "logins_per_day": {
    #                 "date_histogram": {
    #                     "field": field,
    #                     "interval": "day",  # می‌تونی این رو به "hour" یا "week" تغییر بدی
    #                     "format": "yyyy-MM-dd"  # فرمت تاریخ
    #                 }
    #             }
    #         }
    #     }
        
    #     result = self.es.search(index=index, body=query)
        
    #     # استخراج تعداد لاگین‌ها از نتایج آگریگیشن
    #     logins_per_day = result['aggregations']['logins_per_day']['buckets']
        
    #     return logins_per_day

    
    def count_of_index(self, index, field, mindate, maxdate):
        # تبدیل به yyyy-MM-dd برای extended_bounds
        #min_day = datetime.fromisoformat(mindate).strftime('%Y-%m-%d')
        #max_day = datetime.fromisoformat(maxdate).strftime('%Y-%m-%d')

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
            
            
        