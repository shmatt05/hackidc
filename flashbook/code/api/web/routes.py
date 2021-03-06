import webapp2
from api import WebURLs, API_PREFIX
from api.web import handlers
from webapp2_extras import routes


# noinspection PyPep8
APP = webapp2.WSGIApplication(
    [
        routes.PathPrefixRoute(API_PREFIX, [
            webapp2.Route(WebURLs.LOGIN, handler=handlers.LoginUserHandler),
            webapp2.Route(WebURLs.RECIPE_ALL, handler=handlers.RecipesHandler),
            webapp2.Route(WebURLs.RECIPE, handler=handlers.RecipeHandler),
        ])
    ], debug=True
)
