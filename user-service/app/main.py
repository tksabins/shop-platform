
import os

import psycopg2
from psycopg2 import errors
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(title="ShopSphere User Service")

SERVICE_NAME = os.getenv("SERVICE_NAME", "user-service")
VERSION = os.getenv("VERSION", "v3")


def get_db_connection():
    return psycopg2.connect(
        host=os.environ["POSTGRES_HOST"],
        port=int(os.getenv("POSTGRES_PORT", "5432")),
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        connect_timeout=5,
    )


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr


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
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT id, name, email FROM users ORDER BY id"
                )
                users = cursor.fetchall()

        return {"users": [dict(user) for user in users]}

    except psycopg2.Error:
        raise HTTPException(
            status_code=503,
            detail="Database temporarily unavailable"
        )


@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    """
                    INSERT INTO users (name, email)
                    VALUES (%s, %s)
                    RETURNING id, name, email
                    """,
                    (user.name, str(user.email))
                )
                created_user = cursor.fetchone()

        return dict(created_user)

    except errors.UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    except psycopg2.Error:
        raise HTTPException(
            status_code=503,
            detail="Database temporarily unavailable"
        )

