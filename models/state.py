#!/usr/bin/python3
"""This is the state class"""
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column
from sqlalchemy.orm import relationship, backref
from os import environ
from models.city import City
import models

env_storage = environ.get('HBNB_TYPE_STORAGE')


class State(BaseModel, Base):
    """This is the class for State
    Attributes:
        name: input name
    """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    if (env_storage == 'db'):
        cities = relationship("City", backref="state",
                              cascade="all, delete, delete-orphan")
    else:
        @property
        def cities(self):
            """
                Return Instances City
            """
            all_city = models.storage.all(City)
            state_city = []

            for city in all_city.values():
                if (city.state_id == self.id):
                    state_city.append(city)

            return (state_city)
