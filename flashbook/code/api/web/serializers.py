from datetime import datetime
from shared.models import Recipe, FlightBookingCondition

__author__ = 'david'

DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:%S.%f'
DATETIME_FORMAT = '%sT%sZ' % (DATE_FORMAT, TIME_FORMAT)


class RecipeSerializer(object):
    def serialize(self, recipe):
        serialized_recipe = dict(
            id=recipe.key.id(),
            enabled=recipe.enabled,
            booking_condition=self.__serialize_booking_condition(recipe.booking_condition),
            created_at=recipe.created_at.strftime(DATETIME_FORMAT),
            is_booked=recipe.is_booked,
        )

        if recipe.title is not None:
            serialized_recipe['title'] = recipe.title

        if recipe.description is not None:
            serialized_recipe['description'] = recipe.description

        if recipe.enabled_at is not None:
            serialized_recipe['enabled_at'] = recipe.enabled_at.strftime(DATETIME_FORMAT)

        return serialized_recipe

    def deserialize_new_recipe(self, serialized_recipe):
        recipe = Recipe(booking_condition=self.__deserialize_booking_condition(serialized_recipe['booking_condition']))

        if 'title' in serialized_recipe:
            recipe.title = serialized_recipe['title']

        if 'description' in serialized_recipe:
            recipe.description = serialized_recipe['description']

        return recipe

    def __serialize_booking_condition(self, booking_condition):
        return BookingConditionSerializerFactory.create(booking_condition).serialize(booking_condition)

    def __deserialize_booking_condition(self, serialized_booking_condition):
        return BookingConditionDeserializerFactory.create(serialized_booking_condition['type']).deserialize(
            serialized_booking_condition)


class BookingConditionSerializerFactory(object):
    @classmethod
    def create(cls, booking_condition):
        if isinstance(booking_condition, FlightBookingCondition):
            return FlightBookingConditionSerializer()
        else:
            raise AttributeError("Unsupported booking condition type")


class BookingConditionDeserializerFactory(object):
    @classmethod
    def create(cls, booking_condition_type):
        if booking_condition_type == 'flight':
            return FlightBookingConditionSerializer()
        else:
            raise AttributeError("Unsupported booking condition type")


class FlightBookingConditionSerializer(object):
    def serialize(self, flight_booking_condition):
        serialized_flight_booking_condition = dict(
            origin=flight_booking_condition.origin,
            destination=flight_booking_condition.destination,
            booking_start_date=flight_booking_condition.booking_start_date.strftime(DATETIME_FORMAT),
            booking_end_date=flight_booking_condition.booking_end_date.strftime(DATETIME_FORMAT),
            exclude_companies=flight_booking_condition.exclude_companies,
            max_price=flight_booking_condition.max_price
        )

        if flight_booking_condition.duration is not None:
            serialized_flight_booking_condition['duration'] = flight_booking_condition.duration

        if flight_booking_condition.number_of_connections is not None:
            serialized_flight_booking_condition[
                'number_of_connections'] = flight_booking_condition.number_of_connections

        if flight_booking_condition.duration is not None:
            serialized_flight_booking_condition['max_flight_duration'] = flight_booking_condition.max_flight_duration

        if flight_booking_condition.duration is not None:
            serialized_flight_booking_condition[
                'number_of_adult_tickets'] = flight_booking_condition.number_of_adult_tickets

        return serialized_flight_booking_condition

    def deserialize(self, serialized_flight_booking_condition):
        flight_booking_condition = FlightBookingCondition(origin=serialized_flight_booking_condition['origin'],
                                                          destination=serialized_flight_booking_condition[
                                                              'destination'],
                                                          booking_start_date=datetime.strptime(
                                                              serialized_flight_booking_condition['booking_start_date'],
                                                              DATETIME_FORMAT),
                                                          booking_end_date=datetime.strptime(
                                                              serialized_flight_booking_condition['booking_end_date'],
                                                              DATETIME_FORMAT),
                                                          max_price=serialized_flight_booking_condition['max_price'])

        if 'duration' in serialized_flight_booking_condition:
            flight_booking_condition.duration = serialized_flight_booking_condition['duration']

        if 'number_of_connections' in serialized_flight_booking_condition:
            flight_booking_condition.number_of_connections = serialized_flight_booking_condition[
                'number_of_connections']

        if 'max_flight_duration' in serialized_flight_booking_condition:
            flight_booking_condition.max_flight_duration = serialized_flight_booking_condition['max_flight_duration']

        if 'number_of_adult_tickets' in serialized_flight_booking_condition:
            flight_booking_condition.number_of_adult_tickets = serialized_flight_booking_condition[
                'number_of_adult_tickets']

        return flight_booking_condition