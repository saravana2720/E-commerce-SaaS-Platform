from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.controllers.product_controller import delete_product, upsert_product
from app.middlewares.authz import admin_required
from app.models.models import Inventory, Order, OrderItem, Product

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.post("/product")
@jwt_required()
@admin_required
def admin_add_product():
    return upsert_product(request.get_json(force=True))


@bp.put("/product/<int:product_id>")
@jwt_required()
@admin_required
def admin_update_product(product_id: int):
    return upsert_product(request.get_json(force=True), product_id)


@bp.delete("/product/<int:product_id>")
@jwt_required()
@admin_required
def admin_delete_product(product_id: int):
    return delete_product(product_id)


@bp.get("/orders")
@jwt_required()
@admin_required
def admin_orders():
    orders = Order.query.order_by(Order.created_at.desc()).limit(200).all()
    return {
        "items": [
            {"id": o.id, "user_id": o.user_id, "status": o.status.value, "total_paise": o.total_paise}
            for o in orders
        ]
    }


@bp.get("/analytics/revenue")
@jwt_required()
@admin_required
def admin_revenue():
    total = sum(o.total_paise for o in Order.query.all())
    top_products = (
        Product.query.join(OrderItem, OrderItem.product_id == Product.id)
        .with_entities(Product.name, OrderItem.quantity)
        .order_by(OrderItem.quantity.desc())
        .limit(5)
        .all()
    )
    low_stock = Inventory.query.filter(Inventory.stock_qty <= Inventory.reorder_level).all()
    return {
        "total_revenue_paise": total,
        "top_products": [{"name": p[0], "qty": p[1]} for p in top_products],
        "low_stock": [{"product_id": i.product_id, "stock_qty": i.stock_qty} for i in low_stock],
    }
