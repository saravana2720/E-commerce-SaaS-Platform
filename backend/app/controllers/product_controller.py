from sqlalchemy import or_

from app.extensions import db
from app.models.models import Inventory, Product


def list_products(search: str | None):
    query = Product.query.filter_by(is_active=True)
    if search:
        pattern = f"%{search}%"
        query = query.filter(or_(Product.name.ilike(pattern), Product.description.ilike(pattern)))
    items = query.order_by(Product.created_at.desc()).all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "slug": p.slug,
            "description": p.description,
            "price_paise": p.price_paise,
            "image_url": p.image_url,
        }
        for p in items
    ]


def get_product(product_id: int):
    p = Product.query.get_or_404(product_id)
    inv = Inventory.query.filter_by(product_id=product_id).first()
    return {
        "id": p.id,
        "name": p.name,
        "slug": p.slug,
        "description": p.description,
        "price_paise": p.price_paise,
        "image_url": p.image_url,
        "stock": inv.stock_qty if inv else 0,
    }


def upsert_product(payload, product_id=None):
    required = ["name", "slug", "description", "price_paise", "stock_qty"]
    if any(k not in payload for k in required):
        return {"message": f"Missing keys. Required: {required}"}, 400

    product = Product.query.get(product_id) if product_id else Product()
    if product_id and not product:
        return {"message": "Not found"}, 404

    product.name = payload["name"]
    product.slug = payload["slug"]
    product.description = payload["description"]
    product.price_paise = int(payload["price_paise"])
    product.image_url = payload.get("image_url")
    product.is_active = payload.get("is_active", True)
    db.session.add(product)
    db.session.flush()

    inventory = Inventory.query.filter_by(product_id=product.id).first() or Inventory(product_id=product.id)
    inventory.stock_qty = int(payload["stock_qty"])
    inventory.reorder_level = int(payload.get("reorder_level", 20))
    db.session.add(inventory)
    db.session.commit()

    return {"id": product.id}, 200 if product_id else 201


def delete_product(product_id: int):
    product = Product.query.get_or_404(product_id)
    product.is_active = False
    db.session.commit()
    return {"message": "Product archived"}, 200
