import json
from shared.framework import Handler, BusinessException
from shared.models import Recipe, User
from serializers import RecipeSerializer, UserSerializer
from validators import InsertRecipeValidator
from datetime import datetime

__author__ = 'david'


def authenticate_user():
    def actual_decorator(method):
        def wrapper(self, *args, **kwargs):
            try:
                self.user = self.authentication_service.authenticate_user()

                return method(self, *args, **kwargs)
            except BusinessException, ex:
                self.digest_exception(ex)

        return wrapper

    return actual_decorator


class LoginUserHandler(Handler):
    def __init__(self, *args, **kwargs):
        super(LoginUserHandler, self).__init__(*args, **kwargs)

    def post(self):
        serializer = UserSerializer()
        authenticated_user = self.authentication_service.login_user()
        self.successful_response(authenticated_user=serializer.serialize(authenticated_user))


class RecipesHandler(Handler):
    @authenticate_user()
    def get(self):
        serializer = RecipeSerializer()
        recipes = self.data_service.query_entities(Recipe, filter_expression=Recipe.user == self.user.key)
        serialized_recipes = [serializer.serialize(recipe) for recipe in recipes]

        self.successful_response(recipes=serialized_recipes)

    @authenticate_user()
    def post(self):
        serializer = RecipeSerializer()
        serialized_recipe = json.loads(self.request.body)

        InsertRecipeValidator().validate(serialized_recipe)

        recipe = serializer.deserialize_new_recipe(serialized_recipe)
        recipe.user = self.user.key
        if recipe.enabled:
            recipe.enabled_at = datetime.now()

        self.data_service.update_entity(recipe)

        self.successful_response(recipe_id=recipe.key.id())
