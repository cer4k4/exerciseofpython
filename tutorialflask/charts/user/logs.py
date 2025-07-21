from flask_restful import Resource

class HistoryLogs(Resource):
    def post(self):
            return {
            "name":"HistoryLogs"
        }