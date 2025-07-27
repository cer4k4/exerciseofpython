from flask import request, jsonify
from flask_restful import Resource
from tools.elastic import ConnectionElasticsearch

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