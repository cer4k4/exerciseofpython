import pymongo
from models import User
from bson import ObjectId

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["shop"]
userscollection = mydb["users"]


class UserRepository:
    def get_users():
        user = userscollection.find()
        return user
    def get_user_by_id(id):
        user = userscollection.find_one({"_id":ObjectId(id)})
        return user
    def get_user_by_phone_number(phonenumber):
        user = userscollection.find_one({"phone_number":phonenumber})
        return user
    def save_user(user: User.UserRegister):
        result = userscollection.insert_one({"name":user.name,"phone_number":user.phoneumber,"is_admin":user.is_admin,"email":user.email,"hashed_password":user.password,"created_at":user.created_at})
        return result.inserted_id





