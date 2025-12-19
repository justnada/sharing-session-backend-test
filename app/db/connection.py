from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings


class MongoDB:
    client: AsyncIOMotorClient = None


mongodb = MongoDB()


async def connect_to_mongo():
    """Membuat koneksi ke MongoDB"""
    mongodb.client = AsyncIOMotorClient(settings.mongodb_url)
    print(f"Connected to MongoDB: {settings.mongodb_url}")


async def close_mongo_connection():
    """Menutup koneksi ke MongoDB"""
    if mongodb.client:
        mongodb.client.close()
        print("Disconnected from MongoDB")


def get_database():
    """Mengambil instance database"""
    return mongodb.client.get_database()
