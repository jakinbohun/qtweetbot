#!/usr/bin/env python
# coding: utf-8

# In[6]:

'''
- Skills Utilized/Topics Visited -
Crontab Creation and Usage
    - During development of this simple tweetbot I learned how to set scripts
    for crontab usage. It is simple, but effective for automating a wide range
    of tasks.

    - It must be noted that crontab will not work if the computer is asleep or off.
    anacron can handle tasks on such a computer, but it can only perform each task
    once a day and not multiple times a day like crontab. This of course is not
    an issue on systems that are not regularly shutdown.

    - Launchd performs the same functionality, more or less, as anacron for Mac OSX.

    Future Improvements: Having different quotes set for each day.

    Additions:

API Usage through HTTP requests
    - Simple API call.

    Future Improvements: Remove reliance of calling on API each day by creating
        a collection of quotes that inspire me/are from different interests of
        mine.

        More importantly, check for new quotes not stored in a file and add them
        to the file.

    Additions:

Other Notes:
    I plan on implementing a factory method here with the addition of different
    quotes that will more than likely use different API calls.

'''

import tweepy
import json
import requests
import time
from twitter_bot_helper import *

# In[10]:


def get_quote_of_day():
    """Perform the API call and return the json portion of the response"""
    endpoint = 'http://quotes.rest/qod.json?category=inspire'
    response = requests.get(endpoint)
    if response.status_code != 200:
        raise Exception('Request was not successful')
    else:
        jsonRes = response.json()
        return jsonRes


# In[11]:


def create_tweet():
    """Retrieve the quote and the author from the json object and concatenate
    with attribution into a string that is returned as the tweet."""
    inc_json = get_quote_of_day()
    quote = inc_json['contents']['quotes'][0]['quote']
    author = inc_json['contents']['quotes'][0]['author']
    attribution = 'https://theysaidso.com/'
    tweet = """
            "{}" - {}
            A quote from - {}
            """.format(quote, author, attribution)
    return tweet


# In[12]:


def post_tweet():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    interval = 60 * 60 * 24
    while True:
        print('getting a random quote...')
        tweet = create_tweet()
        '''
        If the previous tweet is a copy of the same tweet,
        an exception will be raised, but the program will continue.
        In the event that the program is interrupted and restarted,
        a duplicate tweet will not be posted that day.
        '''
        try:
            api.update_status(tweet)
        except tweepy.TweepError as e:
            print(e.reason)
        time.sleep(interval)


# In[13]:


if __name__ == "__main__":
    post_tweet()


# In[ ]:
