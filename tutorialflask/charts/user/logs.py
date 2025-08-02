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
        
        try:
            mindate = datetime.fromisoformat(raw_data["min_date"])
            maxdate = datetime.fromisoformat(raw_data["max_date"])
        except ValueError as e:
            return {
                "error": f"Invalid date format: {str(e)}"
            }
        
        result = elsmanager.count_of_index("users-logs","login_at",int(mindate.timestamp() * 1000),int(maxdate.timestamp() * 1000))
        dates = []
        counts = []
        for r in result:
            # Use key_as_string if available, otherwise format the timestamp
            date_str = r.get("key_as_string")
            if date_str is None:
                timestamp = r.get("key") / 1000
                date_obj = datetime.fromtimestamp(timestamp)
                date_str = date_obj.strftime("%Y-%m-%d")
            
            dates.append(date_str)
            counts.append(r.get("doc_count", 0))
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
                    print()
                    user_doc = {
                        "uuid": g["_id"],
                        "login_at": datetime.now().timestamp() * 1000
                    }
                    elsmanager.insert_document(index=logschema, doc_id=user_id, body=user_doc)
                    return {"status":"successful"}
                else:
                    return {"status":"password invalid"}
    

def validatepassword(password,dbpassword):
    if password != dbpassword:
        return False
    return True
