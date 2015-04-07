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
    # If the duration is None, it means the trip starts at booking_start_date and ends at booking_end_date.
    duration = ndb.IntegerProperty()
    number_of_connections = ndb.IntegerProperty()
    exclude_companies = ndb.StringProperty(repeated=True)
    max_flight_duration = ndb.IntegerProperty()
    number_of_adult_tickets = ndb.IntegerProperty()
    max_price = ndb.IntegerProperty(required=True)
    travel_class = ndb.StringProperty()


class HotelBookingCondition(BookingCondition):
    """
    Not supported yet but here for design\architecture reasons.
    """
    pass


class User(ndb.Model):
    # TODO: implement.
    pass


class Recipe(ndb.Model):
    user = ndb.KeyProperty(User, required=True)
    title = ndb.StringProperty()
    description = ndb.StringProperty()
    booking_condition = ndb.LocalStructuredProperty(required=True)
    enabled = ndb.BooleanProperty(required=True, default=False)
    enabled_at = ndb.DateTimeProperty()
    created_at = ndb.DateTimeProperty(auto_now_add=True)
    is_booked = ndb.BooleanProperty(required=True, default=False)


class BookingInfo(polymodel.PolyModel):
    user = ndb.KeyProperty(User, required=True)


class FlightBookingInfo(BookingInfo):
    # TODO: add properties required for booking a flight.
    pass


class BookingRequest(ndb.Model):
    user = ndb.KeyProperty(User, required=True)
    booking_infos = ndb.KeyProperty(BookingInfo, repeated=True)
    is_booked = ndb.BooleanProperty(required=True, default=False)
