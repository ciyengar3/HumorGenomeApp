#!/usr/bin/python

from werkzeug.security import generate_password_hash
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


def addUser(username, password, first_name, last_name, internal):
    # Connect to the DB
    collection = MongoClient()["JokeReview"]["users"]

    # Ask for data to store
    pass_hash = generate_password_hash(password, method='pbkdf2:sha256')
    print(username)
    print(password)
    # Insert the user in the DB
    try:
        collection.insert({"_id": username, "password": pass_hash, "first_name": first_name, "last_name": last_name, "internal": internal})
        print "User created."
    except DuplicateKeyError:
        print "User already present in DB."


if __name__ == '__main__':
    addUser()
