"""
Routes for API are defined here.
"""
from flask import Blueprint, jsonify, request, g

from moody import geo
from moody.auth import require_token
from moody.db import session
from moody.models import MoodEvent, Place, User
from moody.schemas import CreateMoodEventSchema, MoodEventSchema, CreateUserSchema, UserSchema


main = Blueprint('main', __name__)


@require_token
@main.route('/mood_events', methods=['POST'])
def create_mood_event():
    """
    Create a mood event from request data

    Steps:
    1. Require user auth
    2. Validate request data
    3. Instantiate MoodEvent from request data
    4. Query places near mood event coords from Google Places API
    5. Get or create these places for our db
    6. Associate mood event with places
    7. Commit mood event and any new places to db
    8. Return serialized/jsonified mood event
    """
    request_body = request.get_json()
    kwargs = CreateMoodEventSchema(strict=True).load(request_body).data

    user = User.query.filter(User.email == g.validated_token['email']).one()
    mood_event = MoodEvent(**kwargs)

    places_from_google_api = geo.google_places_from_coord(
        latitude=mood_event.latitude,
        longitude=mood_event.longitude
    )

    places_from_db = [
        Place.get_or_create(**place)
        for place in places_from_google_api
    ]

    mood_event.places = places_from_db

    session.add(mood_event)
    session.commit()

    status = 201
    response_body = {
        'data': MoodEventSchema().dump(mood_event).data,
        'status': status
    }

    return jsonify(response_body), status


@require_token
@main.route('/mood_events', methods=['GET'])
def get_mood_events(**kwargs):
    """Get mood events"""
    user = User.query.filter(User.email == g.validated_token['email']).one()

    query = MoodEvent.apply_query_params(kwargs)
    query = query.filter(MoodEvent.user_id == user.id)
    mood_events = query.all()

    status = 200
    response_body = {
        'data': MoodEventSchema(many=True).dump(mood_events).data,
        'status': status
    }

    return jsonify(response_body), status


@main.route('/users', methods=['POST'])
def create_user():
    """Create a user"""
    request_body = request.get_json()
    kwargs = CreateUserSchema(strict=True).load(request_body).data

    user = User(**kwargs)
    session.add(user)
    session.commit()

    status = 201
    response_body = {
        'data': UserSchema().dump(user).data,
        'status': status
    }

    return jsonify(response_body), status


@main.route('/tokens', methods=['POST'])
def create_token():
    """Route to issue a token for a user based on authentication request"""
    request_body = request.get_json()
    kwargs = CreateTokenSchema(strict=True).load(request_body).data

    user = User.query.filter(User.email == kwargs['email']).one_or_none()

    if not user:
        raise UnauthorizedError("User with email does not exist or password is incorrect.")

    if not user.is_password_valid(kwargs['password']):
        raise UnauthorizedError("User with email does not exist or password is incorrect.")

    token = auth.create_token(user)

    status = 201
    response_body = {
        'status': status,
        'data': token
    }

    return jsonify(response_body), status


@require_token
@main.route('/tokeninfo', methods=['GET'])
def get_token_info():
    """Route to validate token and return token payload without db access"""
    status = 200
    response_body = {
        'status': status,
        'data': g.validated_token
    }

    return jsonify(response_body), status
