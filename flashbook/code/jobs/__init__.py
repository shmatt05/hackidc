__author__ = 'Ari'

JOBS_PREFIX = '/jobs'


def get_jobs_full_url(url):
    return JOBS_PREFIX + url


class JobsURLs(object):
    CHECK_RECIPES = '/check-recipes'
    CHECK_RECIPE = '/check-recipe'
    PERFORM_BOOKINGS = '/perform-bookings'