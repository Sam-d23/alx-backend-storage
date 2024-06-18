#!/usr/bin/env python3
"""
Returns a list of schools.
"""


def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of schools having a specific topic.
    """
    results = mongo_collection.find({"topics": topic})
    return list(results)
