from pymongo import MongoClient
from pymongo.errors import CollectionInvalid
from News_Aggregator.fastapi_app.models import schema


# MongoDB connection settings
MONGODB_URI = "mongodb://localhost:27017/"
DB_NAME = "news_aggregator_db"

FIELDS_VALIDATION_RULES = {
    "username": {
        "$jsonSchema": {
            "bsonType": "string",
            "minLength": 8,
            "pattern": "^(?=.*[a-zA-Z])(?=.*[!@#$%^&*()_+\\-=\[\]{};:\'\"<>,./?])(?=.*[0-9])[a-zA-Z0-9!@#$%^&*()_+\\-=\[\]{};:\'\"<>,./?]{8,}$",
            "description": "must be a string and contain at least one alphanumeric character, one special character, and be at least 8 characters long"
        }
    },
    "email": {
        "$jsonSchema": {
            "bsonType": "string",
            "format": "email",
            "description": "must be a valid email address"
        }
    },
    "password": {
        "$jsonSchema": {
            "bsonType": "string",
            "minLength": 8,
            "pattern": "^(?=.*[a-zA-Z])(?=.*[!@#$%^&*()_+\\-=\[\]{};:\'\"<>,./?])(?=.*[0-9])[a-zA-Z0-9!@#$%^&*()_+\\-=\[\]{};:\'\"<>,./?]{8,}$",
            "description": "must be a string and contain at least one alphanumeric character, one special character, and be at least 8 characters long"
        }
    }
}


def create_database_and_collection():
    # Connect to MongoDB
    client = MongoClient(MONGODB_URI)
    db = client[DB_NAME]

    # Create collection based on Pydantic model class name
    collection_name = schema.UserCreate.__name__
    try:
        db.create_collection(collection_name, validator=FIELDS_VALIDATION_RULES)
        print(f"Collection '{collection_name}' created successfully.")
    except CollectionInvalid:
        print(f"Collection '{collection_name}' already exists.")


if __name__ == "__main__":
    create_database_and_collection()
