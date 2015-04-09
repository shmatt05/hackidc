from shared.models import FlightBookingCondition, FlightBookingInfo
from shared.services import FlightSearch
from datetime import datetime
import copy

__author__ = 'david'


class BookingConditionExaminerFactory(object):
    @classmethod
    def create(cls, booking_condition):
        if isinstance(booking_condition, FlightBookingCondition):
            return FlightBookingConditionExaminer(booking_condition)
        else:
            raise AttributeError("Unsupported booking condition type")


class BookingConditionExaminer(object):
    def __init__(self, booking_condition):
        self._booking_condition = booking_condition

    def examine(self):
        """
        Abstract. Examines the booking condition according to its type.
        :return: A list of BookingInfo objects.
        """
        raise NotImplementedError('This is an abstract method.')


FMT = '%Y-%m-%dT%H:%M'
FMD = '%Y-%m-%d'


class FlightBookingConditionExaminer(BookingConditionExaminer):
    def __init__(self, booking_condition):
        super(FlightBookingConditionExaminer, self).__init__(booking_condition)

    def examine(self):
        possible_results = self.__get_possible_results()
        possible_booking_infos = []
        for possible_result in possible_results:
            possible_booking_infos.append(self.__create_booking_info(possible_result))

        return possible_booking_infos

    def __create_booking_info(self, possible_result):
        return FlightBookingInfo(price=float(possible_result['fare']['total_price']),
                                 number_of_adult_tickets=self._booking_condition.number_of_adult_tickets,
                                 itineraries=possible_result['itineraries'],
                                 origin=self._booking_condition.origin,
                                 destination=self._booking_condition.destination)

    def __get_possible_results(self):
        flight = FlightSearch()
        fbc = self._booking_condition
        ret = {}

        departure_start = fbc.booking_start_date if fbc.booking_start_date >= datetime.now() else datetime.now()
        inspiration_data = flight.inspiration_search(fbc.origin, destination=fbc.destination,
                                                     departure_date=departure_start.strftime(
                                                         FMD) + "--" + fbc.booking_end_date.strftime(FMD),
                                                     duration=str(fbc.min_duration) + "--" + str(fbc.max_duration),
                                                     direct="true" if fbc.number_of_connections == 0 else "false",
                                                     max_price=fbc.max_price)

        if not inspiration_data:
            return []

        for att in inspiration_data["results"]:
            low_fare_data = flight.low_fare_search(inspiration_data["origin"], att["destination"],
                                                   att["departure_date"], return_date=att["return_date"],
                                                   adults=fbc.number_of_adult_tickets,
                                                   direct="true" if fbc.number_of_connections == 0 else "false",
                                                   exclude_airlines=','.join(
                                                       fbc.exclude_companies) if fbc.exclude_companies else None,
                                                   max_price=fbc.max_price, number_of_results=250)
            if not low_fare_data:
                continue

            for res in low_fare_data["results"]:
                append = True
                for itnr in res["itineraries"]:
                    if len(itnr["inbound"]["flights"]) - 1 > fbc.number_of_connections or len(itnr["outbound"][
                        "flights"]) - 1 > fbc.number_of_connections:
                        append = False
                        break

                    t1 = itnr["inbound"]["flights"][0]["departs_at"]
                    t2 = itnr["inbound"]["flights"][len(itnr["inbound"]["flights"]) - 1]["arrives_at"]
                    tdelta = datetime.strptime(t2, FMT) - datetime.strptime(t1, FMT)
                    days, seconds = tdelta.days, tdelta.seconds
                    total_inbound_hours = days * 24 + seconds // 3600

                    if total_inbound_hours > fbc.max_flight_duration:
                        append = False
                        break

                    t1 = itnr["outbound"]["flights"][0]["departs_at"]
                    t2 = itnr["outbound"]["flights"][len(itnr["outbound"]["flights"]) - 1]["arrives_at"]
                    tdelta = datetime.strptime(t2, FMT) - datetime.strptime(t1, FMT)
                    days, seconds = tdelta.days, tdelta.seconds
                    total_outbound_hours = days * 24 + seconds // 3600

                    if total_outbound_hours > fbc.max_flight_duration:
                        append = False
                        break

                if append:
                    res_hash = self._hash_result(res)
                    ret[res_hash] = res

                    if len(ret) >= 5:
                        return ret.values()

        return ret.values()

    def _hash_result(self, result):
        return make_hash(result)


def make_hash(o):
    if isinstance(o, (set, tuple, list)):
        return tuple([make_hash(e) for e in o])

    elif not isinstance(o, dict):
        return hash(o)

    new_o = copy.deepcopy(o)
    for k, v in new_o.items():
        new_o[k] = make_hash(v)

    return hash(tuple(frozenset(sorted(new_o.items()))))