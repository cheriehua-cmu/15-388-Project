import snscrape.modules.twitter as sntwitter
from itertools import islice
from lxml import html
import requests
from time import sleep

def get_tweets(query, since, until, max_tweets=100):
    criteria = f"{query} since:{since} until:{until} exclude:retweets exclude:replies lang:en"
    tweets = islice(sntwitter.TwitterSearchScraper(criteria).get_items(), max_tweets)
    return tweets

for t in get_tweets("uwu", "2020-12-1", "2020-12-5", 1):
    xpath = f'/html/body/div/div/div/div[1]' #/main/div/div/div/div/div/div[2]/div/section/div/div/div[1]/div/div/article/div/div/div/div[3]/div[1]/div/div/span'
    headers = headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
    xpath = 'string()'
    page = requests.get(t, headers=headers)
    tree = html.fromstring(page.content)
    l = tree.xpath(xpath)
    print(t)
    #print(l)
    sleep(4)


# This is an alternative method to get tweets that uses selenium and a headless chrome browser, in case sntwitter fails.
def get_tweets2(query, start_date, end_date, max_tweets):
    # initiate chrome webdriver (headless to save resources)
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(executable_path = './chromedriver.exe', chrome_options=options)
    df = pd.DataFrame()

    # get list of links to tweets
    urls = ['https://twitter.com/EguProperty/status/1335010863900549120', 'https://twitter.com/skelegreg/status/1335010852941000705']

    # xpath to get tweet contents
    post_element_xpath = '/html/body/div/div/div/div[2]/main/div/div/div/div/div/div[2]/div/section/div/div/div[1]/div/div/article/div/div/div/div[3]/div[1]/div/div/span'

    # scrape each tweet url
    for url in urls:
        driver.get(url)
        sleep(1)
    
        post_list = driver.find_elements_by_xpath(post_element_xpath)
        post_text = ''.join([x.text for x in post_list])

        temp_df = pd.DataFrame([post_text], columns={'all_text'})
        df = df.append(temp_df)
        driver.find_element_by_xpath('//body').send_keys(Keys.END)

        #print(df)
        #print("\n")

    return df