from fastapi import FastAPI, HTTPException
from pymongo import MongoClient, DESCENDING
from models.transactions import Transaction
import os
from typing import List

app = FastAPI(title="Transaction Stream API")

# MongoDB connection
mongo_host = os.getenv('MONGO_HOST', 'localhost')
mongo_user = os.getenv('MONGO_USER', 'admin')
mongo_pass = os.getenv('MONGO_PASS', 'password')
mongo_uri = f"mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:27017/"
client = MongoClient(mongo_uri)
db = client['transactions']
collection = db['transactions']

@app.get("/")
def root():
    return {"status": "ok", "message": "Transaction Stream API is running"}

@app.get("/transactions/latest", response_model=List[Transaction])
def get_latest_transactions(limit: int = 10):
    try:
        docs = list(collection.find().sort("timestamp", DESCENDING).limit(limit))
        # Convert ObjectId to str and parse to Transaction
        for doc in docs:
            doc['id'] = str(doc.get('id', ''))
        return [Transaction(**doc) for doc in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/transactions/stats")
def get_transaction_stats():
    try:
        total = collection.count_documents({})
        pipeline = [
            {"$group": {
                "_id": None,
                "total_amount": {"$sum": "$amount"},
                "avg_amount": {"$avg": "$amount"},
                "max_amount": {"$max": "$amount"},
                "min_amount": {"$min": "$amount"}
            }}
        ]
        stats = list(collection.aggregate(pipeline))
        if not stats:
            return {"total": 0, "total_amount": 0, "avg_amount": 0, "max_amount": 0, "min_amount": 0}
        s = stats[0]
        return {
            "total": total,
            "total_amount": round(s["total_amount"], 2),
            "avg_amount": round(s["avg_amount"], 2),
            "max_amount": round(s["max_amount"], 2),
            "min_amount": round(s["min_amount"], 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/transactions/by-category")
def get_transactions_by_category():
    try:
        pipeline = [
            {"$group": {"_id": "$category", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        cats = list(collection.aggregate(pipeline))
        return {cat["_id"]: cat["count"] for cat in cats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
