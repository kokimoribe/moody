import itertools
from collections import Counter

from sqlalchemy import joinedload

from moody.models import MoodEvent


def get_frequency_distribution(created_before, created_after, user):
    """
    Get frequency distribution for a user's mood events
    """

    query = MoodEvent.query
        .filter(
            MoodEvent.date_created >= created_after,
            MoodEvent.date_created <= created_before,
            MoodEvent.user_id == user.id
        )

    mood_events = query.all()

    sentiments = (mood_event.sentiment for mood_event in mood_events)

    frequency_distribution = Counter(sentiments)

    return frequency_distribution

    # It's also possible to do this calculation entirely in the query
    # query = session.query(MoodEvent.sentiment, func.count(MoodEvent.sentiment)).group_by(MoodEvent.sentiment).filter(...)


def get_place_counts(user, sentiment):
    """
    Get count of how many MoodEvents with a particular sentiment are associated with each place
    """

    query = MoodEvent.query
        .filter(MoodEvent.sentiment == sentiment, MoodEvent.user_id == user.id)
        .options(joinedload(MoodEvent.places))

    mood_events = query.all()

    places = (place for mood_event in mood_events for place in mood_event.places)

    counts = Counter((place.name for place in places))

    return counts

    # query = session.query(Place.name, func.count(Place.name)).group_by(Place.name)
    #   .join(Place.mood_events)
    #   .filter(MoodEvent.sentiment = sentiment, MoodEvent.user_id == user.id)
