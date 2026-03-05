from flask import Blueprint, request
from flask_limiter.util import get_remote_address

from app.controllers.auth_controller import login, signup
from app.extensions import limiter

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.post("/signup")
@limiter.limit("10/minute", key_func=get_remote_address)
def signup_route():
    body = request.get_json(force=True)
    response, status = signup(body)
    return response, status


@bp.post("/login")
@limiter.limit("20/minute", key_func=get_remote_address)
def login_route():
    body = request.get_json(force=True)
    response, status = login(body)
    return response, status
