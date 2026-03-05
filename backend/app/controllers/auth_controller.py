from flask_jwt_extended import create_access_token

from app.extensions import bcrypt, db
from app.models.models import User, UserRole
from app.utils.validators import LoginSchema, SignupSchema, parse_or_400


def signup(payload):
    parsed = parse_or_400(SignupSchema(), payload)
    if isinstance(parsed, tuple):
        return parsed

    if User.query.filter_by(email=parsed["email"].lower()).first():
        return {"message": "Email already registered"}, 409

    user = User(
        name=parsed["name"],
        email=parsed["email"].lower(),
        password_hash=bcrypt.generate_password_hash(parsed["password"]).decode(),
        role=UserRole.CUSTOMER,
    )
    db.session.add(user)
    db.session.commit()
    return {"id": user.id, "email": user.email}, 201


def login(payload):
    parsed = parse_or_400(LoginSchema(), payload)
    if isinstance(parsed, tuple):
        return parsed

    user = User.query.filter_by(email=parsed["email"].lower(), is_active=True).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, parsed["password"]):
        return {"message": "Invalid credentials"}, 401

    token = create_access_token(identity=str(user.id), additional_claims={"role": user.role.value})
    return {"access_token": token, "user": {"id": user.id, "name": user.name, "role": user.role.value}}, 200
