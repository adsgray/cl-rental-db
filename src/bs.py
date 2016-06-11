#!/usr/bin/python

import ConfigParser
import sys
import codecs
import re
from bs4 import BeautifulSoup
import sqlite3 as lite
from sqlite3 import IntegrityError

config = ConfigParser.ConfigParser()
config.read("config.ini")
dbpath = config.get("main", "dbpath")

soup = BeautifulSoup(codecs.open(sys.argv[1], "r", "utf-8"), "lxml")

# wheee global db variables (traditional)
con = lite.connect(dbpath)
con.text_factory = str
cur = con.cursor()


def add_ad_to_db(ad):
    """
    Add this ad to the db
    """
    add = ('INSERT INTO ad (time, title, loctext, bedrooms, squarefeet, price) values(?,?,?,?,?,?)')
    data = (ad['time'], ad['title'], ad['loctext'], ad['bedrooms'], ad['squarefeet'], ad['price'])
    try:
        cur.execute(add, data)
    except IntegrityError:
        print("constraint fail")
        print(ad)


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
    title = item.find('span', {"id": 'titletextonly'})
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
    p = item.find_all('span', class_='price')
    try:
        raw = p[0].contents[0]
        m = re.search("\$(\d+)", raw)
        if m:
            return m.group(1)
        else:
            return 0
    except IndexError:
        return -1

def getLocation(item):
    loc = item.find_all('span', class_='pnr')
    raw = loc[0].contents[1].contents[0]
    m = re.search("\((.+)\)", raw)
    if m:
        return m.group(1).encode("utf-8")
    else:
        return ""


# https://www.sqlite.org/lang_datefunc.html

for item in soup.find_all('p', class_="row"):
    #data = (ad['time'], ad['title'], ad['loctext'], ad['bedrooms'], ad['squarefeet'], ad['price'])
    housing = getHousing(item)
    ad = {'time': getTime(item), 'title': getTitle(item), 'loctext': getLocation(item), 'bedrooms': housing['bedrooms'], 'squarefeet': housing['squarefeet'], 'price': getPrice(item) }
    add_ad_to_db(ad)

con.commit()
con.close()
