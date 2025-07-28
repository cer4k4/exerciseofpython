import urllib3
from config import configer
#from datetime import datetime, timedelta
from elasticsearch import Elasticsearch,ElasticsearchWarning
import warnings

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
            self.es = Elasticsearch(f"http://{es_host_ip}:{es_port}") 

        #   self.es = Elasticsearch([{'host': myConfig.get("es", "host_ip"), 'port': int(es_port)}],http_auth=(es_user,es_pass))
        #   self.es = Elasticsearch(es_connection, use_ssl=False, ca_certs=False, http_auth=(
        #         es_user, es_pass), verify_certs=False)
            self.request_timeout = int(myConfig.get("es", "request_timeout"))
            self.current_index = None

    def get_data_by_filter(self, index, filter,val):
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
    
    def insert_document(self, index, doc_id,body):
        try:
            result = self.es.index(index=index, id=doc_id, body=body)
            return result
        except Exception as e:
            print(f"Elasticsearch index error: {e}")
            return None
        
    def count_of_index(self,index,feild,mindate,maxdate):
            query = {
                "range": {
                    feild: {
                        "gte":mindate,
                        "lte":maxdate
                    }
                }
            }
            result = self.es.count(index=index,query=query)
            return result
        
    def update_document(self,index,id,doc):
        return self.es.index(index=index,id=id,body=doc)
    
    def get_documnets(self,index):
        pass
    
