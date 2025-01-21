import logging
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from grading.database.qdrant import generate_embedding, save_to_qdrant

app = Flask(__name__)

client = MongoClient("mongodb://mongo:27017/")
db = client["reports_db"] 
reports_collection = db["reports"] 

@app.route("/a", methods=["GET"])
def index():

    try:
        reports = reports_collection.find({}, {"_id": 1, "title": 1})
        texts = [{"id": str(report["_id"]), "title": report["title"]} for report in reports]
        return render_template("index.html", texts=texts)
    except Exception as e:
        app.logger.error(f"Error fetching texts: {e}")
        return jsonify({"error": "Unable to fetch texts"}), 500

@app.route("/grading/texts", methods=["GET"])
def get_texts():
    try:
        reports = reports_collection.find({}, {"_id": 1, "title": 1}) 
        texts = [{"id": str(report["_id"]), "title": report["title"]} for report in reports]
        return jsonify(texts)
    except Exception as e:
        app.logger.error(f"Error fetching texts: {e}")
        return jsonify({"error": "Unable to fetch texts"}), 500

@app.route("/grading/embed/<text_id>", methods=["POST"])
def embed_text(text_id):
    try:
        report = reports_collection.find_one({"_id": MongoClient.ObjectId(text_id)})
        if not report:
            return jsonify({"error": "Text not found"}), 404
        
        text = report["text"]
        embedding = generate_embedding(text)
        
        save_to_qdrant(collection="report_analysis", file_name=report["title"], text=embedding)
        
        return jsonify({"embedding": embedding})
    
    except Exception as e:
        app.logger.error(f"Error embedding text: {e}")
        return jsonify({"error": "Unable to generate embedding"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
