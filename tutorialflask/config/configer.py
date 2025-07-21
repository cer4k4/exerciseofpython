import configparser
import json


class Configer:
    """
    configer class to get configs from .ini file
    """
    def __init__(self):
        self.parser = configparser.ConfigParser()
        self.parser.read('config/config.ini', encoding='utf-8')
        
    def get(self, *args, type="str"):
        try:
            
            self.parser.sections()
            if type == "int":
                return self.parser.getint(*args)

            if type == "str":
                return self.parser.get(*args)

            if type == "float":
                return self.parser.getfloat(*args)

            if type == "boolean":
                return self.parser.getboolean(*args)

            if type == "list":
                return json.loads(self.parser.get(*args))
            else:
                print(f"you entered wrong value:{type} to type. please enter these value: int | str | float | boolean")

        except Exception as e:
            print("configer.py --> def get_config -->", e, ",args=>", *args)
