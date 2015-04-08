import webapp2
from jobs import JobsURLs, JOBS_PREFIX
from jobs import handlers
from webapp2_extras import routes

# noinspection PyPep8
APP = webapp2.WSGIApplication(
    [
        routes.PathPrefixRoute(JOBS_PREFIX, [
            webapp2.Route(JobsURLs.CHECK_RECIPES, handler=handlers.CheckRecipesHandler),
            webapp2.Route(JobsURLs.CHECK_RECIPE, handler=handlers.CheckRecipeHandler),
        ])
    ], debug=True
)
