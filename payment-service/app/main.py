import os

import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="ShopSphere Payment Service")

SERVICE_NAME = os.getenv("SERVICE_NAME", "payment-service")
VERSION = os.getenv("VERSION", "v1")

NOTIFICATION_SERVICE_URL = os.getenv(
    "NOTIFICATION_SERVICE_URL",
    "http://notification-service:8000"
)


class PaymentRequest(BaseModel):
    order_id: int
    user_id: int
    amount: float


@app.get("/")
def root():
    return {
        "service": SERVICE_NAME,
        "version": VERSION,
        "message": "ShopSphere Payment Service"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": SERVICE_NAME
    }


@app.post("/payments")
def process_payment(payment: PaymentRequest):
    payment_result = {
        "payment_id": f"PAY-{payment.order_id}",
        "order_id": payment.order_id,
        "amount": payment.amount,
        "status": "success"
    }

    try:
        notification_response = requests.post(
            f"{NOTIFICATION_SERVICE_URL}/notifications",
            json={
                "order_id": payment.order_id,
                "user_id": payment.user_id,
                "message": f"Payment successful for order {payment.order_id}"
            },
            timeout=3
        )

        notification_response.raise_for_status()

        payment_result["notification"] = notification_response.json()

        return payment_result

    except requests.RequestException as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Notification service unavailable: {exc}"
        )
