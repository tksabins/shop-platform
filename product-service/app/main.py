import os
import time

from fastapi import FastAPI

app = FastAPI(title="ShopSphere Product Service")

SERVICE_NAME = os.getenv("SERVICE_NAME", "product-service")
VERSION = os.getenv("VERSION", "v1")


@app.get("/")
def root():
    return {
        "service": SERVICE_NAME,
        "version": VERSION,
        "message": "ShopSphere Product Service"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": SERVICE_NAME
    }


@app.get("/products")
def get_products():
    return {
        "products": [
            {
                "id": 1,
                "name": "Laptop",
                "price": 75000
            },
            {
                "id": 2,
                "name": "Mobile Phone",
                "price": 35000
            },
            {
                "id": 3,
                "name": "Headphones",
                "price": 5000
            }
        ]
    }


@app.get("/slow")
def slow_endpoint():
    time.sleep(5)

    return {
        "message": "Slow response"
    }
