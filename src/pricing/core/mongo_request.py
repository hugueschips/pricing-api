from bson.objectid import ObjectId
from fastapi import Depends, HTTPException
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from pricing.api.v0.firebase import validate_token
from pricing.core.settings import settings
from pricing.models.v0.user import User


def get_many_trips(query: dict, collection_name: str = "trip") -> list:
    connection = MongoClient(host=settings.MONGO_URI)
    database = connection[settings.MONGO_DBNAME]
    collection = database[collection_name]
    documents = list(collection.find(query))
    connection.close()
    return documents


def get_one_trip(
    id: str, user: User = Depends(validate_token), collection_name: str = "trip"
) -> list:
    connection = MongoClient(host=settings.MONGO_URI)
    database = connection[settings.MONGO_DBNAME]
    collection = database[collection_name]
    query = {"_id": ObjectId(id), "user": user.user_id}
    try:
        trip = collection.find_one(query)
        connection.close()
        return trip
    except Exception as e:
        connection.close()
        raise HTTPException(status_code=500, detail=str(e))


def get_one_document(
    unique_key: str, unique_id: str | ObjectId, collection_name: str
) -> dict:
    connection = MongoClient(host=settings.MONGO_URI)
    database = connection[settings.MONGO_DBNAME]
    collection = database[collection_name]
    query = {unique_key: unique_id}
    try:
        document = collection.find_one(query)
        connection.close()
        return document
    except Exception as e:
        connection.close()
        raise e


def insert_one_document(document, collection_name: str) -> list:
    connection = MongoClient(host=settings.MONGO_URI)
    database = connection[settings.MONGO_DBNAME]
    collection = database[collection_name]
    try:
        response = collection.insert_one(document)
        connection.close()
        return response
    except Exception as e:
        connection.close()
        raise HTTPException(status_code=500, detail=str(e))


def insert_or_replace_document(document, collection_name: str, unique_key: str) -> list:
    connection = MongoClient(host=settings.MONGO_URI)
    database = connection[settings.MONGO_DBNAME]
    collection = database[collection_name]
    unique_id = str(document.pop(unique_key))
    try:
        query = {unique_key: ObjectId(unique_id)}
        response = collection.update_one(query, {"$set": document}, upsert=True)
        connection.close()
        return response
    except DuplicateKeyError:
        connection.close()
        raise HTTPException(
            status_code=400, detail=f"Document with {unique_key} already exists."
        )
    except Exception as e:
        connection.close()
        raise HTTPException(status_code=500, detail=str(e))


def get_last_flespi_data() -> list[dict]:
    connection = MongoClient(host=settings.MONGO_URI)
    database = connection[settings.MONGO_DBNAME]
    collection = database["flespi"]

    result = collection.find({}, {"locations": {"$slice": -1}})

    # Initialize an empty list to store the last locations
    last_locations = []

    # Iterate through the result and append the last location for each document
    for document in result:
        if "locations" in document and document["locations"]:
            last_location = document["locations"][-1]
            last_locations.append(last_location)

    # Print or use the list as needed
    connection.close()
    return last_locations


def trim_flespi_document(id: str, last_item: int):
    connection = MongoClient(host=settings.MONGO_URI)
    database = connection[settings.MONGO_DBNAME]
    collection = database["flespi"]

    try:
        query = {"device_id": id}
        document = collection.find_one(query)
        last_item = min(last_item, len(document["locations"]) - 1)
        document["locations"] = document["locations"][last_item::]
        response = collection.update_one(query, {"$set": document}, upsert=True)
        connection.close()
        return response
    except Exception as e:
        connection.close()
        raise HTTPException(status_code=500, detail=str(e))
