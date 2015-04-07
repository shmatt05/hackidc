import logging
from google.appengine.api import mail


from google.appengine.ext import ndb
from google.appengine.api import search

from shared.models import Channel, ChannelItem

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


class ChannelService(object):
    def __init__(self):
        self.data_service = get_data_service()

    def get_channel_items(self, channel):
        return self.data_service.query_entities(ChannelItem,
                                                filter_expression=ChannelItem.channel == channel.key)


def get_channel_service():
    return ChannelService()

class EmailService(object):

    def __init__(self, receiver_email, pnr, name):
        self.receiver_email = receiver_email
        self.pnr = pnr
        self.sender_email = 'sender@flashbook-app.appspotmail.com'
        self.name = name

    def send_mail(self):
        message = mail.EmailMessage("Flashbook Inc. <" + self.sender_email + ">",
                            subject="Your Flight Has Been Booked!")
        message.to(self.name + "<" + self.receiver_email + ">")
        message.body = """
        Dear """ + str(self.name) + """

        Your flight has been succefully booked!
        PNR : """ + str(self.pnr)

        message.send()
