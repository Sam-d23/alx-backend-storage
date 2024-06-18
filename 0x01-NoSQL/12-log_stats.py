#!/usr/bin/env python3
"""
This script connects to a MongoDB instance,
accesses the logs.nginx collection, and prints 
statistics about the Nginx logs stored in the collection.
"""


from pymongo import MongoClient


def log_stats(mongo_collection):
    """
    The function of the script.
    """
    total_logs = mongo_collection.count_documents({})
    print(f"{total_logs} logs")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        count = mongo_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")
    status_check_count = mongo_collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_check_count} status check")


if __name__ == "__main__":
    # Connect to MongoDB server and access the logs.nginx collection
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx
    log_stats(nginx_collection)
