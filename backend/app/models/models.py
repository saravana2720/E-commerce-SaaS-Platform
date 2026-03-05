import enum

from app.extensions import db
from app.models.base import TimestampMixin


class UserRole(enum.Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"


class OrderStatus(enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class PaymentStatus(enum.Enum):
    CREATED = "created"
    SUCCESS = "success"
    FAILED = "failed"


class User(TimestampMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.CUSTOMER)
    is_active = db.Column(db.Boolean, default=True, nullable=False)


class AdminUser(TimestampMixin, db.Model):
    __tablename__ = "admin_users"
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    permissions = db.Column(db.JSON, nullable=False, default=dict)


class Product(TimestampMixin, db.Model):
    __tablename__ = "products"
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    slug = db.Column(db.String(255), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    price_paise = db.Column(db.BigInteger, nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)


class Inventory(TimestampMixin, db.Model):
    __tablename__ = "inventory"
    id = db.Column(db.BigInteger, primary_key=True)
    product_id = db.Column(db.BigInteger, db.ForeignKey("products.id", ondelete="CASCADE"), unique=True)
    stock_qty = db.Column(db.Integer, nullable=False)
    reorder_level = db.Column(db.Integer, nullable=False, default=20)


class Cart(TimestampMixin, db.Model):
    __tablename__ = "cart"
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id", ondelete="CASCADE"), index=True)
    product_id = db.Column(db.BigInteger, db.ForeignKey("products.id", ondelete="CASCADE"), index=True)
    quantity = db.Column(db.Integer, nullable=False)

    __table_args__ = (db.UniqueConstraint("user_id", "product_id", name="uq_cart_user_product"),)


class Order(TimestampMixin, db.Model):
    __tablename__ = "orders"
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id", ondelete="RESTRICT"), index=True)
    status = db.Column(db.Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING)
    subtotal_paise = db.Column(db.BigInteger, nullable=False)
    tax_paise = db.Column(db.BigInteger, nullable=False, default=0)
    shipping_paise = db.Column(db.BigInteger, nullable=False, default=0)
    total_paise = db.Column(db.BigInteger, nullable=False)
    address = db.Column(db.JSON, nullable=False)


class OrderItem(TimestampMixin, db.Model):
    __tablename__ = "order_items"
    id = db.Column(db.BigInteger, primary_key=True)
    order_id = db.Column(db.BigInteger, db.ForeignKey("orders.id", ondelete="CASCADE"), index=True)
    product_id = db.Column(db.BigInteger, db.ForeignKey("products.id", ondelete="RESTRICT"), index=True)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price_paise = db.Column(db.BigInteger, nullable=False)
    line_total_paise = db.Column(db.BigInteger, nullable=False)


class Payment(TimestampMixin, db.Model):
    __tablename__ = "payments"
    id = db.Column(db.BigInteger, primary_key=True)
    order_id = db.Column(db.BigInteger, db.ForeignKey("orders.id", ondelete="RESTRICT"), index=True)
    provider = db.Column(db.String(50), nullable=False, default="razorpay")
    provider_order_id = db.Column(db.String(120), unique=True, nullable=False, index=True)
    provider_payment_id = db.Column(db.String(120), nullable=True, index=True)
    provider_signature = db.Column(db.String(255), nullable=True)
    amount_paise = db.Column(db.BigInteger, nullable=False)
    status = db.Column(db.Enum(PaymentStatus), nullable=False, default=PaymentStatus.CREATED)
