#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import shlex


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self):
        """Returns a dictionary of models currently in storage"""
        new_dict = {}
        if cls:
            for k in self.__objects:
                item = k.replace('.', ' ')
                item = shlex.split(item)

                if item[0] == cls.__name__:
                    new_dict[k] = self.__objects[k]
            return new_dict
        else:
            return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        if obj:
            i_name = type(obj).__name__
            i_id = obj.id
            k = "{}.{}".format(i_name, i_id)
            self.__objects[k] = obj

    def save(self):
        """Saves storage dictionary to file"""
        dic = {}
        for k, v in self.__objects.items():
            dic[k] = v.to_dict()

        with open(self.__file_path, 'w', encoding="UTF-8") as fichier:
            json.dump(dic, fichier)

    def reload(self):
        """Loads storage dictionary from file"""
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as fichier:
                for k, v in (json.load(fichier)).items():
                    v = eval(value["__class__"])(**v)
                    self.__objects[k] = v
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete an instance"""
        if obj:
            i_name = type(obj).__name__
            i_id = obj.id
            key = "{}.{}".format(i_name, i_id)
            del self.__objects[key]

    def close(self):
        """ reload """
        self.reload()
