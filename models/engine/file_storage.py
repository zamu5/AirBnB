#!/usr/bin/python3
import json
from ..base_model import BaseModel
from ..user import User
from ..place import Place
from ..state import State
from ..city import City
from ..amenity import Amenity
from ..review import Review

class FileStorage():
    __file_path = "file.json"
    __objects = {}

    def all(self):
        return self.__objects

    def new(self, obj):
        self.__objects["{}.{}".format(obj.__class__.__name__, obj.id)] = obj

    def save(self):
        new_obj = {}
        for obj in self.__objects:
            new_obj[obj] = self.__objects[obj].to_dict()
        with open(self.__file_path, 'w') as f:
            f.write(json.dumps(new_obj))

    def reload(self):
        try:
            with open(self.__file_path) as f:
                json_obj = json.loads(f.read())
                for obj in json_obj:
                    obj_c = obj.split('.')
                    self.__objects[obj] = eval(obj_c[0])(**(json_obj[obj]))
        except:
            pass
