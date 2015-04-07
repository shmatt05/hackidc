__author__ = 'Ari'
from shared.framework import Handler
import webapp2
import Recipe

class checkRecipeHandler(webapp2.RequestHandler):

    def post(self):
        recipe_id = self.request.get('recipe_id')
        recipe = self.data_service.get_entity_by_key(recipe_id)
        params_dict = Recipe.parsed_recipe(recipe)

        #TODO: get_results_from_tomer
    #TODO: def get_Results_from_tomer







