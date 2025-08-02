from flask import request, jsonify
from flask_restful import Resource
from tools.elastic import ConnectionElasticsearch
from tools.cerberus_validator import schema_validator_cerberus
from tools.inputSchema import InputSchema
from datetime import datetime
import uuid

logschema = "users-logs"
userschema = "users"
elsmanager = ConnectionElasticsearch()
class HistoryLogs(Resource):
    def post(self):
        raw_data = request.get_json()
        usermodel = InputSchema()
        resultvalidate = schema_validator_cerberus(raw_data,usermodel.history_logs())
        if resultvalidate.get("errors"):
            return {
                "error": resultvalidate.get("errors")
            }
        mindate = raw_data["min_date"]
        maxdate = raw_data["max_date"]
        result = elsmanager.count_of_index("users-logs","login_at",mindate,maxdate)
        dates = []
        counts = []
        for r in result:
            dates.append(r.get("key_as_string"))
            counts.append(r.get("doc_count"))
        return {
            "dates":dates,
            "counts": counts
        }
    
class UserLogin(Resource):
    def post(self):
        raw_data = request.get_json()
        usermodel = InputSchema()
        resultvalidate = schema_validator_cerberus(raw_data,usermodel.login())
        if resultvalidate.get("errors"):
            return {
                "error": resultvalidate.get("errors")
            }
        user_id = str(uuid.uuid4())
        getUserFromDB = elsmanager.get_data_by_filter(userschema,"phone_number",raw_data["phone_number"])
        for g in getUserFromDB["hits"]["hits"]:
            if g["_source"]:
                if validatepassword(raw_data["password"],g["_source"]["password"]):
                    user_doc = {
                        "uuid": g["_id"],
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
