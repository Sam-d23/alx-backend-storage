#!/usr/bin/env python3
"""
This script connects to a MongoDB instance,
accesses the logs.nginx collection, and prints 
statistics about the Nginx logs stored in the collection.
"""


from pymongo import MongoClient

def log_stats():
    """
    Connect to MongoDB server
    """
    client = MongoClient('mongodb://localhost:27017/')
    db = client.logs
    collection = db.nginx
    total_logs = collection.count_documents({})
    print(f"{total_logs} logs")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")
    status_check_count = collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_check_count} status check")
