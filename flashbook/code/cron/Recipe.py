__author__ = 'Ari'

class Recipe(object):

    def parse_recipe(recipe):

        return dict(
            user=recipe.name,
            title=recipe.title,
            description=recipe.description,
            booking_condition=recipe.booking_condition,
            enabled=recipe.enabled,
            enabled_at=recipe.enabled_at,
            created_at=recipe.created_at,
            booked=recipe.booked
            #TODO: Add all fields to be transmitted to tomer API.

        )



