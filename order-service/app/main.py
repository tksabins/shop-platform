import os

import requests
from fastapi import FastAPI, HTTPException

app = FastAPI(title="ShopSphere Order Service")

SERVICE_NAME = os.getenv("SERVICE_NAME", "order-service")
VERSION = os.getenv("VERSION", "v1")

PRODUCT_SERVICE_URL = os.getenv(
    "PRODUCT_SERVICE_URL",
    "http://product-service:8000"
)

USER_SERVICE_URL = os.getenv(
    "USER_SERVICE_URL",
    "http://user-service:8000"
)


@app.get("/")
def root():
    return {
        "service": SERVICE_NAME,
        "version": VERSION,
        "message": "ShopSphere Order Service"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": SERVICE_NAME
    }


@app.get("/orders")
def get_orders():
    return {
        "orders": [
            {
                "id": 1001,
                "user_id": 1,
                "product_id": 1,
                "quantity": 1,
                "status": "created"
            },
            {
                "id": 1002,
                "user_id": 2,
                "product_id": 3,
                "quantity": 2,
                "status": "created"
            }
        ]
    }


@app.get("/order-summary")
def order_summary():
    try:
        product_response = requests.get(
            f"{PRODUCT_SERVICE_URL}/products",
            timeout=3
        )
        user_response = requests.get(
            f"{USER_SERVICE_URL}/users",
            timeout=3
        )

        product_response.raise_for_status()
        user_response.raise_for_status()

        return {
            "service": SERVICE_NAME,
            "products": product_response.json()["products"],
            "users": user_response.json()["users"]
        }

    except requests.RequestException as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Dependent service unavailable: {exc}"
        )
