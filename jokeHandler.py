import pymongo
from pymongo import MongoClient
import random
import sys
sys.path.insert(0, '/Users/ciyengar/PycharmProjects/FlaskLogin-and-pymongo-master/app')
import jokes



jokesList = []
client = MongoClient('mongodb://localhost:27017/')
db = client.JokeReview

def populateList():
    cursor = db.jokes.find().sort([
    ("joke", pymongo.ASCENDING),
    ])
    count = 0
    for joke in cursor:
        if "content" in joke:
            joke_string = unicode(joke["content"]).encode("utf-8")
            joke_id = unicode(joke["_id"]).encode("utf-8")
            joke_title = "joke"
            new_joke = jokes.Joke(joke_string,"joke", joke_id)
            #print(joke_string)
            jokesList.append(new_joke)
            count += 1


def getRandomJoke():
    randInt = random.randrange(0, len(jokesList))
    #print(jokesList[randInt].content)
    return jokesList[randInt]


def addRating(joke_id, rating):
    client = MongoClient('mongodb://localhost:27017/')
    db = client.JokeReview
    rating_coll = db.ratings
    rating_coll.insert({
        "joke_id" : joke_id,
        "number_rating" : rating
    })