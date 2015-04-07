__author__ = 'Ari'
from shared.framework import Handler
from shared.models import Recipe
from shared import Queues
from google.appengine.api import taskqueue

import webapp2
import Recipe
import Queue



class checkRecipeHandler(Handler):

    def post(self):
        recipe_id = self.request.get('recipe_id')
        recipe = self.data_service.get_entity_by_key(recipe_id)
        params_dict = Recipe.parsed_recipe(recipe)

        #TODO: get_results_from_tomer
    #TODO: def get_Results_from_tomer




class RecipesHandler(Handler):
    def post(self):
        recipes_keys = self.data_service.query_entities(Recipe, keys_only=True)

        # Add the task to the recipe queue.
        for recipe in recipes_keys:
            taskqueue.Task(
                params={'recipe_id':recipe.id()}
            ).add(Queues.CHECK_RECIPE_QUEUE)
