import webapp2
from cron import CronURLs
from cron import handlers


# noinspection PyPep8
APP = webapp2.WSGIApplication(
    [
        webapp2.Route(CronURLs.CHECK_RECIPE, handler=handlers.CheckRecipeHandler),
    ], debug=True
)
