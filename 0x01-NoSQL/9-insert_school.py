#!/usr/bin/env python3
"""
Inserts a new document.
"""


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a collection based on kwargs.
    """
    result = mongo_collection.insert_one(kwargs)
    return str(result.inserted_id)


if __name__ == "__main__":
    pass
