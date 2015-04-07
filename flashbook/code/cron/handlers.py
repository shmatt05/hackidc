from shared.framework import Handler
from shared import Queues
from google.appengine.api import taskqueue
from shared.models import Recipe, BookingRequest
from cron.examiners import BookingConditionExaminerFactory
from shared.services import EmailService
from shared.services import BookingService

__author__ = 'Ari'

class CheckRecipeHandler(Handler):

    def post(self):
        recipe_id = self.request.get('recipe_id')
        recipe = self.data_service.get_entity(Recipe, recipe_id)

        booking_condition_examiner = BookingConditionExaminerFactory.create(recipe.booking_condition)
        possible_booking_infos = booking_condition_examiner.examine()
        if possible_booking_infos:
            self.__create_booking_request(recipe, possible_booking_infos)

    def __create_booking_request(self, recipe, possible_booking_infos):
        booking_request = BookingRequest(user=recipe.user, booking_infos=possible_booking_infos, recipe_id=recipe.id())
        self.data_service.update_entity(booking_request)



class RecipesHandler(Handler):
    def post(self):
        recipes_keys = self.data_service.query_entities(Recipe, keys_only=True)

        # Add the task to the recipe queue.
        for recipe in recipes_keys:
            taskqueue.Task(
                params={'recipe_id':recipe.id()}
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



