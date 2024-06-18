#!/usr/bin/env python3
"""
Returns all students sorted by averrage score.
"""


from pymongo import MongoClient


def top_students(mongo_collection):
    """
    Script's function.
    """
    pipeline = [
        {"$project": {"name": 1, "averageScore": {"$avg": "$scores"}}},
        {"$sort": {"averageScore": -1}}
    ]

    return list(mongo_collection.aggregate(pipeline))


if __name__ == "__main__":
    client = MongoClient('mongodb://localhost:27017/')
    top_students_data = top_students(client.my_db.students)
    for student in top_students_data:
        print(student)
