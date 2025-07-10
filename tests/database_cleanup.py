"""
Database cleanup utility for tests.
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings


async def clean_test_database():
    """Clean test database collections."""
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    try:
        db = client.cats_api
        # Clean all collections
        await db.users.delete_many({})
        # Add other collections as needed
    finally:
        client.close()


def sync_clean_database():
    """Synchronous wrapper for database cleanup."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Create a new event loop in a thread
            import threading
            
            def run_clean():
                new_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(new_loop)
                try:
                    new_loop.run_until_complete(clean_test_database())
                finally:
                    new_loop.close()
            
            thread = threading.Thread(target=run_clean)
            thread.start()
            thread.join()
        else:
            loop.run_until_complete(clean_test_database())
    except RuntimeError:
        # No event loop running, create one
        asyncio.run(clean_test_database())
