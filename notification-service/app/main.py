import os

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="ShopSphere Notification Service")

SERVICE_NAME = os.getenv("SERVICE_NAME", "notification-service")
VERSION = os.getenv("VERSION", "v1")


class NotificationRequest(BaseModel):
    order_id: int
    user_id: int
    message: str


@app.get("/")
def root():
    return {
        "service": SERVICE_NAME,
        "version": VERSION,
        "message": "ShopSphere Notification Service"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": SERVICE_NAME
    }


@app.post("/notifications")
def send_notification(notification: NotificationRequest):
    return {
        "notification_id": f"NOTIFY-{notification.order_id}",
        "order_id": notification.order_id,
        "user_id": notification.user_id,
        "message": notification.message,
        "status": "sent"
    }
