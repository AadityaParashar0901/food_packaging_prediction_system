import os

_client = None


def connect_db():
    global _client

    uri = os.getenv(
        "MONGODB_URI",
        "mongodb://127.0.0.1:27017/food_packaging",
    )

    try:
        from pymongo import MongoClient

        _client = MongoClient(uri, serverSelectionTimeoutMS=1500)
        _client.admin.command("ping")
    except Exception:
        _client = None


def close_db():
    global _client

    if _client is not None:
        _client.close()
        _client = None


def database_status():
    return "connected" if _client is not None else "unavailable"
