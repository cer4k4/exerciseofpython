from flask import request, jsonify
from flask_restful import Resource
from tools.elastic import ConnectionElasticsearch
from datetime import datetime
import uuid

logschema = "users-logs"
userschema = "users"
elsmanager = ConnectionElasticsearch()
class HistoryLogs(Resource):
    def post(self):
        raw_data = request.get_json()
        mindate = raw_data["mindate"]
        maxdate = raw_data["maxdate"]
        result = elsmanager.count_of_index("users-logs","login_at",mindate,maxdate)
        return {
            "count_of_logs": result["count"]
        }
    
class UserLogin(Resource):
    def post(self):
        raw_data = request.get_json()
        user_id = str(uuid.uuid4())
        getUserFromDB = elsmanager.get_data_by_filter(userschema,"phone_number",raw_data["phone_number"])
        for g in getUserFromDB["hits"]["hits"]:
            if g["_source"]:
                if validatepassword(raw_data["password"],g["_source"]["password"]):
                    user_doc = {
                        "uuid": g["_source"]["uuid"],
                        "login_at": datetime.now().isoformat()
                    }
                    elsmanager.insert_document(index=logschema, doc_id=user_id, body=user_doc)
                    return {"status":"successful"}
                else:
                    return {"status":"password invalid"}
    

def validatepassword(password,dbpassword):
    if password != dbpassword:
        return False
    return True
