from shared.framework import Handler
from shared import Queues
from google.appengine.api import taskqueue
from shared.models import Recipe, BookingRequest
from jobs.examiners import BookingConditionExaminerFactory
from jobs import JobsURLs, get_jobs_full_url
from shared.framework import BusinessException

__author__ = 'Ari'


class CheckRecipeHandler(Handler):
    def post(self):
        recipe_id = self.request.get('recipe_id')
        recipe = self.data_service.get_entity(Recipe, int(recipe_id))

        if recipe is None:
            raise BusinessException(400, 'Invalid recipe id')

        booking_condition_examiner = BookingConditionExaminerFactory.create(recipe.booking_condition)
        possible_booking_infos = booking_condition_examiner.examine()
        if possible_booking_infos:
            self.__create_booking_request(recipe, possible_booking_infos)

    def __create_booking_request(self, recipe, possible_booking_infos):
        booking_request = BookingRequest(user=recipe.user, booking_infos=possible_booking_infos)
        self.data_service.update_entity(booking_request)


class CheckRecipesHandler(Handler):
    def post(self):
        enabled_recipes_filter = Recipe.enabled == True and Recipe.is_booked == False
        recipes_keys = self.data_service.query_entities(Recipe, keys_only=True,
                                                        filter_expression=enabled_recipes_filter)

        # Add the task to the recipe queue.
        for recipe in recipes_keys:
            taskqueue.Task(
                url=get_jobs_full_url(JobsURLs.CHECK_RECIPE),
                params={'recipe_id': recipe.id()}
            ).add(Queues.CHECK_RECIPE_QUEUE)
