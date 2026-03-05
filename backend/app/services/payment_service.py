import hmac
import hashlib

import razorpay
from flask import current_app


class RazorpayService:
    @staticmethod
    def client():
        return razorpay.Client(
            auth=(
                current_app.config["RAZORPAY_KEY_ID"],
                current_app.config["RAZORPAY_KEY_SECRET"],
            )
        )

    @staticmethod
    def create_order(amount_paise: int, receipt: str):
        payload = {"amount": amount_paise, "currency": "INR", "receipt": receipt}
        return RazorpayService.client().order.create(data=payload)

    @staticmethod
    def verify_signature(order_id: str, payment_id: str, signature: str) -> bool:
        secret = current_app.config["RAZORPAY_KEY_SECRET"].encode()
        body = f"{order_id}|{payment_id}".encode()
        digest = hmac.new(secret, body, hashlib.sha256).hexdigest()
        return hmac.compare_digest(digest, signature)
