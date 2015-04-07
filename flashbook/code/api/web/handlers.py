from shared.framework import Handler
from shared.models import Channel, ChannelItem
from serializers import ChannelSerializer

__author__ = 'david'


class ChannelsHandler(Handler):
    def get(self):
        serializer = ChannelSerializer()
        channels = self.data_service.query_entities(Channel)
        serialized_channels = [serializer.serialize(channel) for channel in channels]

        self.successful_response(channels=serialized_channels)
