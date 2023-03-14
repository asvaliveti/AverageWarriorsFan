import requests
import random
import json
import os
from dotenv import load_dotenv


class Tweets:
    def getWarriorsTweet():
        load_dotenv()
        TWITTER_KEY = os.getenv('TWITTER_API_KEY')

        url = "https://twitter135.p.rapidapi.com/Search/"

        querystring = {"q":"Golden State Warriors", "count": "20"}

        headers = {
            "X-RapidAPI-Key": TWITTER_KEY,
            "X-RapidAPI-Host": "twitter135.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        json_data = response.text
        json_object = json.loads(json_data)["globalObjects"]["tweets"]

        listToSelectTweetFrom = []

        for key in json_object.keys():
            tweet = json_object[key]["full_text"]
            listToSelectTweetFrom.append(tweet)

        tweetToReturn = random.choice(listToSelectTweetFrom)
        return tweetToReturn