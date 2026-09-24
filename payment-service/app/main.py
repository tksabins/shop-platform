import os

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="ShopSphere Payment Service")

SERVICE_NAME = os.getenv("SERVICE_NAME", "payment-service")
VERSION = os.getenv("VERSION", "v1")


class PaymentRequest(BaseModel):
    order_id: int
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
    return {
        "payment_id": f"PAY-{payment.order_id}",
        "order_id": payment.order_id,
        "amount": payment.amount,
        "status": "success"
    }
