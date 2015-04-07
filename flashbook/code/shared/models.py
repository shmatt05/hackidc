__author__ = 'david'

from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel


class Video(ndb.Model):
    title = ndb.StringProperty(required=True)
    url = ndb.StringProperty(required=True)
    created_at = ndb.DateTimeProperty(auto_now_add=True)


class Channel(ndb.Model):
    title = ndb.StringProperty(required=True)
    description = ndb.StringProperty(required=True)
    intro_video = ndb.KeyProperty(kind=Video, required=True)


class ChannelItem(polymodel.PolyModel):
    channel = ndb.KeyProperty(kind=Channel, required=True)
    title = ndb.StringProperty(required=True)
    description = ndb.StringProperty()
    video = ndb.KeyProperty(Video, required=True)
    related_items = ndb.KeyProperty(repeated=True)

    # questionnaire = ndb.KeyProperty(Video, required=True)
    # additional_material = ndb.KeyProperty(AdditionalMaterial, required=True)


class Term(ChannelItem):
    pass


class TopicalNews(ChannelItem):
    pass


class Lesson(ndb.Model):
    title = ndb.StringProperty(required=True)
    video = ndb.KeyProperty(Video, required=True)


class Course(ChannelItem):
    lessons = ndb.LocalStructuredProperty(Lesson, repeated=True)
