from marshmallow import Schema, fields, ValidationError, validate, validates_schema
import re


# Custom password validator
def validate_password(password):
    """Validate password complexity: at least one uppercase letter, one lowercase letter, one digit, and one special character."""
    if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
        raise ValidationError(
            "Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character."
        )


# Token response schema (for login)
class TokenResponseSchema(Schema):
    email = fields.Str(required=True, description="User email", error_messages={"required": "Email is required."})
    password = fields.Str(required=True, description="User password",
                          error_messages={"required": "Password is required."})


# Register schema (for registration)
class RegisterSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(
        required=True,
        validate=validate.Regexp(
            r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
            error="Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character."
        )
    )
    confirm_password = fields.Str(required=True)

    @validates_schema
    def validate_passwords(self, data, **kwargs):
        """Ensure that password and confirm_password match and validate password complexity."""
        if data["password"] != data["confirm_password"]:
            raise ValidationError("Passwords do not match.", field_name="confirm_password")

        # Apply custom password complexity check
        validate_password(data["password"])

        return data


# Schema for general character properties
class CharacterSchema(Schema):
    limit = fields.Int(load_default=20, metadata={"description": "Number of results per page (default: 20)."})
    skip = fields.Int(load_default=0, metadata={"description": "Number of results to skip (default: 0)."})


# Schema for user-related data
class UserSchema(Schema):
    id = fields.Integer(dump_only=True)  # ID is read-only
    name = fields.String(required=True, validate=validate.Length(min=1))
    house = fields.String(required=True, validate=validate.Length(min=1))
    animal = fields.String(required=False, validate=validate.Length(min=1))
    symbol = fields.String(required=True, validate=validate.Length(min=1))
    nickname = fields.String(required=True, validate=validate.Length(min=1))
    role = fields.String(required=True, validate=validate.Length(min=1))
    age = fields.Integer(required=True, validate=validate.Range(min=0))
    death = fields.Integer(required=False, validate=validate.Range(min=0))
    strength = fields.String(required=True, validate=validate.Length(min=1))


# Schema for user deletion (without full data)
class UserSchemaDeletion(Schema):
    id = fields.Int(required=True, description="ID of the user to delete")


# Schema to manage character details (filtering and inclusion)
class GetCharacterSchema(Schema):
    include_id = fields.Bool(load_default=False, description="Include id information in the response.")
    include_name = fields.Bool(load_default=False, description="Include name information in the response.")
    include_house = fields.Bool(load_default=False, description="Include house information in the response.")
    include_role = fields.Bool(load_default=False, description="Include role information in the response.")
    include_age = fields.Bool(load_default=False, description="Include age information in the response.")


# Schema for complex filtering (characters)
class FilterCharactersQuerySchema(Schema):
    name = fields.Str(required=False, description="Filter by character's name.")
    house = fields.Str(required=False, description="Filter by character's house.")
    role = fields.Str(required=False, description="Filter by character's role.")
    age_min = fields.Int(required=False, description="Filter by minimum age.")
    age_max = fields.Int(required=False, description="Filter by maximum age.")
    include_age = fields.Bool(required=False, description="Whether to include age filtering.")
    sort_by = fields.Str(required=False, description="Attribute to sort by (e.g., name, age).")
    sort_order = fields.Str(required=False, validate=lambda x: x in ['asc', 'desc'],
                            description="Sort order ('asc' or 'desc').")


# Schema for sorting characters
class SortRequestSchema(Schema):
    sort_by = fields.Str(load_default="name", validate=lambda x: x in ["name", "age", "house"],
                         metadata={"description": "Field to sort by."})
    sort_order = fields.Str(load_default="asc", validate=lambda x: x in ["asc", "desc"],
                            metadata={"description": "Sort order (asc or desc)."})


# Schema for pagination, sorting, and filtering characters
character_schema = CharacterSchema()
characters_schema = CharacterSchema(many=True)


# Login Schema
class LoginSchema(Schema):
    email = fields.Email(required=True, description="User's email")
    password = fields.String(required=True, description="User's password")
