from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from config.configer import Configer
from charts.user.logs import HistoryLogs
from charts.user.user import RegisterUser,UserLogin

myConf = Configer()

app = Flask(__name__, template_folder='swagger-ui/templates')
api = Api(app)

CORS(app)
cors = CORS(app, resource={
    r"/*": {
        "origins": "*"
    }
})

# route
user_register = myConf.get("user", "register_user")
user_login = myConf.get("user", "login")
chart  = myConf.get("chart_name", "users_logs")

api.add_resource(RegisterUser, user_register)
api.add_resource(UserLogin, user_login)
api.add_resource(HistoryLogs, chart)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)