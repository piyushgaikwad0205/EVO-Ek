
from pymongo import MongoClient
from datetime import datetime

MONGO_URL = "mongodb://localhost:27017/"
DB_NAME = "safety_nav"

client = MongoClient(MONGO_URL)
db = client[DB_NAME]
hazards_collection = db["hazards"]

# Example insert function
def insert_hazard(hazard):
	hazard["timestamp"] = datetime.utcnow()
	hazards_collection.insert_one(hazard)

# Example fetch function
def get_hazards():
	return list(hazards_collection.find())
