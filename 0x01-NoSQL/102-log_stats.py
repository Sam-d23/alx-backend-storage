#!/usr/bin/env python3
"""
This script connects to a MongoDB instance,
accesses the logs.nginx collection, and prints 
statistics about the Nginx logs stored in the collection,
including top 10 most present IPs.
"""

from pymongo import MongoClient


def log_stats(mongo_collection):
    """
    Print statistics about Nginx logs including total logs, HTTP methods, status check,
    and top 10 most present IPs.

    Args:
        mongo_collection (pymongo.collection.Collection): The PyMongo collection object for nginx logs.
    """
    # Total logs count
    total_logs = mongo_collection.count_documents({})
    print(f"{total_logs} logs")

    # HTTP methods count
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        count = mongo_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    # Status check count
    status_check_count = mongo_collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_check_count} status check")

    # Top 10 IPs by count
    print("IPs:")
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_ips = mongo_collection.aggregate(pipeline)
    for idx, ip_doc in enumerate(top_ips, 1):
        ip = ip_doc["_id"]
        count = ip_doc["count"]
        print(f"\t{ip}: {count}")


if __name__ == "__main__":
    # Connect to MongoDB server and access the logs.nginx collection
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx
    log_stats(nginx_collection)
