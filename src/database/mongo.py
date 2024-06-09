import pymongo

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["student_reports"]
mongo_collection = mongo_db["reports"]
