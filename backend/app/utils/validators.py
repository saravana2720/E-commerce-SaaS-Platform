from marshmallow import Schema, ValidationError, fields, validate


class SignupSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2, max=120))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8, max=128))


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class CartAddSchema(Schema):
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True, validate=validate.Range(min=1, max=50))


class CheckoutSchema(Schema):
    address = fields.Dict(required=True)


def parse_or_400(schema, payload):
    try:
        return schema.load(payload)
    except ValidationError as exc:
        return {"errors": exc.messages}, 400
