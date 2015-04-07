from shared.models import FlightBookingCondition

__author__ = 'david'

DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:%S.%f'
DATETIME_FORMAT = '%sT%sZ' % (DATE_FORMAT, TIME_FORMAT)


class RecipeSerializer(object):
    def serialize(self, recipe):
        return dict(
            id=recipe.key.id(),
            title=recipe.title,
            description=recipe.description,
            enabled=recipe.enabled,
            booking_condition=self.__serialize_booking_condition(recipe.booking_condition),
            enabled_at=recipe.enabled_at.strftime(DATETIME_FORMAT),
            created_at=recipe.created_at.strftime(DATETIME_FORMAT),
            is_booked=recipe.is_booked,
        )

    def __serialize_booking_condition(self, booking_condition):
        return BookingConditionSerializerFactory.create(booking_condition).serialize(booking_condition)


class BookingConditionSerializerFactory(object):
    @classmethod
    def create(cls, booking_condition):
        if isinstance(booking_condition, FlightBookingCondition):
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
            serialized_flight_booking_condition['number_of_connections'] = flight_booking_condition.number_of_connections

        if flight_booking_condition.duration is not None:
            serialized_flight_booking_condition['max_flight_duration'] = flight_booking_condition.max_flight_duration

        if flight_booking_condition.duration is not None:
            serialized_flight_booking_condition['number_of_adult_tickets'] = flight_booking_condition.number_of_adult_tickets

        if flight_booking_condition.travel_class is not None:
            serialized_flight_booking_condition['travel_class'] = flight_booking_condition.travel_class

        return serialized_flight_booking_condition
