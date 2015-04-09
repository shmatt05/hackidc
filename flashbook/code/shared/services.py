import logging
import json
import urllib2
import random
import os
import sys
from google.appengine.api import mail
from google.appengine.ext import ndb
from google.appengine.api import search, urlfetch
from shared.models import User
from shared.framework import BusinessException

__author__ = 'david'


class DataService(object):
    def update_entity(self, entity):
        return entity.put()

    def update_entities(self, entities_to_update):
        return ndb.put_multi(entities_to_update)

    def get_entity(self, entity_type, entity_id, parent_key=None):
        return ndb.Key(entity_type, entity_id, parent=parent_key).get()

    def get_entity_by_key(self, entity_key, use_cache=None):
        return entity_key.get(use_cache=use_cache)

    def get_entities(self, entity_keys, include_none=False):
        returned_entities = ndb.get_multi(entity_keys)

        if include_none:
            return returned_entities

        return [entity for entity in returned_entities if entity is not None]

    def get_key(self, entity_type, eid):
        return ndb.Key(entity_type, eid)

    def get_keys(self, entity_type, eids):
        return [self.get_key(entity_type, eid) for eid in eids]

    def query_entities(self, entity_type, filter_expression=None, offset=None, limit=None, projection=None,
                       keys_only=False, order=None):
        query = entity_type.query()

        if filter_expression is not None:
            query = query.filter(filter_expression)

        if order is not None:
            if isinstance(order, (list, tuple)):
                for arg in order:
                    query = query.order(arg)
            else:
                query = query.order(order)

        return query.fetch(limit=limit, projection=projection, offset=offset, keys_only=keys_only)

    def query_entity_page(self, entity_type, page_size, cursor=None, filter_expression=None, projection=None,
                          keys_only=False, order=None):
        query = entity_type.query()

        if filter_expression is not None:
            query = query.filter(filter_expression)

        if order is not None:
            if isinstance(order, (list, tuple)):
                for arg in order:
                    query = query.order(arg)
            else:
                query = query.order(order)

        is_query_multi_filter = isinstance(query.filters, (list, ndb.query.ConjunctionNode, ndb.query.DisjunctionNode))
        if query.orders is not None and is_query_multi_filter:
            query = query.order(entity_type.key)

        page, cursor, more = query.fetch_page(
            page_size, start_cursor=cursor, projection=projection, keys_only=keys_only
        )

        return page, cursor, more

    def delete_entity(self, entity_key):
        entity_key.delete()

    def delete_entities(self, entity_keys):
        ndb.delete_multi(entity_keys)

    def count_entity(self, entity_type, filter_expression=None):
        query = entity_type.query()

        if filter_expression is not None:
            query = query.filter(filter_expression)

        return query.count(keys_only=True)

    def full_text_query(self, index_name, query_string=None, cursor=None, offset=None, limit=None, sort_options=None,
                        ids_only=True, deadline=None):
        options = search.QueryOptions(
            limit=limit,
            cursor=cursor,
            offset=offset,
            sort_options=sort_options,
            ids_only=ids_only
        )

        logging.debug('Running full text search. Index: %s. Query: %s', index_name, query_string)

        query = search.Query(query_string=query_string, options=options)

        index = search.Index(name=index_name)
        documents = index.search(query, deadline=deadline)

        return documents, documents.cursor, documents.number_found


def get_data_service():
    return DataService()


class FlightSearch:
    """ Flight Search API """

    def __init__(self):
        """ Set API KEY """
        self.api_key = "nzPtUZtGWpnYAkC1NGGlNQxjCTMyPVfs"

    def inspiration_search(self, origin, destination=None, departure_date=None, duration=None, direct=None,
                           max_price=None, aggregation_mode="DAY"):
        """ Amadeus Inspiration Search """
        uri = "http://api.sandbox.amadeus.com/v1.2/flights/inspiration-search?"
        uri_dict = {}
        if origin is None:
            return False
        else:
            uri_dict["origin"] = origin

        uri_dict["destination"] = destination
        uri_dict["departure_date"] = departure_date
        uri_dict["duration"] = duration
        uri_dict["direct"] = direct
        uri_dict["max_price"] = max_price
        uri_dict["aggregation_mode"] = aggregation_mode
        uri_dict["apikey"] = self.api_key

        query = ""
        for parm in uri_dict:
            if uri_dict[parm] is not None:
                query += parm + "=" + str(uri_dict[parm]) + "&"

        url = uri + query[:-1]

        try:
            urlfetch.set_default_fetch_deadline(60)
            return json.load(urllib2.urlopen(url))
        except Exception:
            return False

    def low_fare_search(self, origin, destination, departure_date, return_date=None, arrive_by=None, return_by=None,
                        adults=1, direct="false", include_airlines=None, exclude_airlines=None, currency="USD",
                        max_price=None, number_of_results=250):
        """ Amadeus Low Fare Search """
        uri = "http://api.sandbox.amadeus.com/v1.2/flights/low-fare-search?"
        uri_dict = {}
        if origin is None:
            return False
        else:
            uri_dict["origin"] = origin

        if destination is None:
            return False
        else:
            uri_dict["destination"] = destination

        if departure_date is None:
            return False
        else:
            uri_dict["departure_date"] = departure_date

        uri_dict["return_date"] = return_date
        uri_dict["arrive_by"] = arrive_by
        uri_dict["return_by"] = return_by
        uri_dict["adults"] = adults
        uri_dict["direct"] = direct
        if include_airlines:
            uri_dict["include_airlines"] = include_airlines
        if exclude_airlines:
            uri_dict["exclude_airlines"] = exclude_airlines
        uri_dict["currency"] = currency
        uri_dict["max_price"] = max_price
        uri_dict["number_of_results"] = number_of_results
        uri_dict["apikey"] = self.api_key

        query = ""
        for parm in uri_dict:
            if uri_dict[parm] is not None:
                query += parm + "=" + str(uri_dict[parm]) + "&"

        url = uri + query[:-1]

        try:
            urlfetch.set_default_fetch_deadline(60)
            return json.load(urllib2.urlopen(url))
        except Exception, ex:
            return False


class EmailService(object):
    sender_email = 'sender@flashbook-app.appspotmail.com'

    def send_confirmation_email(self, user, booking_info):
        confirmation_format = open(os.path.dirname(__file__) + '/assets/confirmation_format.html').read()

        outbound_table = self.__build_itineraries(booking_info.origin, booking_info.destination,
                                                  booking_info.itineraries[0]['outbound'])

        inbound_table = self.__build_itineraries(booking_info.destination, booking_info.origin,
                                                 booking_info.itineraries[0]['inbound'])

        message = mail.EmailMessage(to=user.name + " <" + user.email + ">",
                                    sender="Flashbook Inc. <" + self.sender_email + ">",
                                    subject="Your Flight Has Been Booked!",
                                    html=confirmation_format.replace('{name}', user.name)
                                    .replace('{passport}', '3433222093')
                                    .replace('{pnr}', booking_info.pnr or '')
                                    .replace('{origin}', booking_info.origin)
                                    .replace('{destination}', booking_info.destination)
                                    .replace('{price}', str(booking_info.price))
                                    .replace('{outbound}', outbound_table)
                                    .replace('{inbound}', inbound_table))

        message.send()

    def __build_itineraries(self, origin, destination, itinerary):
        result = '<table><tr><td colspan="4">{0} to {1}</td></tr>'.format(origin, destination)
        flights = itinerary['flights']
        i = 1
        for flight in flights:
            departure = flight['departs_at']
            arrival = flight['arrives_at']
            origin = flight['origin']['airport']
            destination = flight['destination']['airport']
            flight_num = flight['operating_airline'] + flight['flight_number']
            result += '<tr><td>Flight {0}</td><td>Departure: {1} from {2}</td><td>Arrival: {3} to {4}</td><td>Flight #: {5}</td></tr>'.format(
                i, departure, origin, arrival, destination, flight_num)
            i += 1

        result += '</table>'
        return result


class BookingService(object):
    """
    Only works in the Live API, not in the sandbox HackIDC,
    So we mock the booking process.
    """

    def book(self, booking_info):
        if booking_info:
            booking_info.pnr = str(random.randint(0, sys.maxint))

        return booking_info


class FairnessService(object):
    def pick_fairest_booking_info(self, booking_request, booking_requests):
        return booking_request.booking_infos[0]


class AuthenticationService(object):
    def __init__(self):
        self.data_service = get_data_service()
        self.default_user = User(name="Ari Propper",
                                 email="aripro@gmail.com",
                                 address="16, Rue Yafo, 94142 JERUSALEM, ISRAEL")

    def login_user(self):
        users = self.data_service.query_entities(User)
        if users:
            return users[0]
        else:
            self.data_service.update_entity(self.default_user)
            return self.default_user

    def authenticate_user(self):
        users = self.data_service.query_entities(User)
        if users:
            return users[0]

        raise BusinessException(400, 'Authentication Failed')


def get_authentication_service():
    return AuthenticationService()