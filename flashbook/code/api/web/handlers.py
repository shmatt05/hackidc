import json
from shared.framework import Handler
from shared.models import Recipe
from serializers import RecipeSerializer
from validators import InsertRecipeValidator
from datetime import datetime

__author__ = 'david'


class RecipesHandler(Handler):
    def get(self):
        serializer = RecipeSerializer()
        # TODO: get only the authenticated user's recipes.
        recipes = self.data_service.query_entities(Recipe)
        serialized_recipes = [serializer.serialize(recipe) for recipe in recipes]

        self.successful_response(recipes=serialized_recipes)

    def post(self):
        serializer = RecipeSerializer()
        serialized_recipe = json.loads(self.request.body)

        InsertRecipeValidator().validate(serialized_recipe)

        recipe = serializer.deserialize_new_recipe(serialized_recipe)
        if recipe.enabled:
            recipe.enabled_at = datetime.now()

        self.data_service.update_entity(recipe)

        self.successful_response(recipe_id=recipe.key.id())
