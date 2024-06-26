#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
import models
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""

    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=(datetime.utcnow()))
    updated_at = Column(DateTime, nullable=False, default=(datetime.utcnow()))

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""

        if kwargs:
            for k, v in kwargs.items():
                if k == "created_at" or k == "updated_at":
                    v = datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%f")
                if k != "__class__":
                    setattr(self, k, v)
            if "id" not in kwargs:
                self.id = str(uuid.uuid4())
            if "created_at" not in kwargs:
                self.created_at = datetime.now()
            if "updated_at" not in kwargs:
                self.updated_at = datetime.now()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()

    def __str__(self):
        """Returns a string representation of the instance"""
        i_name = type(self).__name__
        i_id = self.id
        i_dict = self.__dict__
        return '[{}] ({}) {}'.format(i_name, i_id, i_dict)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def delete(self):
        """Delete an instance"""
        models.storage.delete(self)

    def to_dict(self):
        """Convert instance into dict format"""
        dict_format = dict(self.__dict__)

        dict_format["__class__"] = str(type(self).__name__)
        dict_format["created_at"] = self.created_at.isoformat()
        dict_format["updated_at"] = self.updated_at.isoformat()
        if '_sa_instance_state' in dict_format.keys():
            del dict_format['_sa_instance_state']

        return dict_format

    def __repr__(self):
        """ String representation of an instance"""
        return self.__str__()
