import webapp2
from api import WebURLs, API_PREFIX
from api.web import handlers
from webapp2_extras import routes


# noinspection PyPep8
APP = webapp2.WSGIApplication(
    [
        routes.PathPrefixRoute(API_PREFIX, [
            webapp2.Route(WebURLs.CHANNELS, handler=handlers.ChannelsHandler),
        ])
    ], debug=True
)
