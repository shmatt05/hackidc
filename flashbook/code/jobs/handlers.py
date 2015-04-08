from shared.framework import Handler
from shared import Queues
from google.appengine.api import taskqueue
from shared.models import Recipe, BookingRequest
from shared.services import EmailService
from shared.services import BookingService
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
        booking_request = BookingRequest(user=recipe.user, booking_infos=possible_booking_infos, recipe=recipe.key)
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

    """
    Assuming all entities in the database has booking request (Query met conditions),
    Books the invitation and sends emails to costumers.
    """

    def post(self):
        booking_list = self.data_service.query_entities(BookingRequest)
        if booking_list:

            #TODO: FareNess Goes Here
            for booking in booking_list:
                if not(booking.is_booked):
                    #TODO: add pnr and other relevant infos
                    pnr_tmp = BookingService.book(booking)
                    mail_sender = EmailService(booking.user.email, booking.user.name, pnr_tmp)
                    mail_sender.send_mail()
                    booking.is_booked = True
                    #Updates the booking status to booked @ DB & updates the recipe db table
                    self.data_service.update_entity(booking)
                    recipe_to_change = self.data_service.get_entity_by_key(booking.recipe_id)
                    recipe_to_change.is_booked = True
                    self.data_service.update_entity(recipe_to_change)
                else:
                    continue



