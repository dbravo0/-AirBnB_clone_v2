#!/usr/bin/python3
""" This db Storage Class """
from os import environ
from models.amenity import Amenity
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session


class DBStorage():
    """ Attributes the Class """
    __engine = None
    __session = None

    def __init__(self):
        """ Inizializate Class """
        usersql = environ.get('HBNB_MYSQL_USER')
        pwdsql = environ.get('HBNB_MYSQL_PWD')
        hostsql = environ.get('HBNB_MYSQL_HOST')
        dbsql = environ.get('HBNB_MYSQL_DB')
        envsql = environ.get('HBNB_ENV')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(usersql, pwdsql,
                                              hostsql, dbsql),
                                      pool_pre_ping=True)

        if (envsql == "test"):
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """
            All in Dict Objects
        """
        session = self.__session
        dicsql = {}

        if (not cls):
            hbn = [User, City, State, Place, Review, Amenity]

        else:
            if (type(cls) == str):
                cls = eval(cls)

            hbn = [cls]

        for x in hbn:
            sql = session.query(x)

            for i in sql:
                key = "{}.{}".format(type(i).__name__, i.id)
                dicsql[key] = i

        return (dicsql)

    def new(self, obj):
        """
            Adding Current Object DataBase
        """
        if (obj):
            self.__session.add(obj)

    def save(self):
        """
            Save Objects
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
            Delete Session
        """
        if (obj):
            self.__session.delete(obj)

    def reload(self):
        """
            The Session Objects
        """
        Base.metadata.create_all(self.__engine)
        sess = sessionmaker(bind=self.__engine, expire_on_commit=False)
        sess_2 = scoped_session(sess)

        self.__session = sess_2()

    def close(self):
        """Thread specific storage"""
        self.__session.close()
