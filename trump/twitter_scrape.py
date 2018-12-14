
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import datetime
import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser
from pymongo import MongoClient
import json

# edit these three variables
user = 'realDonaldTrump'
start = datetime.datetime(2017, 12, 1)  # year, month, day
end = datetime.datetime(2018, 12, 4)  # year, month, day

# only edit these if you're having problems

# don't mess with this stuff
days = (end - start).days + 1
user = user.lower()

driver = webdriver.Chrome("C:/Users/PhoenixJauregui/Documents/trump/trump/chromedriver2.exe")

executable_path = {'executable_path': 'C:/Users/PhoenixJauregui/Documents/trump/trump/chromedriver2.exe'}
browser = Browser('chrome', **executable_path, headless=False)

delay = 1

def format_day(date):
    day = '0' + str(date.day) if len(str(date.day)) == 1 else str(date.day)
    month = '0' + str(date.month) if len(str(date.month)) == 1 else str(date.month)
    year = str(date.year)
    return '-'.join([year, month, day])

def form_url(since, until):
    p1 = 'https://twitter.com/search?f=tweets&vertical=default&q=from%3A'
    p2 =  user + '%20since%3A' + since + '%20until%3A' + until + 'include%3Aretweets&src=typd'
    return p1 + p2

def increment_day(date, i):
    return date + datetime.timedelta(days=i)

def concat(words):
    concatenated = ""
    for i in range(len(words)):
        if concatenated == "":
            concatenated = words[i]
        else:    
            concatenated = concatenated +", " + words[i]
    return concatenated

dates = []
tweet_list = []   
trends = []
aux = []
increment = 0

for day in range(days):
    d1 = format_day(increment_day(start, 0))
    d2 = format_day(increment_day(start, 1))
    url = form_url(d1, d2)
    print(d1)
    driver.get(url)
    browser.visit(url)
    sleep(delay)
    
    # Retrieve all elements that contain tweet information
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')    
    try:
        elements = driver.find_elements_by_css_selector('.ProfileTweet-actionCountForPresentation')
        for element in elements:
            if element == '':
                aux.append('0')
            else:
                aux.append(element.text)
        tweets = soup.find_all('p', class_= "TweetTextSize js-tweet-text tweet-text")
        for tweet in tweets:    
            tweet2 = str(tweet.find_all(text=True, recursive=False)).replace(',', '').replace('\'','').replace('â€','').replace(':','').replace('\\','').replace("[","").replace("]","").replace("â€œ","")
            tweet_list.append(tweet2)
            dates.append(d1)
            
            increment += 1
            print("processing tweet " + str(increment))
            
            try:
                links = tweet.find_all('a')
                links2 = concat([link.find("b").text for link in links])
                trends.append(links2)
            except:
                trends.append("")
    except NoSuchElementException:
        print('no tweets on this day')
        
    start = increment_day(start, 1)
    
retweets = aux[1::5]
comments = aux[0::5]
favs = aux[3::5]

favs = [float(i.replace('K', '')) * 1000 for i in favs]
retweets = [float(i.replace('K', '')) * 1000 for i in retweets]
comments = [float(i.replace('K', '')) * 1000 for i in comments]


twitter = pd.DataFrame({
'Date': dates,
'Tweets': tweet_list,
'Trending': trends,
'Retweets': retweets,
'Favs': favs,
'Comments': comments,
})

twitter["Date"] = pd.to_datetime(twitter["Date"].values, infer_datetime_format=True)

twitter = twitter[twitter['Favs'] > 100]
twitter = twitter.set_index("Date")
twitter_group = twitter.groupby(pd.TimeGrouper("3d"))["Favs"].mean()

twitter.to_csv("tweets3.csv")

polls = pd.read_csv("https://projects.fivethirtyeight.com/trump-approval-data/approval_polllist.csv")
polls["enddate"] = pd.to_datetime(polls["enddate"].values)
polls_filtered = polls.set_index("enddate")['2017-1-11':'2018-12-04']
polls_group = polls_filtered.groupby(pd.TimeGrouper("3d"))['approve'].mean()

complete = pd.DataFrame(twitter_group).join(polls_group,how="right")
complete_final = complete.reset_index()
complete_final = complete_final.dropna()

dat = complete_final.to_dict(orient = "records")
dat2 = twitter.to_dict(orient = "records")
dat3 = polls_filtered.to_dict(orient = "records")

mongo = MongoClient('ds017678.mlab.com', 17678)
db = mongo['heroku_sjm9g8xc']
db.authenticate('heroku_sjm9g8xc', '4mvq9ej8mp5hlvqdqbgc53d2bf')

scraped = db.compare
scraped2 = db.twitter
scraped3 = db.polls

for pushed in dat:
    scraped.insert(pushed)

for pushed in dat2:
    scraped2.insert(pushed)

for pushed in dat3:
    scraped3.insert(pushed)