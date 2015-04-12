__author__ = 'david'

from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel


class BookingCondition(polymodel.PolyModel):
    pass


class FlightBookingCondition(BookingCondition):
    """
    And relation between all non None values.
    """
    origin = ndb.StringProperty(required=True)
    destination = ndb.StringProperty(required=True)
    booking_start_date = ndb.DateTimeProperty(required=True)
    booking_end_date = ndb.DateTimeProperty(required=True)
    min_duration = ndb.IntegerProperty(required=True)
    max_duration = ndb.IntegerProperty(required=True)
    number_of_connections = ndb.IntegerProperty(required=True, default=0)
    exclude_companies = ndb.StringProperty(repeated=True)
    max_flight_duration = ndb.IntegerProperty()
    number_of_adult_tickets = ndb.IntegerProperty(required=True, default=1)
    max_price = ndb.IntegerProperty(required=True)


class HotelBookingCondition(BookingCondition):
    """
    Not supported yet but here for design\architecture reasons.
    """
    pass


class User(ndb.Model):
    email = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True)
    address = ndb.StringProperty(required=True)


class Recipe(ndb.Model):
    user = ndb.KeyProperty(User, required=True)
    title = ndb.StringProperty()
    description = ndb.StringProperty()
    booking_condition = ndb.LocalStructuredProperty(BookingCondition, required=True)
    enabled = ndb.BooleanProperty(required=True, default=True)
    enabled_at = ndb.DateTimeProperty()
    created_at = ndb.DateTimeProperty(auto_now_add=True)
    is_booked = ndb.BooleanProperty(required=True, default=False)


class BookingInfo(polymodel.PolyModel):
    user = ndb.KeyProperty(User, required=True)


class FlightBookingInfo(BookingInfo):
    price = ndb.FloatProperty(required=True)
    number_of_adult_tickets = ndb.IntegerProperty(required=True)
    itineraries = ndb.JsonProperty(required=True)
    origin = ndb.StringProperty(required=True)
    destination = ndb.StringProperty(required=True)
    pnr = ndb.StringProperty()


class BookingRequest(ndb.Model):
    recipe = ndb.KeyProperty(Recipe, required=True)
    user = ndb.KeyProperty(User, required=True)
    booking_infos = ndb.LocalStructuredProperty(BookingInfo, repeated=True)
    is_booked = ndb.BooleanProperty(required=True, default=False)

    @classmethod
    def calculate_id(cls, user_key, recipe_key):
        return "{0}::{1}".format(user_key.id(), recipe_key.id())
