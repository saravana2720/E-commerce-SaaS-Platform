from flask import Blueprint, request

from app.controllers.product_controller import get_product, list_products

bp = Blueprint("products", __name__, url_prefix="/products")


@bp.get("")
def products_list():
    return {"items": list_products(request.args.get("search"))}


@bp.get("/<int:product_id>")
def product_detail(product_id: int):
    return get_product(product_id)
