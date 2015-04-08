from shared.framework import Handler
from shared import Queues
from google.appengine.api import taskqueue
from shared.models import Recipe, BookingRequest
from shared.services import EmailService, FairnessService, BookingService
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

        if recipe.is_booked:
            return

        booking_condition_examiner = BookingConditionExaminerFactory.create(recipe.booking_condition)
        possible_booking_infos = booking_condition_examiner.examine()
        if possible_booking_infos:
            self.__create_booking_request(recipe, possible_booking_infos)

    def __create_booking_request(self, recipe, possible_booking_infos):
        booking_request = BookingRequest(id=BookingRequest.calculate_id(recipe.user, recipe),
                                         user=recipe.user,
                                         booking_infos=possible_booking_infos,
                                         recipe=recipe.key)

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


class BookingHandler(Handler):
    def __init__(self, *args, **kwargs):
        super(BookingHandler, self).__init__(*args, **kwargs)
        self.fairness_service = FairnessService()
        self.booking_service = BookingService()
        self.email_service = EmailService()

    def post(self):
        booking_requests = self.data_service.query_entities(BookingRequest,
                                                            filter_expression=BookingRequest.is_booked == False)

        for booking_request in booking_requests:
            booking_info_to_book = self.fairness_service.pick_fairest_booking_info(booking_request, booking_requests)
            self.booking_service.book(booking_info_to_book)
            user = self.data_service.get_entity_by_key(booking_request.user)
            self.email_service.send_confirmation_email(user, booking_info_to_book)

            recipe = self.data_service.get_entity_by_key(booking_request.recipe)
            booking_request.is_booked = True
            recipe.is_booked = True
            self.data_service.update_entities([booking_request, recipe])
