from pymongo import MongoClient
from os import getenv

mongo_client = MongoClient(getenv('MONGO_URI'))
mongo_db = mongo_client["student_reports"]
mongo_collection = mongo_db["reports"]