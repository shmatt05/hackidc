from shared.models import FlightBookingCondition

__author__ = 'david'


class BookingConditionExaminerFactory(object):
    @classmethod
    def create(cls, booking_condition):
        if isinstance(booking_condition, FlightBookingCondition):
            return FlightBookingConditionExaminer(booking_condition)


class BookingConditionExaminer(object):
    def __init__(self, booking_condition):
        self._booking_condition = booking_condition

    def examine(self):
        """
        Abstract. Examines the booking condition according to its type.
        :return: A list of BookingInfo objects.
        """
        raise NotImplementedError('This is an abstract method.')


class FlightBookingConditionExaminer(BookingConditionExaminer):
    def examine(self):
        # TODO: implement
        return False