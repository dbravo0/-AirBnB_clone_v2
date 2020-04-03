
#!/usr/bin/python3
"""This is the place class"""
import models
from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy import MetaData
from sqlalchemy.orm import relationship
from models.city import City
from os import environ

place_amenity = Table("place_amenity", Base.metadata,
                      Column("place_id",
                             String(60),
                             ForeignKey("places.id"),
                             primary_key=True),
                      Column("amenity_id",
                             String(60),
                             ForeignKey("amenities.id"),
                             primary_key=True))


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

    if environ.get('HBNB_TYPE_STORAGE') == "db":
        reviews = relationship('Review', backref="place",
                               cascade="all, delete, delete-orphan")
        amenities = relationship('Amenity', secondary="place_amenity",
                                 viewonly=False)
    else:
        @property
        def reviews(self):
            """ Return the list of the city """
            all_reviews = models.storage.all(Review)
            filter_reviews = []
            for review in all_reviews.values():
                if review.place_id == self.id:
                    filter_reviews.append(review)
            return filter_reviews

        @property
        def amenities(self):
            """ Return list of amenities """
            all_amenities = models.storage.all(Amenity)
            filter_amenities = []
            for amenity in all_amenities.values():
                for place_amenity in self.amenity_ids:
                    if amenity.id == place_amenity:
                        filter_amenities.append(amenity)
            return filter_amenities

        @amenities.setter
        def amenities(self, amenity_obj):
            """ Add Amenity.id to amenity_ids """
            if isinstance(amenity_obj, Amenity):
                self.amenity_ids.append(amenity_obj.id)
