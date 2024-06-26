#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.ext.declarative import declarative_base
from os import getenv
from sqlalchemy import Column, Table, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
import models


place_amenity = Table(
        "place_amenity",
        Base.metadata,
        Column(
            "place_id",
            String(60),
            ForeignKey("places.id"),
            primary_key=True,
            nullable=False
            ),
        Column(
            "amenity_id",
            String(60),
            ForeignKey("amenities.id"),
            primary_key=True,
            nullable=False
            )
        )


class Place(BaseModel, Base):
    """ Place model """
    __tablename__ = "places"
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

    storage_type = getenv("HBNB_TYPE_STORAGE")

    if storage_type == "db":
        reviews = relationship(
                "Review",
                cascade='all, delete, delete-orphan',
                backref="place"
                )

        amenities = relationship(
                "Amenity",
                secondary=place_amenity,
                viewonly=False,
                back_populates="place_amenities"
                )
    else:
        @property
        def reviews(self):
            """ list of reviews.id """
            data = models.storage.all()
            review_list = []
            matched = []
            for key in data:
                review = key.replace('.', ' ')
                review = shlex.split(review)
                if (review[0] == 'Review'):
                    review_list.append(data[key])
            for item in review_list:
                if (item.place_id == self.id):
                    matched.append(item)
            return matched

        @property
        def amenities(self):
            """ list of amenity.id """
            return self.amenity_ids

        @amenities.setter
        def amenities(self, obj=None):
            """ add amenity.id to attributes """
            if type(obj) is Amenity and obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)
