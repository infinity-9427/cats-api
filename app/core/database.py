from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings


class Database:
    client: AsyncIOMotorClient = None


db = Database()


async def get_database():
    """Get database instance."""
    return db.client.cats_api


async def connect_to_mongo():
    """Create database connection."""
    db.client = AsyncIOMotorClient(settings.DATABASE_URL)


async def close_mongo_connection():
    """Close database connection."""
    db.client.close()
