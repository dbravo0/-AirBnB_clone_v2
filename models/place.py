#!/usr/bin/python3
"""This is the place class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, ForeignKey, String, Float, Table
from sqlalchemy.orm import relationship, backref
from os import environ
from models.review import Review
import models

type_storage = environ.get('HBNB_TYPE_STORAGE')

place_amenity = Table("place_amenity", Base.metadata,
                      Column("place_id", String(60),
                             ForeignKey("places.id"),
                             primary_key=True,
                             nullable=False),
                      Column("amenity_id", String(60),
                             ForeignKey("amenities.id"),
                             primary_key=True,
                             nullable=False))


class Place(BaseModel, Base):
    """This is the class for Place
    Attributes:
        city_id: city id
        user_id: user id
        name: name input
        description: string of description
        number_rooms: number of room in int
        number_bathrooms: number of bathrooms in int
        max_guest: maximum guest in int
        price_by_night:: pice for a staying in int
        latitude: latitude in flaot
        longitude: longitude in float
        amenity_ids: list of Amenity ids
    """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []

    if (type_storage == "db"):
        reviews = relationship('Review', backref="place",
                               cascade="all, delete, delete-orphan")
        amenities = relationship("Amenity", secondary=place_amenity,
                                 backref="place_amenities", viewonly=False)
    else:
        @property
        def reviews(self):
            """
                Return Instances Reviews
            """
            all_review = models.storage.all(Review)
            review_place = []
            for review_ins in all_review.values():
                if (review_ins.place_id == self.id):
                    review_place.append(review_ins)
            return (review_place)

        @property
        def amenities(self):
            """ Amenity Getter """
            all_amenities = models.storage.all(models.Amenity)
            place_amenities = []
            for amenity_ins in all_amenities.values():
                if (amenity_ins.place_id == self.id):
                    place_amenities.append(amenity_ins)

            return (place_amenities)

        @amenities.setter
        def amenities(self, amenity_ins):
            """
                Amenity Setter
            """
            if isinstance(amenity_ins, models.Amenity):
                self.amenities.append(amenity_ins.id)
