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

def get_tweets(query, since, until, num_tweets, show_pbar=False):
    # scrape all tweets using sntwitter
    criteria = f"{query} since:{since} until:{until} exclude:retweets exclude:replies lang:en"
    criteria += f" min_retweets:20 min_faves:20"  # this biases the search towards popular tweets
    tweets = islice(sntwitter.TwitterSearchScraper(criteria).get_items(), num_tweets)

    # process tweets to remove reply links and return a list of tweet content
    output = []
    if (show_pbar):
        pbar = ProgressBar(widgets=[Percentage(), Bar(), ETA()], maxval=num_tweets)
        pbar.start()
    for (i,t) in enumerate(tweets):
        text = re.sub(r'https:\/\/t.co\/[A-Za-z0-9]{10}$', '', t.content, flags=re.MULTILINE)  # remove links to reply tweets
        output.append([text, t.date])
        if show_pbar: pbar.update(i+1)
    return pd.DataFrame(output, columns=["text", "date"])

query = "coronavirus"
tweets_per_day = 50
start_date = date(2020, 1, 1)
end_date = date(2021, 5, 1)
df = pd.DataFrame()

pbar = ProgressBar(widgets=[Percentage(), Bar(), AdaptiveETA()], maxval=(end_date - start_date).days)
pbar.start()
for (i,d) in enumerate(pd.date_range(start_date, end_date)):
    since = d.strftime("%Y-%m-%d")
    until = (d + timedelta(days=1)).strftime("%Y-%m-%d")
    tweets = get_tweets(query, since, until, tweets_per_day)
    df = df.append(tweets)
    pbar.update(i)

df.to_csv('./output.csv')
print("\nDone!\n")
