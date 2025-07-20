from datetime import datetime
from dataclasses import dataclass
from utils.Encrypt import encrytion

@dataclass
class User:
    name: str
    email: str
    phoneumber: str
    is_admin: bool
    created_at = datetime.utcnow()

class UserRegister(User):
    password: str
    def encrytion_password(self):
        self.password = encrytion(self.password)
        return self.password