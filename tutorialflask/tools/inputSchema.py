from time import time
#from config.configer import Configer

#myConf = Configer()
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