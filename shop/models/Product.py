import datetime
from bson import ObjectId

class Product:
    def __init__(self,title,price,stock,category):
        self._id = ObjectId(_id) if _id else ObjectId()
        self.title = title
        self.price = price
        self.stock = stock
        self.category = category
        self.created_at = datetime.now()