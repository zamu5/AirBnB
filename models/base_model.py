#!/usr/bin/python3
from uuid import uuid4
from datetime import datetime
import models

class BaseModel:

    def __init__(self, *args, **kwargs):
        if (kwargs):
            #recretae the values of a instance in base a dictionary
            for k, v in kwargs.items():
                if k != '__class__':
                    if k == "created_at" or k == "updated_at":
                        v = datetime.strptime(v, '%Y-%m-%dT%H:%M:%S.%f')
                    setattr(self, k, v)
        else:
            #create a new instance
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        #print format
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id,
                                     self.__dict__)

    def save(self):
        #update the date
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        #return a dictionary similar to __dict__ but change the format of
        #created_at and updated_at
        ret_dict = {}
        object_dict = self.__dict__
        ret_dict['__class__'] = self.__class__.__name__
        for k, v in object_dict.items():
            if k is "created_at" or k is "updated_at":
                ret_dict[k] = v.isoformat()
            else:
                ret_dict[k] = v
        return ret_dict
