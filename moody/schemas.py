"""Request schemas are defined here"""
from marshmallow import Schema, ValidationError, fields, validates


class MoodEventSchema(Schema):
    """Schema for dumping a MoodEvent instance"""
    sentiment = fields.Str()
    longitude = fields.Float()
    latitude = fields.Float()
    user = fields.Nested('UserSchema')
    places = fields.Nested('PlaceSchema', many=True)


class CreateMoodEventSchema(Schema):
    """Schema for creating a MoodEvent"""
    sentiment = fields.Str(required=True)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)

    @validates('sentiment')
    def validate_sentiment(self, value):
        """Sentiment validation logic goes here"""
        sentiments = {'happy', 'sad', 'neutral'}

        if value not in sentiments:
            raise ValidationError(f"Sentiment must be one of {list(sentiments)} (given: {value}).")

        return sentiments

    @validates('longitude')
    def validate_longitude(self, value):
        """Longitude validation logic goes here"""
        if not -180 <= value <= 180:
            raise ValidationError(f"Longitude must be between -180 and 180 (given: {value}).")

    @validates('latitude')
    def validate_latitude(self, value):
        """Latitude validation logic goes here"""
        if not -90 <= value <= 90:
            raise ValidationError(f"Latitude must be between -90 and 90 (given: {value}).")


class PlaceSchema(Schema):
    """Schema for dumping a Place instance"""
    name = fields.Str()
    latitude = fields.Float()
    longitude = fields.Float()
    types = fields.List(fields.String())


class UserSchema(Schema):
    """Schema for dumping a User instance"""
    first_name = fields.Str()
    last_name = fields.Str()
    email = fields.Email()
    date_created = fields.DateTime()
    date_updated = fields.DateTime()


class CreateUserSchema(Schema):
    """Schema for loading request to create a user"""
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)

    @validates('email')
    def validate_email(self, value):
        """Email validation logic goes here"""
        if '@' not in value:
            raise ValidationError(f"No '@' found in email (given: {value}).")

        return True

    @validates('password')
    def validate_password(self, value):
        """Password validation logic goes here"""
        if len(value) < 8:
            raise ValidationError("Password must be 8 or more characters.")

        return True


class CreateTokenSchema(Schema):
    """Schema for loading request for token"""
    email = fields.Str(required=True)
    password = fields.Str(required=True)
