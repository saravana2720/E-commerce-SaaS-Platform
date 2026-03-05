from flask_jwt_extended import get_jwt_identity
from sqlalchemy import select

from app.extensions import db
from app.models.models import Cart, Inventory, Order, OrderItem, OrderStatus, Payment, PaymentStatus, Product
from app.services.payment_service import RazorpayService


def add_to_cart(payload):
    user_id = int(get_jwt_identity())
    product_id = int(payload["product_id"])
    qty = int(payload["quantity"])

    product = Product.query.filter_by(id=product_id, is_active=True).first_or_404()
    item = Cart.query.filter_by(user_id=user_id, product_id=product.id).first()
    if item:
        item.quantity += qty
    else:
        item = Cart(user_id=user_id, product_id=product.id, quantity=qty)
    db.session.add(item)
    db.session.commit()
    return {"message": "Added to cart"}, 201


def get_cart():
    user_id = int(get_jwt_identity())
    rows = (
        db.session.query(Cart, Product)
        .join(Product, Product.id == Cart.product_id)
        .filter(Cart.user_id == user_id)
        .all()
    )
    items = []
    total = 0
    for cart, product in rows:
        line = cart.quantity * product.price_paise
        total += line
        items.append({"product_id": product.id, "name": product.name, "quantity": cart.quantity, "unit_price_paise": product.price_paise, "line_total_paise": line})
    return {"items": items, "total_paise": total}


def checkout(address: dict):
    user_id = int(get_jwt_identity())
    cart_items = Cart.query.filter_by(user_id=user_id).all()
    if not cart_items:
        return {"message": "Cart is empty"}, 400

    subtotal = 0
    order_items = []

    with db.session.begin_nested():
        for item in cart_items:
            product = Product.query.get(item.product_id)
            inventory = db.session.execute(
                select(Inventory).where(Inventory.product_id == product.id).with_for_update()
            ).scalar_one()

            if inventory.stock_qty < item.quantity:
                return {"message": f"Insufficient stock for {product.name}"}, 409

            inventory.stock_qty -= item.quantity
            line_total = item.quantity * product.price_paise
            subtotal += line_total
            order_items.append((item, product, line_total))

        shipping = 5000 if subtotal < 49900 else 0
        total = subtotal + shipping
        order = Order(user_id=user_id, subtotal_paise=subtotal, shipping_paise=shipping, tax_paise=0, total_paise=total, status=OrderStatus.PENDING, address=address)
        db.session.add(order)
        db.session.flush()

        for cart, product, line_total in order_items:
            db.session.add(
                OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=cart.quantity,
                    unit_price_paise=product.price_paise,
                    line_total_paise=line_total,
                )
            )

        razorpay_order = RazorpayService.create_order(total, receipt=f"order_{order.id}")
        payment = Payment(order_id=order.id, provider_order_id=razorpay_order["id"], amount_paise=total, status=PaymentStatus.CREATED)
        db.session.add(payment)

        Cart.query.filter_by(user_id=user_id).delete()

    db.session.commit()
    return {"order_id": order.id, "razorpay_order_id": payment.provider_order_id, "amount_paise": total}


def list_orders():
    user_id = int(get_jwt_identity())
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    return [{"id": o.id, "status": o.status.value, "total_paise": o.total_paise, "created_at": o.created_at.isoformat()} for o in orders]


def verify_payment(payload):
    payment = Payment.query.filter_by(provider_order_id=payload["razorpay_order_id"]).first_or_404()
    valid = RazorpayService.verify_signature(
        payload["razorpay_order_id"], payload["razorpay_payment_id"], payload["razorpay_signature"]
    )
    if not valid:
        payment.status = PaymentStatus.FAILED
        db.session.commit()
        return {"message": "Invalid signature"}, 400

    payment.provider_payment_id = payload["razorpay_payment_id"]
    payment.provider_signature = payload["razorpay_signature"]
    payment.status = PaymentStatus.SUCCESS
    order = Order.query.get(payment.order_id)
    order.status = OrderStatus.PAID
    db.session.commit()
    return {"message": "Payment verified", "order_id": order.id}, 200
