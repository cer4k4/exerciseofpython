#import copy
from flask import request, jsonify
from flask_restful import Resource
from tools.elastic import ConnectionElasticsearch
from tools.cerberus_validator import schema_validator_cerberus
from tools.inputSchema import InputSchema
import uuid
from datetime import datetime
elsmanager = ConnectionElasticsearch()
userschema = "users"
logschema = "users-logs"
errors = {
    "phone_registered": "another user registered with this phone number",
    "uuid": "uuid is not valid"
}

class RegisterUser(Resource):
    def post(self):
        user_id = str(uuid.uuid4())
        usermodel = InputSchema()
        raw_data = request.get_json()
        resultvalidate = schema_validator_cerberus(raw_data,usermodel.register_user())
        if resultvalidate.get("errors"):
            return {
                "error": resultvalidate.get("errors")
            }
        else:
            user = elsmanager.get_data_by_filter(index=userschema, filter="phone_number",val=raw_data["phone_number"])
            if uuidvalidation(user,"_id"):
                return {
                    "error": errors["phone_registered"]
                }
            user_doc = {
                "name": raw_data["name"],
                "phone_number": raw_data["phone_number"],
                "age": raw_data["age"],
                "password":raw_data["password"],
                "registered_at": datetime.now().isoformat(),
                "status": True
            }
            result = elsmanager.insert_document(index=userschema, doc_id=user_id, body=user_doc)
            return {
                "uuid": result.get("_id")
            }
    
class GetUser(Resource):
    def get(self):
        uuid = request.args.get('uuid')
        usermodel = InputSchema()
        resultvalidate = schema_validator_cerberus({"uuid":uuid},usermodel.get_user_or_delete_user())
        if resultvalidate.get("errors"):
            return {
                "error": resultvalidate.get("errors")
            }
        else:
            user = elsmanager.get_data_by_filter(index=userschema, filter="_id",val=uuid)
            return {
                "user": user["hits"]["hits"][0]["_source"]
            }

class GetUsers(Resource):
    def post(self):
        filterbody = request.get_json()
        usermodel = InputSchema()
        resultvalidate = schema_validator_cerberus(filterbody,usermodel.get_users_with_filter())
        if resultvalidate.get("errors"):
            return {
                "error": resultvalidate.get("errors")
            }
        else:
            if filterbody.get("filter",True):
                users = elsmanager.get_documents(index=userschema,feild=filterbody["field"],val=filterbody["value"],page=filterbody["page"],size=filterbody["size"])
                return {
                    "users": users
                }
            elif filterbody.get("filter",False):
                users = elsmanager.get_documents(index=userschema,feild=None,val=None,page=filterbody["page"],size=filterbody["size"])
                return {
                    "users": users
                }
            else:
                return {
                    "users": "unknow"
                }


class UpdateUser(Resource):
    def put(self):
        inputbody = request.get_json()
        uuid = request.args.get('uuid')
        userdb = elsmanager.get_data_by_filter(index=userschema,filter="_id",val=uuid)
        # check exist user
        if uuidvalidation(userdb,"_id"):
            # check duplicate phone number
            if not validationuserfields(userdb,"_source","phone_number",inputbody["phone_number"]):
                anotheruserdb = elsmanager.get_data_by_filter(index=userschema,filter="phone_number",val=inputbody["phone_number"])
                if uuidvalidation(anotheruserdb,"_id"):
                    if giveuuid(anotheruserdb) != giveuuid(userdb):
                        return {
                            "error": errors["phone_registered"]
                        }
            user_doc = {
                "name": inputbody["name"],
                "phone_number": inputbody["phone_number"],
                "age": inputbody["age"],
                "password":inputbody["password"],
                "updated_at": datetime.now().isoformat(),
            }
            result = elsmanager.update_document(index=userschema, id=inputbody["uuid"], doc=user_doc)        
            return {
                "status": result["result"]
            }
        return {
               "error": errors["uuid"]
        }
    
class DeleteUser(Resource):
    def delete(self):
        uuid = request.args.get('uuid')
        usermodel = InputSchema()
        resultvalidate = schema_validator_cerberus({"uuid":uuid},usermodel.get_user_or_delete_user())
        if resultvalidate.get("errors"):
            return {
                "error": resultvalidate.get("errors")
            }
        else:
            result = elsmanager.delete_document(index=userschema, id=uuid)
            return {
                "status": result
            }

def uuidvalidation(user,key):
    for g in user["hits"]["hits"]:
        if g[key]:
                return True
    return False

def validationuserfields(user,key,subkey,phone):
    for g in user["hits"]["hits"]:
        if g[key][subkey]:
            if g[key][subkey] == phone:
                return True
    return False

def giveuuid(user):
    for g in user["hits"]["hits"]:
        if g["_id"]:
            return g["_id"]
    return ""
