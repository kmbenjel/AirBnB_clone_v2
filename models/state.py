#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.ext.declarative import declarative_base
import models
from models.city import City
import shlex
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship(
            "City",
            cascade='all, delete, delete-orphan',
            backref="state"
            )

    @property
    def cities(self):
        """
        Cities
        """
        data = models.storage.all()
        cities_list = []
        matched = []
        for key in cities_list:
            the_city = key.replace('.', ' ')
            the_city = shlex.split(the_city)
            if the_city[0] == 'City':
                cities_list.append(data[key])
        for item in cities_list:
            if item.state_id == self.id:
                matched.append(item)
        return matched
