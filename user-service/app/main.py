import os

from fastapi import FastAPI

app = FastAPI(title="ShopSphere User Service")

SERVICE_NAME = os.getenv("SERVICE_NAME", "user-service")
VERSION = os.getenv("VERSION", "v1")


@app.get("/")
def root():
    return {
        "service": SERVICE_NAME,
        "version": VERSION,
        "message": "ShopSphere User Service"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": SERVICE_NAME
    }


@app.get("/users")
def get_users():
    return {
        "users": [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"},
            {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
        ]
    }
