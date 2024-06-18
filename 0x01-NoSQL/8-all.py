#!/usr/bin/env python3
"""
Operates on MongoDB
"""


def list_all(mongo_collection):
    """
    Lists all documents in a collection.
    """
    return list(mongo_collection.find({}))


if __name__ == "__main__":
    pass
