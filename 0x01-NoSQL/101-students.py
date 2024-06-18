#!/usr/bin/env python3
"""
Returns all students sorted by average score.
"""


from pymongo import collection


def top_students(mongo_collection):
    """
    Script's function.
    """
    pipeline = [
        {"$project": {"name": "$name", "averageScore": {"$avg": "$topics.score"}}},
        {"$sort": {"averageScore": -1}}
    ]
    
    return mongo_collection.aggregate(pipeline)
