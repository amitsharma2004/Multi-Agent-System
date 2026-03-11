from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

mongodb_client: AsyncIOMotorClient = None


async def connect_to_mongo():
    """Connect to MongoDB"""
    global mongodb_client
    try:
        mongodb_client = AsyncIOMotorClient(settings.mongodb_url, serverSelectionTimeoutMS=5000)
        # Test connection
        await mongodb_client.admin.command('ping')
        print(f"✅ Connected to MongoDB at {settings.mongodb_url}")
        
        # Create indexes
        db = mongodb_client[settings.database_name]
        await db.users.create_index("email", unique=True)
        await db.leads.create_index("user_id")
        await db.leads.create_index("status")
        print("✅ Database indexes created")
    except Exception as e:
        print(f"⚠️  MongoDB connection failed: {e}")
        print("⚠️  Server will run without database. Please start MongoDB to use database features.")


async def close_mongo_connection():
    """Close MongoDB connection"""
    global mongodb_client
    if mongodb_client:
        mongodb_client.close()
        print("✅ Closed MongoDB connection")


def get_database():
    """Get database instance"""
    return mongodb_client[settings.database_name]
