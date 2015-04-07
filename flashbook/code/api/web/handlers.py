from shared.framework import Handler
from shared.models import Recipe
from serializers import RecipeSerializer

__author__ = 'david'


class RecipesHandler(Handler):
    def get(self):
        serializer = RecipeSerializer()
        # TODO: get only the authenticated user's recipes.
        recipes = self.data_service.query_entities(Recipe)
        serialized_recipes = [serializer.serialize(recipe) for recipe in recipes]

        self.successful_response(recipes=serialized_recipes)
