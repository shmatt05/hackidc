from shared.services import get_data_service, get_channel_service

__author__ = 'david'


class VideoSerializer(object):
    def serialize(self, video):
        return dict(
            title=video.title,
            url=video.url
        )


class ChannelItemSerializer(object):
    def __init__(self):
        self.data_service = get_data_service()

    def serialize(self, channel_item):
        video_serializer = VideoSerializer()
        video = self.data_service.get_entity_by_key(channel_item.video)

        return dict(
            id=channel_item.key.id(),
            title=channel_item.title,
            description=channel_item.description,
            video=video_serializer.serialize(video)
        )


class ChannelSerializer(object):
    def __init__(self):
        self.data_service = get_data_service()
        self.channel_service = get_channel_service()

    def serialize(self, channel):
        video_serializer = VideoSerializer()
        channel_item_serializer = ChannelItemSerializer()

        channel_items = self.channel_service.get_channel_items(channel)
        intro_video = self.data_service.get_entity_by_key(channel.intro_video)

        return dict(
            id=channel.key.id(),
            title=channel.title,
            intro_video=video_serializer.serialize(intro_video),
            items=[channel_item_serializer.serialize(channel_item) for channel_item in channel_items]
        )
