from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import pandas as pd
import re
from datetime import timedelta, date

import snscrape.modules.twitter as sntwitter
from itertools import islice

from time import sleep
import random

from progressbar import *
pbar = ProgressBar()

def get_tweets(query, since, until, num_tweets, city=None, within=None):
    # scrape all tweets using sntwitter
    criteria = f"{query} since:{since} until:{until} exclude:retweets exclude:replies lang:en"
    criteria += f" min_retweets:5 min_faves:5"  # this biases the search towards popular tweets
    if (city is not None and within is not None): 
        criteria += f" near:{city} within:{within}"
    else:
        pass #criteria += f" place:96683cc9126741d1"  # US place id
    
    tweets = islice(sntwitter.TwitterSearchScraper(criteria).get_items(), num_tweets)

    # process tweets to remove reply links and return a list of tweet content
    output = []
    for t in tweets:
        text = re.sub(r'https:\/\/t.co\/[A-Za-z0-9]{10}$', '', t.content, flags=re.MULTILINE)  # remove links to reply tweets
        output.append([text, t.date, t.retweetCount, t.likeCount, t.quoteCount])

    return pd.DataFrame(output, columns=["text", "date", "retweets", "likes", "quotes"])

query = "coronavirus OR covid"
tweets_per_day = 1000
start_date = date(2020, 2, 1)
end_date = date(2021, 5, 1)
df = pd.DataFrame()

pbar = ProgressBar(widgets=[Percentage(), Bar(), AdaptiveETA()], maxval=(end_date - start_date).days)
pbar.start()
for (i,d) in enumerate(pd.date_range(start_date, end_date)):
    since = d.strftime("%Y-%m-%d")
    until = (d + timedelta(days=1)).strftime("%Y-%m-%d")
    tweets = get_tweets(query, since, until, tweets_per_day)
    df = df.append(tweets)
    #print(i)
    pbar.update(i)

df.to_csv('./output.csv')
df.to_csv('./dataset.csv')
print("\nDone!\n")
