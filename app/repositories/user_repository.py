from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from app.models.user import User
from app.repositories.user_repository_interface import UserRepositoryInterface


class MongoUserRepository(UserRepositoryInterface):
    """MongoDB implementation of user repository."""
    
    def __init__(self, database: AsyncIOMotorDatabase):
        self.database = database
        self.collection = database.users
    
    async def create_user(self, user: User) -> User:
        """Create a new user."""
        try:
            user_dict = user.model_dump(exclude={"id"})
            result = await self.collection.insert_one(user_dict)
            user.id = str(result.inserted_id)
            return user
        except DuplicateKeyError as e:
            if "username" in str(e):
                raise ValueError(f"Username '{user.username}' already exists")
            else:
                raise ValueError("Duplicate data error occurred")
        except Exception as e:
            raise ValueError(f"Database error: {str(e)}")
    
    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        user_doc = await self.collection.find_one({"username": username})
        if user_doc:
            user_doc["id"] = str(user_doc["_id"])
            del user_doc["_id"]  # Remove the original _id field
            return User(**user_doc)
        return None
    
    async def get_all_users(self) -> List[User]:
        """Get all users."""
        users = []
        cursor = self.collection.find({})
        async for user_doc in cursor:
            user_doc["id"] = str(user_doc["_id"])
            del user_doc["_id"]  # Remove the original _id field
            users.append(User(**user_doc))
        return users
    
    async def username_exists(self, username: str) -> bool:
        """Check if username exists."""
        count = await self.collection.count_documents({"username": username})
        return count > 0
