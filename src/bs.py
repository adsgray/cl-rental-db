#!/usr/bin/python

import ConfigParser
import sys
import codecs
import re
import requests
import json
from bs4 import BeautifulSoup
import sqlite3 as lite
from sqlite3 import IntegrityError
import locguess

config = ConfigParser.ConfigParser()
config.read("config.ini")
dbpath = config.get("main", "dbpath")
slacktoken = config.get("main", "slacktoken")

soup = BeautifulSoup(codecs.open(sys.argv[1], "r", "utf-8"), "lxml")

# wheee global db variables (traditional)
con = lite.connect(dbpath)
con.text_factory = str
cur = con.cursor()


def add_ad_to_db(ad):
    """
    Add this ad to the db
    """
    loc1 = locguess.guessLocation(ad['title'], ad['loctext'])
    add = ('INSERT INTO ad (time, title, loctext, bedrooms, squarefeet, price, loc1, furnished) values(?,?,?,?,?,?,?,?)')
    data = (ad['time'], ad['title'], ad['loctext'], ad['bedrooms'], ad['squarefeet'], ad['price'], loc1, ad['furnished'])
    try:
        cur.execute(add, data)
        return "added";
    except IntegrityError:
        print("constraint fail")
        print(ad)
        return "duplicate";


def guessLocation(title, location):
    # use map of regex->location_string to guess?
    mapping = {}
    return guessFromStringWithMapping(title + " " + location, mapping)

def guessBedrooms(title):
    mapping = {}
    return guessFromStringWithMapping(title, mapping)

def guessSquarefoot(title):
    mapping = {}
    return guessFromStringWithMapping(title, mapping)


def getTime(item):
    t = item.find_all('time')
    return t[0]['datetime']

def getTitle(item):
    title = item.find('a', class_="hdrlnk")
    return title.contents[0].encode("utf-8")

# return number of bedrooms and square footage, if present
def getHousing(item):
    h = item.find('span', class_='housing')
    try:
        # eg "/ 2br - 1000ft"
        raw = h.contents[0]
        m = re.search("(\d+)br\s", raw)
        if m:
            bedrooms = m.group(1)
        else:
            bedrooms = 0

        #m = re.search("-\s+(\d+)ft", raw)
        m = re.search("-\s+(\d+)", raw)
        if m:
            squarefeet = m.group(1)
        else:
            squarefeet = 0

        return {"bedrooms": bedrooms, "squarefeet": squarefeet}

    except AttributeError:
        # will have to figure out from title?
        return {"bedrooms": 0, "squarefeet": 0}

def getPrice(item):
    p = item.find_all('span', class_='result-price')
    try:
        raw = p[0].contents[0]
        clean = re.sub('[$,]', '', raw)
        m = re.search("(\d+)", clean)
        if m:
            ret = m.group(1) 
            return ret
        else:
            return 0
    except IndexError:
        return -1

def getLocation(item):
    #loc = item.find_all('span', class_='pnr')
    loc = item.find_all('span', class_='result-hood')
    if loc:
        raw = loc[0].contents[0] #.contents[0]
        m = re.search("\((.+)\)", raw)
        if m:
            return m.group(1).encode("utf-8")
        else:
            return ""
    else:
        return ""

# returns 1 if title contains "Furnished" 0 otherwise
def getFurnished(title):
    r = re.compile("\bfurnished", re.IGNORECASE)
    if re.search(r, title):
        return 1
    else:
        return 0


def send_stats_to_slack(results):
    """
    Send stats to slack channel.
    """
    slackurl="https://hooks.slack.com/services/" + slacktoken
    payload = {'text': "added {0}, {1} duplicates.".format(results["added"], results["duplicate"])}
    headers = {'content-type': 'application/json'}
    requests.post(slackurl, data=json.dumps(payload))
    return 1

results = { "added" : 0, "duplicate" : 0}

# https://www.sqlite.org/lang_datefunc.html
for item in soup.find_all('div', class_="result-info"):
    #data = (ad['time'], ad['title'], ad['loctext'], ad['bedrooms'], ad['squarefeet'], ad['price'])
    housing = getHousing(item)
    title = getTitle(item)
    furnished = getFurnished(title)


    ad = {'time': getTime(item), 'title': getTitle(item), 'loctext': getLocation(item),
          'bedrooms': housing['bedrooms'], 'squarefeet': housing['squarefeet'],
          'price': getPrice(item), 'furnished': furnished }

    result = add_ad_to_db(ad) # either "added" or "duplicate"
    results[result] += 1


send_stats_to_slack(results)

con.commit()
con.close()
