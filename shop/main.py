from db.Mongo import UserRepository
from models.User import UserRegister
from utils.Decryption import decrytion

user = UserRegister("ali","cer4k4@gmail.com","09981012169",False)
user.password = "asdasd"
user.encrytion_password()
print(UserRepository.save_user(user))
for counter in UserRepository.get_users():
    print(decrytion((counter["hashed_password"])))

