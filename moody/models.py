"""Database models and relationships are defined here"""
from sqlalchemy import Table, Column, Integer, Float, ARRAY, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql import JSONB
import bcrypt

from moody.db import session


Base = declarative_base()
Base.query = session.query_property()


# This defines our association table for associating MoodEvents with Places
mood_events_places = Table(
    'mood_events_places',
    Base.metadata,
    Column('mood_event_id', Integer, ForeignKey('mood_events.id')),
    Column('place_id', Integer, ForeignKey('places.id'))
)


class MoodEvent(Base):
    """
    MoodEvent model

    The main goal is to persist the emotion (sentiment) captured by the client and make sure it's associated with the user.
    We'll also want to capture the WHEN and WHERE of this sentiment so that we can provide useful insights using this data.

    We want the eventual capability to aggregate and attribute MoodEvents to locations/landmarks that are meaningful to users, not just latitude/longitude coordinates.
    Thus, we we want to store human-readable characteristics about the overall *vicinity* of the location along with the exact position.
    To get this "locational context", we will need to query information about the area surrounding the coordinates.
    Then, we can disseminate this context into a discrete list of "Places" associated with the MoodEvent.
    We can require the conversion of coordinates to places to occur in multiple possible points in the workflow, namely:
    a) convert coordinates to places on the client-side before it sends mood data to server
    b) convert coordinates to places on the server-side when handling POST request of mood data
    c) convert coordinates to places asynchronously server-side by delegating a worker to do the conversion after a new MoodEvent is inserted to the db

    For this implementation, we'll go with option b), and also pretend we have fast and unrestricted access to the Google Places API.
    """
    __tablename__ = 'mood_events'

    id = Column(Integer, primary_key=True, nullable=False)

    sentiment = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    date_created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    user = relationship('User')

    places = relationship(
        'Place',
        backref='mood_events',
        secondary=mood_events_places
    )

    def __init__(self, sentiment, latitude, longitude, user):
        self.sentiment = sentiment
        self.latitude = latitude
        self.longitude = longitude
        self.user = user

    @classmethod
    def apply_query_params(cls, kwargs):
        """
        Return a MoodEvent query with various parameters applied.
        """
        query = cls.query

        # One application for this method is to create a query for all mood events with a particular sentiment value, e.g
        # query = query.filter(cls.sentiment == kwargs['sentiment'])

        return query


class Place(Base):
    """
    Place model

    We define "Places" to be locations that are meaningful to a user (instead of just longitude/latitude coords).
    "Places" can then be associated with MoodEvents based on their proximity.

    For our implementation, we'll be associating each Places with MoodEvents, where each Place can be associated with multiple MoodEvents and
    each MoodEvent can be associated with multiple Places.

    At the ORM level, the list of MoodEvents associated with a given place will be accessible by `place.mood_events`.
    We'll also be able to get the list of places for any given mood event by accessing `mood_event.places`

    For each place, we'll keep track of:
    - unique id
    - name of place
    - latitude of place
    - longitude of place
    - types, or categories, this place falls under (e.g. ["restaurant", "food", "establishment"])
    - additional data to identify location in a "human-readable" way e.g.
        - address
        - city
        - country
        - continent

    It might make sense to put columns like types, city, country, and continent as their own tables if want this data to be normalized
    """
    __tablename__ = 'places'

    id = Column(Integer, primary_key=True, nullable=False)

    name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    types = Column(ARRAY(String), nullable=False)
    # address = Column(String, nullable=False)
    # city = Column(String, nullable=False)
    # country = Column(String, nullable=False)
    # continent = Column(String, nullable=False)

    def __init__(self, name, latitude, longitude, types):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.types = types


class User(Base):
    """User model"""
    __tablename__ = 'users'
    id = Column(Integer, nullable=False, primary_key=True)

    email = Column(String, nullable=False)
    _password = Column('password', String, nullable=False)
    date_created = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    date_updated = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    def __init__(self, email, password):
        self.email = email
        self.password = password

    @hybrid_property
    def password(self):
        """Define password as a property since we want a special setter method"""
        return self._password

    @password.setter
    def password(self, password):
        """Hash the password in a cryptographically secure way. We don't want to persist plain text passwords to the db."""
        self._password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def password_equals(self, password):
        """Return True if User's password matches the given input"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
