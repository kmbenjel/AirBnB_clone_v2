#!/usr/bin/python3
"""DBStorage module"""
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import (create_engine)
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """ DBStorage env setup"""
    __engine = None
    __session = None

    def __init__(self):
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        db = getenv("HBNB_MYSQL_DB")
        host = getenv("HBNB_MYSQL_HOST")
        env = getenv("HBNB_ENV")

        config = "mysql+mysqldb://{}:{}@{}/{}".format(user, passwd, host, db)

        self.__engine = create_engine(config, pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Get all objects """
        data = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            req = self.__session.query(cls)
            for item in req:
                i_name = type(item).__name__
                i_id = item.id
                key = "{}.{}".format(i_name, i_id)
                data[key] = item
        else:
            table_list = [State, City, User, Place, Review, Amenity]
            for item in table_list:
                req = self.__session.query(item)
                for i in req:
                    i_name = type(i).__name__
                    i_id = i.id
                    key = "{}.{}".format(i_name, i_id)
                    data[key] = i
        return data

    def new(self, obj):
        """post data in the table"""
        self.__session.add(obj)

    def save(self):
        """save"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete data in the table"""
        if obj:
            self.session.delete(obj)

    def reload(self):
        """ Reload DBStorage """
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session)
        self.__session = Session()

    def close(self):
        """ Leave DBStorage """
        self.__session.close()
