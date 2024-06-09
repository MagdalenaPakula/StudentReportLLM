import pymongo

mongo_client = pymongo.MongoClient("mongodb://mongo:27017/")
mongo_db = mongo_client["student_reports"]
mongo_collection = mongo_db["reports"]
