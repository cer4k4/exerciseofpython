from time import time
# Cerberus provides powerful yet simple and lightweight data validation functionality out of the box and is designed to be easily extensible, allowing for custom validation.


# Generate cerberus schema
class InputSchema:
    @staticmethod
    def register_user():
        userregistermodel = {
            "name": {'type':'string','required': True,'max': 120},
            "phone_number": {'type':'string','required': True,'regex': r'^09\d{9}$'},
            "age": {'type':'integer'},
            "password": {'type':'string','required': True},
        }
        return userregistermodel
    
    @staticmethod
    def get_user_or_delete_user():
        uuid = {"uuid":{'type':'string','required': True,'regex': r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$'}}
        return uuid
    
    @staticmethod
    def get_users_with_filter():
        pagination = {
            "value":{'required': True},
            "field":{'type':'string','required': True,'allowed': ['phone_number', 'name', 'age','']},
            "size":{'type':'integer','default':50,'required': True},
            "page":{'type':'integer','default':1,'required': True}            
        }
        return pagination    
    