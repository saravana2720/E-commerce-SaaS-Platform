from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.controllers.order_controller import add_to_cart, checkout, get_cart, list_orders, verify_payment
from app.utils.validators import CartAddSchema, CheckoutSchema, parse_or_400

bp = Blueprint("orders", __name__)


@bp.post("/cart/add")
@jwt_required()
def cart_add():
    parsed = parse_or_400(CartAddSchema(), request.get_json(force=True))
    if isinstance(parsed, tuple):
        return parsed
    return add_to_cart(parsed)


@bp.get("/cart")
@jwt_required()
def cart_get():
    return get_cart()


@bp.post("/orders/checkout")
@jwt_required()
def order_checkout():
    parsed = parse_or_400(CheckoutSchema(), request.get_json(force=True))
    if isinstance(parsed, tuple):
        return parsed
    return checkout(parsed["address"])


@bp.get("/orders")
@jwt_required()
def orders_list():
    return {"items": list_orders()}


@bp.post("/payments/verify")
@jwt_required()
def payment_verify():
    body = request.get_json(force=True)
    required = ["razorpay_order_id", "razorpay_payment_id", "razorpay_signature"]
    if any(k not in body for k in required):
        return {"message": "Missing payment fields"}, 400
    return verify_payment(body)
