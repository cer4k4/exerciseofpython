from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from config.configer import Configer
from charts.user.logs import HistoryLogs,UserLogin
from charts.user.user import *

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
register_user = myConf.get("user", "register_user")
update_user = myConf.get("user","update_user")
users = myConf.get("user","get_list_users")
user = myConf.get("user","get_user")
delete_user = myConf.get("user","delete_user")
login = myConf.get("user", "login")
chart  = myConf.get("chart_name", "users_logs")

# User
api.add_resource(RegisterUser, register_user)
api.add_resource(GetUsers,users)
api.add_resource(GetUser,user)
api.add_resource(UpdateUser, update_user)
api.add_resource(DeleteUser, delete_user)

# Login
api.add_resource(UserLogin, login)
api.add_resource(HistoryLogs, chart)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)